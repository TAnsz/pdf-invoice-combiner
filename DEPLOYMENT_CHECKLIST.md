# 📋 GitHub 上传前检查清单

在上传到 GitHub 前，请确保完成以下步骤：

## ✅ 代码检查

- [ ] 脚本可以正常运行：`python combine_pdfs_two_per_a4.py`
- [ ] 脚本能生成正确的 PDF 输出
- [ ] 没有硬编码的个人信息或路径
- [ ] 所有 import 都能正确导入
- [ ] 代码注释清晰，易于理解

## ✅ 文档检查

- [ ] README.md 内容完整且准确
- [ ] QUICKSTART.md 示例可以复制粘贴
- [ ] LICENSE 文件已创建（MIT）
- [ ] CHANGELOG.md 版本号与 setup.py 一致
- [ ] 所有 markdown 文件格式正确，无语法错误

## ✅ 项目配置检查

- [ ] setup.py 中的项目信息已更新：
  - [ ] name
  - [ ] version
  - [ ] author
  - [ ] author_email
  - [ ] url (GitHub 仓库链接)
  
- [ ] requirements.txt 包含所有依赖
- [ ] .gitignore 包含 Python 和 IDE 常见文件
- [ ] .github/workflows/build.yml 配置正确

## ✅ 文件清理

- [ ] 删除或忽略 test 输出的 PDF（merged.pdf）
- [ ] 不包含虚拟环境文件（.venv/）
- [ ] 不包含构建文件（dist/, build/）
- [ ] 不包含 IDE 配置文件（.vscode/, .idea/）
- [ ] 不包含 Python 缓存（__pycache__/）

## ✅ Git 配置检查

- [ ] Git 已初始化：`git status` 显示正确
- [ ] .gitignore 已生效（不显示不应提交的文件）
- [ ] 已配置 git user.name 和 user.email
- [ ] 第一次提交消息有意义

## ✅ GitHub 准备

- [ ] 已创建 GitHub 账户
- [ ] 已创建新的空仓库（不初始化 README）
- [ ] 复制了仓库的 HTTPS 链接
- [ ] README.md 中的 GitHub 链接已更新为实际链接

## 📋 最终清单

### 需要在 GitHub 上修改的地方

1. **README.md** - 搜索并替换 `your-username`：
   ```
   https://github.com/TAnsz/pdf-invoice-combiner
   ```
   替换为你的实际 GitHub 用户名

2. **setup.py** - 更新作者信息：
   ```python
   author="Your Name",
   author_email="your.email@example.com",
   url="https://github.com/TAnsz/pdf-invoice-combiner",
   ```

3. **QUICKSTART.md** - 如果有自定义需要，更新示例链接

## 🚀 上传步骤

```bash
# 1. 进入项目目录
cd d:\Code\pdf

# 2. 初始化 Git（如果还未初始化）
git init

# 3. 添加所有文件
git add .

# 4. 首次提交
git commit -m "Initial commit: PDF invoice combiner with auto-merge and crop features"

# 5. 添加远程仓库
git remote add origin https://github.com/TAnsz/pdf-invoice-combiner.git

# 6. 重命名主分支
git branch -M main

# 7. 推送到 GitHub
git push -u origin main

# 8. 创建第一个版本标签
git tag -a v1.0.0 -m "Release v1.0.0 - Initial release"
git push origin v1.0.0
```

## ✅ 上传后验证

1. 访问 `https://github.com/TAnsz/pdf-invoice-combiner`
2. 验证所有文件已上传
3. 检查 README.md 渲染正确
4. 确认 Releases 页面显示 v1.0.0
5. 查看 GitHub Actions 是否运行（如果已配置）

## 🎉 发布完成

一旦上传成功，你可以：

- [ ] 在项目描述中添加仓库链接
- [ ] 在 GitHub 个人资料中展示项目
- [ ] 分享项目链接给朋友和同事
- [ ] 在社区分享项目（如 Reddit、Twitter、etc.）

## 📞 常见问题

### Q: 推送时出现认证错误？

A: 使用 GitHub Personal Access Token：
1. GitHub Settings → Developer settings → Personal access tokens
2. 生成新 token（勾选 repo 权限）
3. 使用 token 作为密码推送

### Q: 如何更新已上传的代码？

A:
```bash
# 修改文件后
git add .
git commit -m "描述你的更改"
git push origin main
```

### Q: 如何撤销已推送的提交？

A: **谨慎操作**，使用：
```bash
git revert <commit-hash>
git push origin main
```

---

**准备好了吗？祝上传顺利！** 🚀
