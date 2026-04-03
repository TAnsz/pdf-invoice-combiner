# 📑 项目文档索引

欢迎！这是 PDF 发票合并工具的完整项目包。以下是所有文档的导航索引。

## 🎯 快速导航

根据你的需求，选择相应的文档：

### 👤 我是普通用户，想使用工具

1. **首先看**: [QUICKSTART.md](QUICKSTART.md) - 3 分钟快速上手
2. **获取详情**: [README.md](README.md) - 完整功能说明
3. **遇到问题**: [README.md#故障排除](README.md#故障排除) - FAQ

**下载方式**：
- Windows 用户：从 [Releases](https://github.com/your-username/pdf-invoice-combiner/releases) 下载 EXE
- 开发者：`git clone` 项目后 `pip install -r requirements.txt`

---

### 💻 我是开发者，想修改或扩展代码

1. **了解项目**: [README.md](README.md) - 功能和原理
2. **项目结构**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 项目完成清单
3. **构建 EXE**: 
   - 使用 PowerShell: `.\build_exe.ps1`
   - 使用 Python: `python build_exe.py`
4. **发布到 GitHub**: [GITHUB_UPLOAD.md](GITHUB_UPLOAD.md)

---

### 🚀 我要上传到 GitHub

**请按顺序查看**：

1. [GITHUB_UPLOAD.md](GITHUB_UPLOAD.md) - 详细上传步骤
2. [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - 上传前检查清单
3. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 项目总结

**上传完成后**：
- 在仓库 Settings 中启用 GitHub Actions
- 推送带有 tag 的提交触发自动 EXE 构建
- 在 Releases 页面发布版本

---

### 📚 我想了解所有细节

**文档完整阅读顺序**：

| # | 文档 | 内容 | 阅读时间 |
|---|------|------|---------|
| 1 | [README.md](README.md) | 项目概览、功能、安装、使用 | 15 分钟 |
| 2 | [QUICKSTART.md](QUICKSTART.md) | 快速开始示例 | 5 分钟 |
| 3 | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | 项目结构和技术细节 | 10 分钟 |
| 4 | [GITHUB_UPLOAD.md](GITHUB_UPLOAD.md) | 上传发布步骤 | 10 分钟 |
| 5 | [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) | 上传前检查 | 5 分钟 |
| 6 | [CHANGELOG.md](CHANGELOG.md) | 版本历史 | 3 分钟 |
| 7 | [LICENSE](LICENSE) | 许可证条款 | 5 分钟 |

**总计**: 约 1 小时

---

## 📂 文件说明

### 核心脚本
- **combine_pdfs_two_per_a4.py** - 主脚本，包含所有 PDF 合并逻辑

### 构建工具
- **build_exe.py** - Python 脚本构建工具
- **build_exe.ps1** - PowerShell 构建工具
- **setup.py** - Python 包配置（用于 pip 安装）

### 依赖文件
- **requirements.txt** - Python 依赖清单
- **.gitignore** - Git 忽略规则

### 文档（用户向）
- **README.md** ⭐⭐⭐⭐⭐ - 项目主说明
- **QUICKSTART.md** ⭐⭐⭐⭐ - 快速开始指南
- **CHANGELOG.md** - 版本更新日志
- **LICENSE** - MIT 许可证

### 文档（开发者向）
- **GITHUB_UPLOAD.md** - GitHub 上传步骤
- **DEPLOYMENT_CHECKLIST.md** - 上传检查清单
- **PROJECT_SUMMARY.md** - 项目完成总结
- **FILES_CREATED.md** - 文件清单说明

### GitHub 配置
- **.github/workflows/build.yml** - GitHub Actions 自动构建

---

## ✨ 项目特色

```
PDF 发票合并工具
├── 🚀 开箱即用
│   ├── EXE 版本无需依赖
│   ├── 可视化步骤指导
│   └── 命令行友好
│
├── 📚 文档完整
│   ├── 中文说明
│   ├── 使用示例
│   └── 故障排查
│
├── 🎯 功能强大
│   ├── 智能页面合并
│   ├── 自动白边裁剪
│   ├── 递归搜索 PDF
│   └── 按高度优化配对
│
├── 🔧 易于扩展
│   ├── 代码清晰
│   ├── 注释详细
│   └── 模块化设计
│
└── 📄 开源免费
    ├── MIT 许可证
    ├── GitHub 托管
    └── 社区支持
```

---

## 🎓 学习路径

### 初级用户（只想用工具）
```
QUICKSTART.md → 下载 EXE → 使用 → 完成
```

### 中级用户（想理解原理）
```
README.md → 阅读脚本代码 → PROJECT_SUMMARY.md → 理解
```

### 高级用户（要修改和发布）
```
README.md → 修改代码 → build_exe.ps1 → GITHUB_UPLOAD.md → 发布
```

---

## 🔗 外部链接

- **GitHub 仓库**: https://github.com/your-username/pdf-invoice-combiner
- **Releases 页面**: https://github.com/your-username/pdf-invoice-combiner/releases
- **Issues 页面**: https://github.com/your-username/pdf-invoice-combiner/issues
- **PyMuPDF 文档**: https://pymupdf.readthedocs.io/
- **Python 官网**: https://www.python.org/

---

## 💡 常见问题

### Q: 从哪里开始？
A: 
- 如果你是**用户**：从 [QUICKSTART.md](QUICKSTART.md) 开始
- 如果你是**开发者**：从 [README.md](README.md) 开始
- 如果你要**上传 GitHub**：从 [GITHUB_UPLOAD.md](GITHUB_UPLOAD.md) 开始

### Q: 各个文件的用途是什么？
A: 查看 [FILES_CREATED.md](FILES_CREATED.md) 了解每个文件的详细说明

### Q: 如何生成 EXE？
A: 
```powershell
# 方式 1：PowerShell
.\build_exe.ps1

# 方式 2：Python
python build_exe.py
```

### Q: 如何上传到 GitHub？
A: 按照 [GITHUB_UPLOAD.md](GITHUB_UPLOAD.md) 中的步骤进行

### Q: 代码可以商用吗？
A: 可以，详见 [LICENSE](LICENSE) - MIT 许可证允许商用

---

## 🎯 建议阅读顺序

根据你的目标，选择最合适的路径：

### 路径 1：我想立即使用工具
1. [QUICKSTART.md](QUICKSTART.md)
2. 下载 EXE 或按步骤安装
3. 开始使用

### 路径 2：我想理解项目
1. [README.md](README.md) - 了解功能
2. 阅读 `combine_pdfs_two_per_a4.py` 源码
3. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 技术细节

### 路径 3：我想发布到 GitHub
1. [README.md](README.md) - 了解项目
2. 修改必要信息（setup.py, README.md 中的链接）
3. [GITHUB_UPLOAD.md](GITHUB_UPLOAD.md) - 按步骤上传
4. [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - 检查清单

---

## 📞 获得帮助

| 问题类型 | 去哪里找答案 |
|--------|-----------|
| 如何使用工具 | [QUICKSTART.md](QUICKSTART.md) / [README.md](README.md) |
| 功能说明 | [README.md](README.md#功能特性) |
| 报错信息 | [README.md#故障排除](README.md#故障排除) |
| 代码修改 | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |
| GitHub 上传 | [GITHUB_UPLOAD.md](GITHUB_UPLOAD.md) |
| 检查清单 | [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) |

---

## 🎉 你已经拥有

一个**完整的、专业的、生产级的** PDF 工具项目，包括：

✅ 功能完整的主脚本
✅ 自动构建 EXE 的脚本
✅ 详细的中文文档
✅ GitHub Actions CI/CD
✅ 完整的项目结构
✅ MIT 许可证
✅ 上传指南

**现在就可以上传到 GitHub 并分享给他人！** 🚀

---

**最后更新**: 2026 年 4 月 3 日
**项目版本**: v1.0.0
**许可证**: MIT

**祝你项目成功！** 🎊
