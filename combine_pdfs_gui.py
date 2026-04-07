#!/usr/bin/env python3
"""
combine_pdfs_gui.py

PDF 发票合并工具 - 图形界面版本

将目录下的多个 PDF 中的页面两张合并到一张 A4 页面上。
提供友好的图形界面进行文件选择和操作。

功能特性:
- 自动裁剪掉 PDF 页面周围的大白边
- 智能配对相邻页面，若缩放后能放入一个 A4 页面则合并（上下布局）
- 页面按高度排序，相似高度的页面优先配对
- 图形界面：选择输入文件夹或单个文件，选择输出位置
- 实时显示处理进度和结果信息

依赖:
  pip install pymupdf tkinter

使用方法:
  python combine_pdfs_gui.py
"""

import sys
import os
import fitz  # PyMuPDF
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import threading
import time

# Landscape A4 for output (swap)
A4_WIDTH = 595.276  # points (72 dpi): 210mm
A4_HEIGHT = 841.89  # points (72 dpi): 297mm

# Merge threshold: half of A4 height
MERGE_THRESHOLD = A4_HEIGHT / 2  # 420.945 points

# Margins
MARGIN_TOP = 10
MARGIN_BOTTOM = 10
MARGIN_LEFT = 20
MARGIN_RIGHT = 20

class PDFMergerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF 发票合并工具 v1.0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Variables
        self.input_mode = tk.StringVar(value="folder")  # "folder" or "file"
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.pdf_files = []
        self.is_processing = False

        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="输入设置", padding="5")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)

        # Input mode selection
        ttk.Label(input_frame, text="输入类型:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        mode_frame = ttk.Frame(input_frame)
        mode_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Radiobutton(mode_frame, text="文件夹", variable=self.input_mode,
                       value="folder", command=self.on_mode_change).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(mode_frame, text="单个文件", variable=self.input_mode,
                       value="file", command=self.on_mode_change).pack(side=tk.LEFT)

        # Input path selection
        ttk.Label(input_frame, text="输入路径:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        path_frame = ttk.Frame(input_frame)
        path_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        path_frame.columnconfigure(0, weight=1)
        ttk.Entry(path_frame, textvariable=self.input_path).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(path_frame, text="浏览...", command=self.browse_input).grid(row=0, column=1)

        # PDF files list
        ttk.Label(input_frame, text="PDF 文件列表:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 5))
        list_frame = ttk.Frame(input_frame)
        list_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.file_listbox = tk.Listbox(list_frame, height=8)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)

        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        ttk.Button(list_frame, text="刷新列表", command=self.refresh_file_list).grid(row=1, column=0, pady=(5, 0))

        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="输出设置", padding="5")
        output_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)

        ttk.Label(output_frame, text="输出文件:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        output_path_frame = ttk.Frame(output_frame)
        output_path_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        output_path_frame.columnconfigure(0, weight=1)
        ttk.Entry(output_path_frame, textvariable=self.output_path).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(output_path_frame, text="浏览...", command=self.browse_output).grid(row=0, column=1)

        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="处理进度", padding="5")
        progress_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(0, weight=1)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))

        self.status_label = ttk.Label(progress_frame, text="就绪")
        self.status_label.grid(row=1, column=0, sticky=tk.W)

        # Log area
        log_frame = ttk.Frame(progress_frame)
        log_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))

        self.start_button = ttk.Button(button_frame, text="开始合并", command=self.start_merge)
        self.start_button.pack(side=tk.RIGHT, padx=(5, 0))

        ttk.Button(button_frame, text="退出", command=self.root.quit).pack(side=tk.RIGHT)

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        input_frame.rowconfigure(3, weight=1)

    def on_mode_change(self):
        self.input_path.set("")
        self.pdf_files = []
        self.file_listbox.delete(0, tk.END)

    def browse_input(self):
        if self.input_mode.get() == "folder":
            path = filedialog.askdirectory(title="选择输入文件夹")
            if path:
                self.input_path.set(path)
                self.refresh_file_list()
        else:
            path = filedialog.askopenfilename(
                title="选择 PDF 文件",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            if path:
                self.input_path.set(path)
                self.pdf_files = [path]
                self.file_listbox.delete(0, tk.END)
                self.file_listbox.insert(tk.END, os.path.basename(path))

    def browse_output(self):
        path = filedialog.asksaveasfilename(
            title="选择输出文件",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile="merged.pdf"
        )
        if path:
            self.output_path.set(path)

    def refresh_file_list(self):
        input_path = self.input_path.get()
        if not input_path:
            return

        if self.input_mode.get() == "folder":
            try:
                self.pdf_files = list(Path(input_path).rglob("*.pdf"))
                self.pdf_files.sort()
            except Exception as e:
                messagebox.showerror("错误", f"无法读取文件夹: {e}")
                return
        else:
            if input_path.lower().endswith('.pdf'):
                self.pdf_files = [input_path]
            else:
                self.pdf_files = []

        self.file_listbox.delete(0, tk.END)
        for pdf_file in self.pdf_files:
            self.file_listbox.insert(tk.END, os.path.basename(pdf_file))

        self.log_message(f"找到 {len(self.pdf_files)} 个 PDF 文件")

    def log_message(self, message):
        self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def start_merge(self):
        if self.is_processing:
            return

        if not self.pdf_files:
            messagebox.showwarning("警告", "请先选择输入文件")
            return

        output_path = self.output_path.get()
        if not output_path:
            messagebox.showwarning("警告", "请选择输出文件路径")
            return

        # Disable start button
        self.start_button.config(state="disabled")
        self.is_processing = True

        # Start processing in background thread
        thread = threading.Thread(target=self.process_pdfs, args=(output_path,))
        thread.daemon = True
        thread.start()

    def process_pdfs(self, output_path):
        try:
            self.progress_var.set(0)
            self.status_label.config(text="正在分析 PDF 文件...")

            # Collect all pages from all PDFs
            all_pages = []
            total_files = len(self.pdf_files)

            for i, pdf_path in enumerate(self.pdf_files):
                self.log_message(f"正在处理: {os.path.basename(pdf_path)}")
                try:
                    doc = fitz.open(pdf_path)
                    for page_num in range(len(doc)):
                        page = doc[page_num]
                        rect = self.get_trimmed_rect(page)
                        effective_rect = self.get_effective_rect(rect)

                        all_pages.append({
                            'path': pdf_path,
                            'page_num': page_num,
                            'rect': rect,
                            'effective_rect': effective_rect,
                            'doc': doc
                        })

                    # Don't close doc here, we'll need it later
                    self.progress_var.set((i + 1) / total_files * 30)

                except Exception as e:
                    self.log_message(f"错误处理文件 {pdf_path}: {e}")

            if not all_pages:
                self.log_message("没有找到有效的 PDF 页面")
                return

            self.log_message(f"共找到 {len(all_pages)} 个页面")

            # Sort pages by height for better pairing
            self.status_label.config(text="正在排序页面...")
            all_pages.sort(key=lambda x: x['effective_rect'].height, reverse=True)

            # Create output PDF
            self.status_label.config(text="正在创建输出 PDF...")
            output_doc = fitz.open()

            # Process pages in pairs
            i = 0
            total_pages = len(all_pages)
            merged_count = 0

            while i < total_pages:
                if i + 1 < total_pages:
                    # Try to merge two pages
                    page1 = all_pages[i]
                    page2 = all_pages[i + 1]

                    if self.can_merge_pages(page1['effective_rect'], page2['effective_rect']):
                        # Merge two pages
                        self.merge_two_pages(output_doc, page1, page2)
                        merged_count += 1
                        self.log_message(f"合并页面: {os.path.basename(page1['path'])}:{page1['page_num']+1} + {os.path.basename(page2['path'])}:{page2['page_num']+1}")
                        i += 2
                    else:
                        # Can't merge, add first page alone
                        self.add_single_page(output_doc, page1)
                        self.log_message(f"单独添加页面: {os.path.basename(page1['path'])}:{page1['page_num']+1}")
                        i += 1
                else:
                    # Last page, add alone
                    self.add_single_page(output_doc, all_pages[i])
                    self.log_message(f"单独添加页面: {os.path.basename(all_pages[i]['path'])}:{all_pages[i]['page_num']+1}")
                    i += 1

                self.progress_var.set(30 + (i / total_pages) * 70)

            # Save output
            self.status_label.config(text="正在保存文件...")
            output_doc.save(output_path)
            output_doc.close()

            # Close all input documents
            for page_info in all_pages:
                page_info['doc'].close()

            self.progress_var.set(100)
            self.status_label.config(text="完成")

            messagebox.showinfo("完成",
                              f"PDF 合并完成!\n\n"
                              f"输入文件: {len(self.pdf_files)}\n"
                              f"总页面数: {total_pages}\n"
                              f"合并页面对: {merged_count}\n"
                              f"输出文件: {output_path}")

            self.log_message(f"合并完成! 输出文件: {output_path}")

        except Exception as e:
            messagebox.showerror("错误", f"处理过程中出现错误: {e}")
            self.log_message(f"错误: {e}")
        finally:
            self.start_button.config(state="normal")
            self.is_processing = False

    def get_trimmed_rect(self, page):
        """Get the trimmed rectangle by detecting content boundaries."""
        # Get all drawing elements and text blocks
        drawings = page.get_drawings()
        text_blocks = page.get_text("dict")["blocks"]

        # Collect all rectangles
        rects = []

        # From drawings
        for drawing in drawings:
            for item in drawing["items"]:
                if "rect" in item:
                    rects.append(fitz.Rect(item["rect"]))

        # From text blocks
        for block in text_blocks:
            if "bbox" in block:
                rects.append(fitz.Rect(block["bbox"]))

        if not rects:
            return page.rect

        # Union all rectangles
        union_rect = rects[0]
        for rect in rects[1:]:
            union_rect = union_rect | rect

        return union_rect

    def get_effective_rect(self, rect):
        """Calculate effective rectangle after scaling to fit A4 width."""
        width = rect.width
        height = rect.height

        if width > A4_WIDTH - MARGIN_LEFT - MARGIN_RIGHT:
            scale = (A4_WIDTH - MARGIN_LEFT - MARGIN_RIGHT) / width
            height *= scale

        return fitz.Rect(0, 0, A4_WIDTH - MARGIN_LEFT - MARGIN_RIGHT, height)

    def can_merge_pages(self, rect1, rect2):
        """Check if two pages can be merged into one A4 page."""
        total_height = rect1.height + rect2.height + MARGIN_TOP + MARGIN_BOTTOM
        return total_height <= MERGE_THRESHOLD

    def merge_two_pages(self, output_doc, page1_info, page2_info):
        """Merge two pages into one A4 page."""
        page = output_doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)

        # Calculate available height for each page
        available_height = (A4_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM) / 2

        # Page 1
        rect1 = page1_info['rect']
        scale1 = min(
            (A4_WIDTH - MARGIN_LEFT - MARGIN_RIGHT) / rect1.width,
            available_height / rect1.height
        )
        scaled_width1 = rect1.width * scale1
        scaled_height1 = rect1.height * scale1

        x1 = (A4_WIDTH - scaled_width1) / 2
        y1 = MARGIN_TOP

        page.show_pdf_page(fitz.Rect(x1, y1, x1 + scaled_width1, y1 + scaled_height1),
                          page1_info['doc'], page1_info['page_num'],
                          clip=rect1)

        # Page 2
        rect2 = page2_info['rect']
        scale2 = min(
            (A4_WIDTH - MARGIN_LEFT - MARGIN_RIGHT) / rect2.width,
            available_height / rect2.height
        )
        scaled_width2 = rect2.width * scale2
        scaled_height2 = rect2.height * scale2

        x2 = (A4_WIDTH - scaled_width2) / 2
        y2 = A4_HEIGHT / 2 + MARGIN_TOP

        page.show_pdf_page(fitz.Rect(x2, y2, x2 + scaled_width2, y2 + scaled_height2),
                          page2_info['doc'], page2_info['page_num'],
                          clip=rect2)

    def add_single_page(self, output_doc, page_info):
        """Add a single page to the output document."""
        page = output_doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)

        rect = page_info['rect']
        scale = min(
            (A4_WIDTH - MARGIN_LEFT - MARGIN_RIGHT) / rect.width,
            (A4_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM) / rect.height
        )
        scaled_width = rect.width * scale
        scaled_height = rect.height * scale

        x = (A4_WIDTH - scaled_width) / 2
        y = (A4_HEIGHT - scaled_height) / 2

        page.show_pdf_page(fitz.Rect(x, y, x + scaled_width, y + scaled_height),
                          page_info['doc'], page_info['page_num'],
                          clip=rect)


def main():
    root = tk.Tk()
    app = PDFMergerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()