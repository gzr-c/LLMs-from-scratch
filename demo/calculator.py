# -*- coding: utf-8 -*-
"""
简易计算器（Windows 桌面小工具）
=================================
基于 Python 标准库 tkinter 编写，无需安装任何第三方依赖。

功能：
    - 四则运算（+ - * /）与括号
    - 百分比（%）
    - 正负号切换（±）
    - 退格（⌫）、清空（C）
    - 支持键盘输入（数字 / 运算符 / Enter 计算 / BackSpace 退格 / Esc 清空）
    - 错误提示（除数为 0、表达式格式错误、数值溢出）

运行方式：
    python calculator.py

作者：gzr-c
"""

import math
import re
import tkinter as tk
from tkinter import font as tkfont

# ---------------------------------------------------------------------------
# 表达式求值核心（纯函数，便于单元测试，不使用 eval，安全）
# ---------------------------------------------------------------------------

def evaluate(expression: str) -> str:
    """对简单算术表达式求值，返回结果字符串。

    支持 + - * / 和括号，以及百分比（例如 200*10% 等价于 200*0.1）。
    除数为 0 时抛出 ZeroDivisionError，格式错误抛出 ValueError，
    数值溢出（超出 float 范围）抛出 OverflowError。
    """
    expr = expression.strip()
    if not expr:
        return "0"

    # 统一运算符符号（GUI 按钮显示 × ÷，内部存储 * /）
    expr = expr.replace("×", "*").replace("÷", "/")

    # 百分比：把数字后的 % 转为 /100，例如 10% -> (10/100)
    expr = re.sub(r"(\d+(?:\.\d+)?)%", r"(\1/100)", expr)

    # 白名单校验：只允许数字、运算符、括号、小数点和空白
    if not re.fullmatch(r"[0-9+\-*/().\s]*", expr):
        raise ValueError("表达式包含不支持的字符")

    value = _Parser(expr).parse()
    if not math.isfinite(value):
        raise OverflowError("数值溢出")
    return _format_result(value)


def toggle_sign(expression: str) -> str:
    """切换表达式中最后一个数字的正负号（对应 GUI 的 ± 按钮）。"""
    if expression == "":
        return "-"
    if expression == "-":
        return ""
    # 情况一：末尾数字已被取负，形如 "1+(-2)"，还原为正
    m2 = re.search(r"\(-(\d+(?:\.\d+)?)\)\s*$", expression)
    if m2:
        return expression[: m2.start()] + m2.group(1)
    # 情况二：末尾是普通数字，形如 "1+2"，取负为 "1+(-2)"
    m = re.search(r"(\d+(?:\.\d+)?)\s*$", expression)
    if m:
        return expression[: m.start(1)] + "(-" + m.group(1) + ")"
    # 情况三：末尾是运算符或括号，直接追加负号
    return expression + "-"


def _format_result(value: float) -> str:
    """把计算结果格式化为用户可读的字符串（去掉多余的 .0 和末尾 0）。"""
    if value == int(value):
        return str(int(value))
    text = f"{value:.10f}".rstrip("0").rstrip(".")
    return text


