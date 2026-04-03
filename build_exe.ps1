# PowerShell 构建脚本
# 使用 PyInstaller 将 Python 脚本打包为独立的 Windows EXE 文件
#
# 使用方法：
#   1. 安装 PyInstaller: pip install pyinstaller
#   2. 在 PowerShell 中运行: .\build_exe.ps1
#
# 生成的 EXE 将在 dist\ 目录中

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptName = "combine_pdfs_two_per_a4.py"
$scriptPath = Join-Path $scriptDir $scriptName

if (-not (Test-Path $scriptPath)) {
    Write-Host "❌ 错误：找不到 $scriptName" -ForegroundColor Red
    exit 1
}

Write-Host "🧹 清理旧文件..." -ForegroundColor Yellow
$distDir = Join-Path $scriptDir "dist"
$buildDir = Join-Path $scriptDir "build"
$specFile = Join-Path $scriptDir "$($scriptName.Replace('.py', '.spec'))"

Remove-Item -LiteralPath $distDir -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $buildDir -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $specFile -Force -ErrorAction SilentlyContinue

Write-Host "📦 构建 EXE 文件..." -ForegroundColor Yellow

# 检查 PyInstaller 是否安装
$pyinstaller = python -m pip list | Select-String "pyinstaller"
if (-not $pyinstaller) {
    Write-Host "⚠️  PyInstaller 未安装，正在安装..." -ForegroundColor Yellow
    python -m pip install pyinstaller --quiet
}

# 构建 EXE
python -m pyinstaller `
    --onefile `
    --name combine_pdfs `
    --icon NONE `
    --collect-all fitz `
    $scriptPath

if ($LASTEXITCODE -eq 0) {
    $exePath = Join-Path $distDir "combine_pdfs.exe"
    if (Test-Path $exePath) {
        Write-Host "`n✅ 成功！EXE 文件已生成: $exePath" -ForegroundColor Green
        Write-Host "`n💡 使用方法:" -ForegroundColor Cyan
        Write-Host "   combine_pdfs.exe" -ForegroundColor White
        Write-Host "   combine_pdfs.exe D:\invoices" -ForegroundColor White
        Write-Host "   combine_pdfs.exe D:\invoices D:\output\merged.pdf" -ForegroundColor White
    } else {
        Write-Host "❌ 错误：未找到生成的 EXE 文件" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "`n❌ 构建失败，返回码: $LASTEXITCODE" -ForegroundColor Red
    exit 1
}
