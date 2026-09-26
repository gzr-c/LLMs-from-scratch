@echo off
REM ============================================================
REM  简易计算器打包脚本（生成 Windows 单文件 exe）
REM  前置条件：pip install pyinstaller
REM  产物位置：dist\Calculator.exe
REM ============================================================
cd /d "%~dp0"

echo [1/2] 开始打包，请稍候...
pyinstaller --onefile --windowed --name Calculator calculator.py

if errorlevel 1 (
    echo [错误] 打包失败，请先确认已执行: pip install pyinstaller
    pause
    exit /b 1
)

echo.
echo [2/2] 打包完成！可执行文件位于: dist\Calculator.exe
pause