class _Parser:
    """递归下降解析器：expr := term (('+'|'-') term)*；term := factor (('*'|'/') factor)*"""

    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def parse(self) -> float:
        value = self.parse_expr()
        if not self.at_end():
            raise ValueError("表达式格式错误")
        return value

    def parse_expr(self) -> float:
        value = self.parse_term()
        while True:
            ch = self.peek()
            if ch == "+":
                self.pos += 1
                value += self.parse_term()
            elif ch == "-":
                self.pos += 1
                value -= self.parse_term()
            else:
                return value

    def parse_term(self) -> float:
        value = self.parse_factor()
        while True:
            ch = self.peek()
            if ch == "*":
                self.pos += 1
                value *= self.parse_factor()
            elif ch == "/":
                self.pos += 1
                value /= self.parse_factor()  # 除数为 0 时抛出 ZeroDivisionError
            else:
                return value

    def parse_factor(self) -> float:
        ch = self.peek()
        if ch == "(":
            self.pos += 1
            value = self.parse_expr()
            if self.peek() != ")":
                raise ValueError("括号不匹配")
            self.pos += 1
            return value
        if ch == "+":
            self.pos += 1
            return self.parse_factor()
        if ch == "-":
            self.pos += 1
            return -self.parse_factor()
        return self.parse_number()

    def parse_number(self) -> float:
        start = self.pos
        while self.pos < len(self.text) and (self.text[self.pos].isdigit()
                                             or self.text[self.pos] == "."):
            self.pos += 1
        token = self.text[start:self.pos]
        if token in ("", ".") or token.count(".") > 1:
            raise ValueError("数字格式错误")
        return float(token)

    def peek(self) -> str:
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1
        return self.text[self.pos] if self.pos < len(self.text) else ""

    def at_end(self) -> bool:
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1
        return self.pos >= len(self.text)


# ---------------------------------------------------------------------------
# 图形界面
# ---------------------------------------------------------------------------

