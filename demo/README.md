# 简易计算器（Windows 桌面小工具）

一个基于 Python 标准库 **tkinter** 编写的 Windows 桌面计算器，零第三方依赖，即下即用。

## 功能特性

- 四则运算：加（+）、减（−）、乘（×）、除（÷），运算优先级正确（乘除优先于加减）
- 支持括号与百分比：`200×10%` = 20
- 正负号切换（±）、退格（⌫）、清空（C）
- 支持键盘操作：数字 / 运算符直接输入，`Enter` 计算，`BackSpace` 退格，`Esc` 清空
- 错误提示：除数为 0、表达式格式错误、数值溢出均有明确中文提示
- 安全求值：表达式由递归下降解析器计算，**不使用 `eval`**，杜绝注入风险

## 项目结构

```
demo/
├── calculator.py        # 计算器主程序（GUI + 表达式求值核心）
├── test_calculator.py   # 单元测试（求值与正负号逻辑）
├── build.bat            # 打包为 Windows exe 的脚本（可选）
└── README.md            # 本说明
```

## 环境要求

- Windows 7 / 10 / 11
- Python 3.8 及以上（**tkinter 为 Python 自带模块，无需安装任何第三方库**）

> 如何确认环境是否就绪：在命令行执行 `python --version` 和
> `python -c "import tkinter; print(tkinter.TkVersion)"`，能看到版本号即可。

## 运行方法

在 `demo` 目录下执行：

```bash
python calculator.py
```

窗口弹出即表示运行成功。若不想保留黑色控制台窗口，可改用：

```bash
pythonw calculator.py
```

## 操作说明

| 操作 | 方式 |
| --- | --- |
| 输入数字 / 运算符 | 点击按钮，或直接按键盘 |
| 计算 | 点击 `=` 或按 `Enter` |
| 退格 | 点击 `⌫` 或按 `BackSpace` |
| 清空 | 点击 `C` 或按 `Esc` / `Delete` |
| 正负号 | 点击 `±`（对当前最后一个数字取反） |
| 百分比 | 键盘输入 `%`，例如 `200×10%` |

小提示：计算完成后直接输入数字会开启新的计算；输入运算符则基于结果继续运算。

## 运行测试

```bash
python -m unittest test_calculator -v
```

共 23 个用例，覆盖四则运算、优先级、括号、小数、百分比、除零、格式错误、溢出和正负号切换。

## 打包为 Windows exe（可选）

1. 安装打包工具（仅这一步需要联网）：

   ```bash
   pip install pyinstaller
   ```

2. 双击运行 `build.bat`（或手动执行）：

   ```bash
   pyinstaller --onefile --windowed --name Calculator calculator.py
   ```

3. 打包完成后，在 `dist` 目录找到 **`Calculator.exe`**，可直接双击运行，
   也可以拷贝到任意 Windows 电脑使用（无需安装 Python）。

## 常见问题

- **双击 exe 报毒 / 被杀毒软件拦截**：PyInstaller 单文件打包程序首次运行较慢且容易被误报，
  属正常现象；可加白名单或改用 `python calculator.py` 运行。
- **界面文字乱码**：本程序已声明 UTF-8 编码；若仍异常，请确认系统区域设置中勾选
  “Beta: 使用 Unicode UTF-8 提供全球语言支持”。
- **tkinter 报错 `No module named 'tkinter'`**：说明当前 Python 安装时未勾选 Tcl/Tk，
  请重新安装 Python 并勾选 “tcl/tk and IDLE”。

## 许可

本 demo 仅供学习交流使用，代码基于 MIT 协议开源。
