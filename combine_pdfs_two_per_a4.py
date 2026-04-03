#!/usr/bin/env python3
"""
combine_pdfs_two_per_a4.py

将目录下的多个 PDF 中的页面两张合并到一张 A4 页面上。
输出为一个合并的 PDF 文件。

功能特性:
- 自动裁剪掉 PDF 页面周围的大白边
- 智能配对相邻页面，若缩放后能放入一个 A4 页面则合并（上下布局）
- 页面按高度排序，相似高度的页面优先配对
- 输出前自动删除已存在的文件，确保生成最新结果

依赖:
  pip install pymupdf

参数说明:
  input_dir     (可选) 输入 PDF 目录，递归搜索所有 PDF 文件。默认: 当前目录 '.'
  output_pdf    (可选) 输出合并后 PDF 的文件路径。默认: 当前目录下的 'merged.pdf'

布局说明:
- 输出 PDF 采用 A4 纵向（595.276 × 841.89 points）
- 两个原始页面各占半页高度（每个约 420.9pt）
- 页面在其半页内水平居中，顶部和底部各留 10pt 边距，左右各留 20pt 边距
- 如果页面超过 A4 宽度，则按比例缩放，保持宽高比不变

使用示例:

1. 最简单用法（使用所有默认值）:
   python combine_pdfs_two_per_a4.py
   # 搜索当前目录所有 PDF，合并后输出到 merged.pdf

2. 指定输入目录:
   python combine_pdfs_two_per_a4.py d:\\tmp\\invoices
   # 搜索 d:\\tmp\\invoices 及其子目录中所有 PDF，合并后输出到当前目录的 merged.pdf

3. 同时指定输入目录和输出文件:
   python combine_pdfs_two_per_a4.py d:\\tmp\\invoices d:\\output\\merged.pdf
   # 搜索 d:\\tmp\\invoices，合并后输出到 d:\\output\\merged.pdf

4. 输出到特定目录（假设输入为当前目录）:
   python combine_pdfs_two_per_a4.py . d:\\output\\result.pdf
"""
import sys
import os
import fitz  # PyMuPDF
from pathlib import Path

# Landscape A4 for output (swap)
A4_WIDTH = 595.276  # points (72 dpi): 210mm
A4_HEIGHT = 841.89  # points (72 dpi): 297mm
A4_LANDSCAPE_WIDTH = A4_HEIGHT
A4_LANDSCAPE_HEIGHT = A4_WIDTH


def collect_pdf_pages(input_dir):
    paths = sorted(Path(input_dir).glob("**/*.pdf"))
    pages = []
    for p in paths:
        try:
            doc = fitz.open(p.as_posix())
        except Exception as e:
            print(f"无法打开 {p}: {e}")
            continue
        for pno in range(len(doc)):
            pages.append((p.as_posix(), pno))
        doc.close()
    return pages


def get_trimmed_rect(page, min_shrink_ratio=0.1):
    """计算页面内容区域，包含文本块和绘制元素（线条、边框等）。
    如果白边比例大于 min_shrink_ratio，返回内容区域，否则返回整页。
    """
    orig_rect = page.rect
    content_rect = None

    # 文本块（text blocks）
    blocks = page.get_text("blocks")
    for b in blocks:
        r = fitz.Rect(b[:4])
        content_rect = r if content_rect is None else (content_rect | r)

    # 绘图对象（线条、图形）; 避免把表格边线裁掉
    drawings = page.get_drawings()
    for d in drawings:
        if "rect" in d and d["rect"]:
            drect = fitz.Rect(d["rect"])
            content_rect = drect if content_rect is None else (content_rect | drect)
        if "items" in d and d["items"]:
            for item in d["items"]:
                if not item or len(item) < 2:
                    continue
                typ, data = item[0], item[1]
                if typ == "l" and isinstance(data, (tuple, list)) and len(data) == 4:
                    x0, y0, x1, y1 = data
                    lrect = fitz.Rect(x0, y0, x1, y1)
                    content_rect = lrect if content_rect is None else (content_rect | lrect)
                elif typ == "re" and isinstance(data, (tuple, list)) and len(data) == 4:
                    x0, y0, w, h = data
                    rrect = fitz.Rect(x0, y0, x0 + w, y0 + h)
                    content_rect = rrect if content_rect is None else (content_rect | rrect)

    if content_rect is None:
        return orig_rect, False

    content_rect = content_rect.intersect(orig_rect)
    if content_rect.is_empty:
        return orig_rect, False

    if ((orig_rect.width - content_rect.width) / orig_rect.width >= min_shrink_ratio or
            (orig_rect.height - content_rect.height) / orig_rect.height >= min_shrink_ratio):
        return content_rect, True
    return orig_rect, False