class CalculatorApp:
    """tkinter 简易计算器界面。"""

    # 显示用符号映射（内部用 * /，界面显示 × ÷）
    DISPLAY_MAP = str.maketrans({"*": "×", "/": "÷"})

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("简易计算器")
        self.root.resizable(False, False)

        self.expression = ""        # 当前表达式（内部表示）
        self.just_evaluated = False # 刚计算完，再输入数字时重新开始
        self.error_shown = False    # 正在显示错误信息

        self._build_ui()
        self._center_window(320, 420)
        # 键盘事件绑定到根窗口
        self.root.bind("<Key>", self._on_key)

    # ---------------------------- 界面构建 ----------------------------
    def _build_ui(self) -> None:
        btn_font = tkfont.Font(family="Microsoft YaHei UI", size=13, weight="bold")
        display_font = tkfont.Font(family="Segoe UI", size=20)

        self.display_var = tk.StringVar(value="0")

        # 显示屏
        self.display = tk.Entry(
            self.root, textvariable=self.display_var, font=display_font,
            justify="right", state="readonly", readonlybackground="#fafafa",
            fg="#222222", bd=0, highlightthickness=1, highlightbackground="#dddddd",
            insertbackground="#222222",
        )
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew",
                          padx=10, pady=(12, 8), ipady=10)

        # 按钮定义：(文本, 样式类型)
        # 样式类型: digit=数字, op=运算符, func=功能键, equal=等号
        buttons = [
            ("C",  "func"),  ("⌫", "func"), ("±", "func"), ("÷", "op"),
            ("7",  "digit"), ("8", "digit"), ("9", "digit"), ("×", "op"),
            ("4",  "digit"), ("5", "digit"), ("6", "digit"), ("−", "op"),
            ("1",  "digit"), ("2", "digit"), ("3", "digit"), ("+", "op"),
            ("0",  "digit"), (".", "digit"), ("=", "equal"),
        ]

        colors = {
            "digit": ("#f5f5f5", "#333333"),
            "op":    ("#dbeafe", "#1d4ed8"),
            "func":  ("#ffe8cc", "#b45309"),
            "equal": ("#4caf50", "#ffffff"),
        }

        row = 1
        col = 0
        for text, kind in buttons:
            bg, fg = colors[kind]
            cmd = self._make_command(text)
            btn = tk.Button(
                self.root, text=text, font=btn_font, bg=bg, fg=fg,
                activebackground=bg, activeforeground=fg, bd=0,
                highlightthickness=1, highlightbackground="#e0e0e0",
                cursor="hand2", command=cmd,
            )
            if text == "0":
                btn.grid(row=row, column=0, columnspan=2, sticky="nsew",
                         padx=2, pady=2, ipady=6)
                col = 2
            elif text == ".":
                btn.grid(row=row, column=2, sticky="nsew", padx=2, pady=2, ipady=6)
                col = 3
            elif text == "=":
                btn.grid(row=row, column=3, sticky="nsew", padx=2, pady=2, ipady=6)
                row += 1
                col = 0
            else:
                btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2, ipady=6)
                col += 1
                if col == 4:
                    row += 1
                    col = 0

        # 让各行列等宽等高
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1, uniform="btn")
        for i in range(1, 6):
            self.root.grid_rowconfigure(i, weight=1, uniform="btn")

    def _make_command(self, text: str):
        """根据按钮文本返回对应的回调函数。"""
        if text == "C":
            return self.clear
        if text == "⌫":
            return self.backspace
        if text == "±":
            return self.toggle_sign
        if text == "=":
            return self.calculate
        if text in ("+", "−", "×", "÷"):
            op = {"+": "+", "−": "-", "×": "*", "÷": "/"}[text]
            return lambda: self.press_key(op)
        return lambda: self.press_key(text)

    # ---------------------------- 核心交互 ----------------------------
    def press_key(self, key: str) -> None:
        """输入一个字符（数字 / 小数点 / 运算符 / 百分号）。"""
        if self.error_shown:
            self.expression = ""
            self.error_shown = False
        if self.just_evaluated:
            # 计算完成后：输入数字则重新开始，输入运算符则继续运算
            if key in "0123456789.%":
                self.expression = ""
            self.just_evaluated = False

        if key in "+-*/":
            if self.expression.endswith("("):
                if key != "-":
                    return
            elif self.expression and self.expression[-1] in "+-*/":
                self.expression = self.expression[:-1]  # 替换末尾运算符
            elif not self.expression:
                if key == "-":
                    self.expression = "-"
                else:
                    return
        elif key == ".":
            segment = re.split(r"[+\-*/()]", self.expression)[-1]
            if "." in segment:
                return
            if segment == "":
                self.expression += "0"
        elif key == "0" and self.expression == "":
            self.expression = "0"

        if len(self.expression) < 60:  # 限制长度，防止溢出
            self.expression += key
        self._update_display()

    def calculate(self) -> None:
        """按下 = 或回车：求值当前表达式。"""
        if not self.expression or self.error_shown:
            return
        try:
            result = evaluate(self.expression)
        except ZeroDivisionError:
            self._show_error("错误：除数不能为0")
            return
        except OverflowError:
            self._show_error("错误：数值溢出")
            return
        except ValueError:
            self._show_error("错误：表达式有误")
            return
        self.expression = result
        self.just_evaluated = True
        self._update_display()

    def clear(self) -> None:
        self.expression = ""
        self.just_evaluated = False
        self.error_shown = False
        self._update_display()

    def backspace(self) -> None:
        if self.error_shown:
            self.clear()
            return
        self.expression = self.expression[:-1]
        self.just_evaluated = False
        self._update_display()

    def toggle_sign(self) -> None:
        if self.error_shown:
            return
        self.expression = toggle_sign(self.expression)
        self.just_evaluated = False
        self._update_display()

    # ---------------------------- 辅助方法 ----------------------------
    def _update_display(self) -> None:
        text = self.expression.translate(self.DISPLAY_MAP) if self.expression else "0"
        self.display_var.set(text)
        self.display.config(fg="#222222")

    def _show_error(self, message: str) -> None:
        self.expression = ""
        self.error_shown = True
        self.just_evaluated = False
        self.display_var.set(message)
        self.display.config(fg="#d32f2f")

    def _on_key(self, event: tk.Event) -> None:
        """键盘输入支持。"""
        if event.char and event.char in "0123456789.+-*/%":
            self.press_key(event.char)
        elif event.keysym in ("Return", "KP_Enter", "equal"):
            self.calculate()
        elif event.keysym == "BackSpace":
            self.backspace()
        elif event.keysym in ("Escape", "Delete"):
            self.clear()
        elif event.keysym in ("c", "C"):
            self.clear()

    def _center_window(self, width: int, height: int) -> None:
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 3
        self.root.geometry(f"{width}x{height}+{x}+{y}")


def main() -> None:
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
