# 快速开始指南

## 3 分钟快速上手

### 方式 1：使用 EXE（推荐 Windows 用户）

1. 从 [Releases](https://github.com/your-username/pdf-invoice-combiner/releases) 下载 `combine_pdfs.exe`
2. 将 PDF 文件放在一个文件夹中，如 `D:\invoices`
3. 打开命令行（CMD 或 PowerShell），运行：
   ```
   combine_pdfs.exe D:\invoices D:\output\merged.pdf
   ```
4. 等待完成，检查输出文件

**就这么简单！** ✨

### 方式 2：使用 Python 脚本

1. 确保已安装 Python 3.7+
2. 克隆项目：
   ```bash
   git clone https://github.com/your-username/pdf-invoice-combiner.git
   cd pdf-invoice-combiner
   ```
3. 安装依赖：
   ```bash
   pip install pymupdf
   ```
4. 运行脚本：
   ```bash
   python combine_pdfs_two_per_a4.py D:\invoices D:\output\merged.pdf
   ```

## 常见问题

### Q1: 为什么有些页面没有合并？
**A:** 脚本会自动判断两个页面缩放后是否能放入一个 A4 页面。如果页面太大，会自动单独放置。这是正常行为。

### Q2: 怎样查看详细的帮助？
**A:** 
- 运行 `combine_pdfs.exe -h` 或 `python combine_pdfs_two_per_a4.py -h`

### Q3: 输出文件很大怎么办？
**A:** 
- 输出 PDF 的大小取决于源 PDF 的尺寸和复杂度
- 可以用 PDF 压缩工具进一步压缩，如 [SmallPDF](https://smallpdf.com) 或 Adobe Reader

### Q4: 能否自定义输出布局？
**A:** 
- 目前脚本固定为上下布局（两页合一）
- 可以修改源代码中的 `combine_pdfs_two_per_a4.py` 来自定义
- 或在 Issue 中提交功能请求

### Q5: 支持其他操作系统吗？
**A:** 
- Python 版本支持 Windows、macOS、Linux
- EXE 版本仅在 Windows 上可用
- 可以尝试使用 Python 版本在其他系统上运行

## 典型使用场景

### 场景 1：合并月度发票

```bash
# 目录结构
C:\invoices\202604\
  ├── invoice_001.pdf
  ├── invoice_002.pdf
  └── invoice_003.pdf

# 合并
combine_pdfs.exe C:\invoices\202604 C:\invoices\202604_merged.pdf
```

### 场景 2：合并多个月份

```bash
# 一次合并整个目录树
combine_pdfs.exe C:\invoices C:\invoices\all_months_merged.pdf

# 脚本会递归搜索所有子目录
```

### 场景 3：定期自动化合并

创建 PowerShell 脚本（如 `daily_merge.ps1`）：

```powershell
# 每天自动合并今天的发票
$today = Get-Date -Format "yyyy-MM-dd"
$inputDir = "C:\invoices\daily\$today"
$outputFile = "C:\invoices\merged\$today.pdf"

if (Test-Path $inputDir) {
    & 'C:\path\to\combine_pdfs.exe' $inputDir $outputFile
    Write-Host "✅ 已合并 $today 的发票"
} else {
    Write-Host "⚠️  今天没有新发票"
}
```

然后在 Windows 任务计划程序中设置定时运行。

## 获取帮助

- 📖 查看完整 [README.md](README.md)
- 🐛 报告 Bug: [Issues](https://github.com/your-username/pdf-invoice-combiner/issues)
- 💬 功能建议: [Discussions](https://github.com/your-username/pdf-invoice-combiner/discussions)

---

祝你使用愉快！ 🎉