def merge_two_per_a4(pages, out_path):
    """
    将两页按上下顺序放到纵向 A4 页面上，不进行任何缩放，直接覆盖输出文件（若存在）。
    上半页放第一页，下半页放第二页。
    """
    out_doc = fitz.open()
    total = len(pages)
    i = 0
    half_height = A4_HEIGHT * 0.5
    threshold_height = A4_HEIGHT * 0.5  # 用 A4/2 作为合并阈值
    margin_x = 20.0
    margin_y = 10.0
    while i < total:
        # inspect current page
        src_path, pno, need_trim, trim_rect, effective_rect = pages[i]
        try:
            src_doc = fitz.open(src_path)
            page = src_doc[pno]
        except Exception:
            i += 1
            continue
        page_rect = trim_rect if (need_trim and trim_rect is not None) else effective_rect
        
        # 尝试与下一页配对（无论 oversized 否）
        can_pair = False
        pair_scale = 1.0
        if i + 1 < total:
            next_path, next_pno, next_need_trim, next_trim_rect, next_effective_rect = pages[i + 1]
            next_rect = next_trim_rect if next_need_trim and next_trim_rect is not None else next_effective_rect
            
            # 判断两个页面通过缩放是否都能放入半页
            max_w = A4_WIDTH - 2 * margin_x
            max_half_h = half_height - 2 * margin_y
            pair_scale = min(max_w / page_rect.width, max_w / next_rect.width,
                        max_half_h / page_rect.height, max_half_h / next_rect.height)
            if pair_scale > 0:
                can_pair = True
        
        if can_pair:
            # pair i (top) and i+1 (bottom)
            next_path, next_pno, next_need_trim, next_trim_rect, next_effective_rect = pages[i + 1]
            next_rect = next_trim_rect if next_need_trim and next_trim_rect is not None else next_effective_rect
            next_doc = None
            try:
                next_doc = fitz.open(next_path)
            except Exception:
                next_doc = None
            
            new_page = out_doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)
            max_w = A4_WIDTH - 2 * margin_x
            max_half_h = half_height - 2 * margin_y

            # top (current)
            cur_place_rect = trim_rect if need_trim and trim_rect is not None else page_rect
            drawn_w = cur_place_rect.width * pair_scale
            drawn_h = cur_place_rect.height * pair_scale
            x0 = margin_x + (max_w - drawn_w) / 2.0
            y0 = margin_y
            rect1 = fitz.Rect(x0, y0, x0 + drawn_w, y0 + drawn_h)
            try:
                if need_trim and trim_rect is not None:
                    pix = src_doc[pno].get_pixmap(clip=trim_rect, matrix=fitz.Matrix(pair_scale * 2, pair_scale * 2), alpha=False)
                    new_page.insert_image(rect1, stream=pix.tobytes("png"))
                else:
                    new_page.show_pdf_page(rect1, src_path, pno)
            except Exception:
                pix = src_doc[pno].get_pixmap(matrix=fitz.Matrix(pair_scale * 2, pair_scale * 2), alpha=False)
                new_page.insert_image(rect1, stream=pix.tobytes("png"))

            # bottom (next)
            next_place_rect = next_trim_rect if next_need_trim and next_trim_rect is not None else next_rect
            drawn_w = next_place_rect.width * pair_scale
            drawn_h = next_place_rect.height * pair_scale
            x0 = margin_x + (max_w - drawn_w) / 2.0
            y0 = half_height + margin_y
            rect2 = fitz.Rect(x0, y0, x0 + drawn_w, y0 + drawn_h)
            try:
                if next_need_trim and next_trim_rect is not None:
                    pix = next_doc[next_pno].get_pixmap(clip=next_trim_rect, matrix=fitz.Matrix(pair_scale * 2, pair_scale * 2), alpha=False)
                    new_page.insert_image(rect2, stream=pix.tobytes("png"))
                else:
                    new_page.show_pdf_page(rect2, next_path, next_pno)
            except Exception:
                pix = next_doc[next_pno].get_pixmap(matrix=fitz.Matrix(pair_scale * 2, pair_scale * 2), alpha=False)
                new_page.insert_image(rect2, stream=pix.tobytes("png"))

            try:
                src_doc.close()
            except Exception:
                pass
            try:
                if next_doc is not None:
                    next_doc.close()
            except Exception:
                pass

            i += 2
            continue

        # can't pair with next (either no next or next oversized): place current alone in top half
        new_page = out_doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)
        try:
            src_doc = fitz.open(src_path)
            src_rect = src_doc[pno].rect
            drawn_w = src_rect.width
            drawn_h = src_rect.height
            src_doc.close()
            x0 = (A4_WIDTH - drawn_w) / 2.0
            # align top of half to avoid clipping when tall
            y0 = 0
            rect1 = fitz.Rect(x0, y0, x0 + drawn_w, y0 + drawn_h)
            new_page.show_pdf_page(rect1, src_path, pno)
        except Exception:
            src_doc = fitz.open(src_path)
            pix = src_doc[pno].get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            src_doc.close()
            new_page.insert_image(rect1, stream=pix.tobytes("png"))
        i += 1
    # 直接覆盖目标文件（若存在，先尝试删除）
    try:
        if os.path.exists(out_path):
            os.remove(out_path)
    except Exception:
        pass
    out_doc.save(out_path)
    out_doc.close()


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='将目录下多 PDF 的页面两页合并为一页 A4（上下），并输出到单个 PDF。',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python combine_pdfs_two_per_a4.py
  python combine_pdfs_two_per_a4.py d:\\tmp\\invoices
  python combine_pdfs_two_per_a4.py d:\\tmp\\invoices d:\\output\\merged.pdf
        '''
    )
    parser.add_argument('input_dir', nargs='?', default='.', 
                       help='输入目录（递归搜索所有 PDF），默认为当前目录 "."')
    parser.add_argument('output_pdf', nargs='?', default='merged.pdf', 
                       help='输出 PDF 文件路径，默认为 "merged.pdf"')
    args = parser.parse_args()
    input_dir = args.input_dir
    out_pdf = args.output_pdf
    if not os.path.isdir(input_dir):
        print(f"输入目录不存在: {input_dir}")
        sys.exit(1)
    pages = collect_pdf_pages(input_dir)
    if not pages:
        print("在目录中未发现 PDF 文件或页面为空。")
        sys.exit(1)
    # 将能合并到一页（A5: width <= A4_WIDTH, height <= A4_HEIGHT/2）的页面排在前面
    fit_pages = []
    oversized_pages = []
    half_height = A4_HEIGHT * 0.5
    for src_path, pno in pages:
        try:
            doc = fitz.open(src_path)
            page = doc[pno]
            trim_rect, need_trim = get_trimmed_rect(page, min_shrink_ratio=0.15)
            if need_trim:
                effective_rect = trim_rect
            else:
                effective_rect = page.rect
            doc.close()
        except Exception:
            continue

        item = (src_path, pno, need_trim, trim_rect, effective_rect)
        if effective_rect.width <= A4_WIDTH and effective_rect.height <= half_height:
            fit_pages.append(item)
        else:
            oversized_pages.append(item)

    # 对 oversized_pages 按高度升序排列，让相似高度的页面挨在一起便于配对
    oversized_pages.sort(key=lambda x: x[4].height)
    ordered_pages = fit_pages + oversized_pages
    print(f"收集 PDF 页面...找到 {len(pages)} 页，开始合并...")
    
    # 删除已存在的输出文件
    if os.path.exists(out_pdf):
        try:
            os.remove(out_pdf)
        except Exception:
            pass
    
    merge_two_per_a4(ordered_pages, out_pdf)
    print(f"已生成: {out_pdf}")


if __name__ == '__main__':
    main()
