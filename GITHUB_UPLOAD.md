# GitHub 上传指南

按照以下步骤将项目上传到 GitHub：

## 1. 创建 GitHub 仓库

1. 访问 [github.com](https://github.com)
2. 点击右上角 `+` → `New repository`
3. 仓库名：`pdf-invoice-combiner`
4. 描述：`Intelligently combine multiple PDF pages into A4 pages (2-per-page layout)`
5. 选择 `Public`（公开）
6. **勾选** `Initialize this repository with: Add a README file` - **不勾选**（我们已有 README）
7. 点击 `Create repository`

## 2. 初始化本地 Git（如果还未初始化）

```bash
cd d:\Code\pdf

# 初始化 Git
git init

# 配置 Git 用户信息（如果还未配置过）
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/TAnsz/pdf-invoice-combiner.git
```

## 3. 提交和推送代码

```bash
cd d:\Code\pdf

# 添加所有文件
git add .

# 提交更改
git commit -m "Initial commit: PDF invoice combiner with auto-merge and crop features"

# 推送到 GitHub（使用 main 分支）
git branch -M main
git push -u origin main
```

## 4. 创建第一个 Release（版本发布）

### 通过 GitHub 网页界面：

1. 访问 https://github.com/TAnsz/pdf-invoice-combiner
2. 右侧找到 `Releases` 或点击 `Create a release`
3. 点击 `Draft a new release`
4. **Tag version**: `v1.0.0`
5. **Release title**: `Release v1.0.0 - Initial Release`
6. **Description**:
   ```
   # PDF Invoice Combiner v1.0.0

   ## 功能
   - ✨ 智能页面合并
   - 📄 自动白边裁剪
   - 📊 按高度排序以优化配对
   - 🚀 支持独立 EXE 版本

   ## 下载
   - 选择下面的 `combine_pdfs.exe` 下载 Windows 版本
   - 或从源码运行 Python 版本

   ## 快速开始
   详见 [QUICKSTART.md](QUICKSTART.md)
   ```
7. 点击 `Publish release`

### 通过命令行（可选）：

```bash
cd d:\Code\pdf

# 创建 tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# 推送 tag 到 GitHub
git push origin v1.0.0
```

## 5. 自动构建 EXE（可选但推荐）

项目中已包含 GitHub Actions 工作流（`.github/workflows/build.yml`）。

当你推送 tag 时，GitHub 会自动：
1. 构建 EXE 文件
2. 创建 Release
3. 上传 EXE 到 Release 页面

这样用户就可以直接下载 EXE 使用了！

**注意**：首次使用 GitHub Actions 可能需要启用权限：
1. 访问仓库的 Settings → Actions → General
2. 确保 `Actions permissions` 设置为允许

## 6. 更新仓库信息

完成以上步骤后，建议：

1. 更新 README.md 中的 GitHub 链接（搜索 `your-username`）
2. 添加仓库的 Topics（右侧 About 部分）：
   - `pdf`
   - `invoice`
   - `merge`
   - `pdf-tools`
   - `python`
   - `windows`

3. 在 GitHub 个人资料中添加项目链接

## 7. 定期更新

```bash
# 修改代码后
git add .
git commit -m "描述你的更改"
git push origin main

# 发布新版本
git tag -a v1.0.1 -m "Fix: bug fixes"
git push origin v1.0.1
```

## 文件清单

以下文件已为你创建，可直接上传：

```
📁 pdf-invoice-combiner/
├── 📄 combine_pdfs_two_per_a4.py    # 主脚本
├── 📄 build_exe.py                   # Python 构建脚本
├── 📄 build_exe.ps1                  # PowerShell 构建脚本
├── 📄 setup.py                       # Python 包配置
├── 📄 requirements.txt               # 依赖列表
├── 📄 README.md                      # 项目说明（中文）
├── 📄 QUICKSTART.md                  # 快速开始指南
├── 📄 CHANGELOG.md                   # 更新日志
├── 📄 LICENSE                        # MIT 许可证
├── 📄 .gitignore                     # Git 忽略列表
└── 📁 .github/
    └── 📁 workflows/
        └── 📄 build.yml              # GitHub Actions 自动构建配置
```

## 常见问题

### Q: 如何修改 GitHub Actions 工作流？

A: 编辑 `.github/workflows/build.yml`，修改后 push 即可生效。

### Q: 如何删除已推送的文件？

A: 
```bash
# 从 Git 中移除但保留本地文件
git rm --cached filename.pdf

# 提交更改
git commit -m "Remove large file"

# 推送
git push origin main
```

### Q: 如何回滚到之前的版本？

A:
```bash
# 查看提交历史
git log --oneline

# 回滚到特定提交
git reset --hard commit-hash
git push origin main --force
```

### Q: 怎样邀请协作者？

A: 在 GitHub 仓库页面 → Settings → Collaborators → 添加用户名

---

祝你 GitHub 之旅愉快！🚀

有问题可以参考 [GitHub 官方文档](https://docs.github.com)
