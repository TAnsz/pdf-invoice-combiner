# 更新日志

所有重要的项目变更都记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)
并且本项目遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/) 版本规范。

## [1.0.0] - 2026-04-03

### 新增
- ✨ 首个正式版本发布
- 📄 智能页面合并功能，自动判断两个页面是否能缩放后放入一个 A4 页面
- 🧹 自动白边裁剪，智能检测并删除 PDF 页面周围的大白空白
- 📊 按高度排序，相似高度的页面优先配对，最大化合并效率
- 🔄 递归搜索，自动扫描输入目录及所有子目录中的 PDF 文件
- 💾 安全输出，合并前自动删除已存在的输出文件
- 📦 支持独立 EXE 打包，Windows 用户无需安装 Python
- 📖 完整的文档和示例代码
- 🤖 GitHub Actions 自动构建和发布 CI/CD

### 技术细节
- 使用 PyMuPDF (fitz) 库进行 PDF 操作
- 支持 Python 3.7+
- 可打包为独立 Windows EXE（使用 PyInstaller）

### 已知限制
- 仅在 Windows 上测试 EXE 版本（理论上支持 macOS/Linux）
- 不支持加密或受保护的 PDF
- 文字提取和裁剪基于内容边界检测，可能在复杂排版上有偏差

---

## 计划中的功能

- [ ] 支持自定义边距和缩放比例
- [ ] 支持 PDF 添加水印或页码
- [ ] 支持不同的输出尺寸（A3、Letter 等）
- [ ] 图形化用户界面（GUI）
- [ ] 更多的自动化选项（如按特定规则分组）

---

## 如何贡献

欢迎提交 Issue 和 Pull Request！

如果你发现了 bug 或有新功能建议，请在 [Issues](https://github.com/your-username/pdf-invoice-combiner/issues) 中提出。

---

**感谢所有贡献者！** 🙏
