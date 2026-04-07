# PDF 发票合并工具 (PDF Invoice Combiner)

一个快速、智能的 Python 工具，用于将目录中的多个 PDF 文件中的页面两张合并到一张 A4 页面上（上下布局），适合合并发票、单据等多页文档。

## 功能特性

- ✨ **智能页面合并**：自动判断相邻页面是否能缩放后放入一个 A4 页面
- 📄 **自动裁剪**：智能检测并删除 PDF 页面周围的大白边
- 📊 **按高度排序**：相似高度的页面优先配对，最大化合并效率
- 🎯 **递归搜索**：自动搜索输入目录及所有子目录中的 PDF 文件
- 💾 **安全输出**：合并前自动删除已存在的输出文件，确保生成最新结果
- �️ **图形界面**：提供直观的 GUI 版本，支持文件选择和进度显示
- �🚀 **开箱即用**：提供独立 EXE 版本，无需安装 Python

## 安装

### 方式 1：Python 脚本（需要 Python 3.7+）

```bash
# 克隆或下载本项目
git clone https://github.com/TAnsz/pdf-invoice-combiner.git
cd pdf-invoice-combiner

# 创建虚拟环境（推荐）
python -m venv venv
source venv/Scripts/activate  # Windows
# 或
# source venv/bin/activate    # macOS/Linux

# 安装依赖
pip install pymupdf

# 运行脚本
python combine_pdfs_two_per_a4.py
```

### 方式 2：图形界面版本（推荐）

```bash
# 安装额外依赖
pip install pymupdf tkinter

# 运行 GUI 版本
python combine_pdfs_gui.py
```

### 方式 3：独立 EXE（Windows，无需 Python）

从 [Releases](https://github.com/TAnsz/pdf-invoice-combiner/releases) 页面下载最新的 `combine_pdfs.exe`，双击运行即可打开图形界面。

## 使用方法

### GUI 版本（推荐）

1. **运行程序**：
   ```bash
   python combine_pdfs_gui.py
   # 或双击下载的 combine_pdfs.exe
   ```

2. **选择输入**：
   - 选择"文件夹"模式：浏览并选择包含 PDF 文件的文件夹
   - 或选择"单个文件"模式：选择特定的 PDF 文件

3. **选择输出**：
   - 点击"浏览"选择输出 PDF 文件的保存位置

4. **开始合并**：
   - 点击"开始合并"按钮
   - 查看进度条和日志了解处理状态

### 命令行版本

#### 基础用法

```bash
# 合并当前目录的所有 PDF，输出到 merged.pdf
python combine_pdfs_two_per_a4.py

# 指定输入目录
python combine_pdfs_two_per_a4.py "D:\invoices"

# 同时指定输入和输出路径
python combine_pdfs_two_per_a4.py "D:\invoices" "D:\output\merged.pdf"
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input_dir` | 输入目录（递归搜索所有 PDF）| `.`（当前目录）|
| `output_pdf` | 输出 PDF 文件路径 | `merged.pdf` |

### 获取帮助

```bash
python combine_pdfs_two_per_a4.py -h
```

## 工作原理

1. **扫描文件**：递归搜索输入目录中所有 `.pdf` 文件
2. **页面提取**：逐个打开 PDF，提取每一页
3. **自动裁剪**：检测页面内容，删除周围大白边（保留表格边框等）
4. **智能配对**：
   - 按高度升序排列所有页面
   - 对每一对相邻页面，计算缩放因子
   - 若缩放后两页都能放入一个 A4 页面（约 420.9pt 高），则合并
   - 否则页面单独占用一个 A4 页面
5. **生成输出**：将所有合并结果保存到一个 PDF 文件

## 输出格式

- **纸张**：A4 纵向（210×297mm）
- **布局**：
  - 两个原始页面上下排列（若可合并）
  - 每页各占约一半高度（420.9pt）
  - 页面在其半页内水平居中
  - 上下各留 10pt 边距，左右各留 20pt 边距
  - 页面宽度超过 A4 时自动按比例缩放

## 示例

### 场景：合并多个月份的发票

```bash
# 目录结构
D:\invoices\
  ├── 2026-01\
  │   ├── invoice_001.pdf
  │   └── invoice_002.pdf
  └── 2026-02\
      ├── invoice_003.pdf
      └── invoice_004.pdf

# 合并所有发票
python combine_pdfs_two_per_a4.py "D:\invoices" "D:\output\all_invoices_merged.pdf"

# 结果：一个合并好的 PDF 文件，包含所有发票页面（两两合并）
```

## 系统要求

### Python 版本
- Python 3.7 或更高版本
- 依赖：`pymupdf` (PyMuPDF)

### EXE 版本
- Windows 7 或更高版本
- 无需安装任何依赖

## 故障排除

| 问题 | 解决方案 |
|------|--------|
| `ModuleNotFoundError: No module named 'fitz'` | 运行 `pip install pymupdf` |
| 输入目录不存在错误 | 检查目录路径，使用完整路径（如 `D:\folder` 而非 `D:\folder\`） |
| 输出文件为空 | 检查输入目录中是否有有效的 PDF 文件 |
| 合并结果页面太小或太大 | 这是根据源 PDF 尺寸自动缩放的结果，属于正常行为 |

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v1.0.0 (2026-04-03)
- ✨ 首个正式版本发布
- 实现 PDF 页面智能合并
- 自动白边裁剪功能
- 支持独立 EXE 打包

## 联系方式

如有问题或建议，请在 [Issues](https://github.com/your-username/pdf-invoice-combiner/issues) 中提出。

---

**Made with ❤️ for invoice management**
