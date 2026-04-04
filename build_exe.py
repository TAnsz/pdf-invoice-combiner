# -*- coding: utf-8 -*-
# 构建 EXE 脚本
# 使用 PyInstaller 将 Python 脚本打包为独立的 Windows EXE 文件
# 
# 使用方法：
#   1. 安装 PyInstaller: pip install pyinstaller
#   2. 运行此脚本: python build_exe.py
#   或在 PowerShell 中: python .\build_exe.py
#
# 生成的 EXE 将在 dist\ 目录中

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Fix encoding for GitHub Actions Windows environment
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def main():
    script_dir = Path(__file__).parent
    script_name = "combine_pdfs_two_per_a4.py"
    script_path = script_dir / script_name
    
    if not script_path.exists():
        print(f"[Error] Script not found: {script_name}")
        sys.exit(1)
    
    # 清理旧的构建文件
    dist_dir = script_dir / "dist"
    build_dir = script_dir / "build"
    spec_file = script_dir / f"{script_name.replace('.py', '.spec')}"
    
    print("[*] Cleaning old files...")
    for path in [dist_dir, build_dir, spec_file]:
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
    
    print("[*] Building EXE file...")
    cmd = [
        sys.executable, "-m", "pyinstaller",
        "--onefile",  # 单个 EXE 文件
        "--name", "combine_pdfs",  # EXE 名称
        "--icon", "NONE",  # 可选：添加图标
        "--add-data", f"{script_dir}{os.pathsep}.",  # 包含其他文件
        "--collect-all", "fitz",  # 收集 PyMuPDF 的所有依赖
        str(script_path)
    ]
    
    result = subprocess.run(cmd, cwd=script_dir)
    
    if result.returncode == 0:
        exe_path = dist_dir / "combine_pdfs.exe"
        if exe_path.exists():
            print(f"\n[OK] EXE file generated successfully: {exe_path}")
            print(f"\n[Info] Usage:")
            print(f"   combine_pdfs.exe")
            print(f"   combine_pdfs.exe D:\\invoices")
            print(f"   combine_pdfs.exe D:\\invoices D:\\output\\merged.pdf")
        else:
            print(f"[Error] EXE file not found")
            sys.exit(1)
    else:
        print(f"[Error] Build failed with return code: {result.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    main()
