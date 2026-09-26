# -*- coding: utf-8 -*-
"""
简易计算器单元测试
==================
覆盖表达式求值（evaluate）与正负号切换（toggle_sign）两个纯函数。

运行方式（在 demo 目录下）：
    python -m unittest test_calculator -v
或：
    python test_calculator.py
"""

import unittest

from calculator import evaluate, toggle_sign


class TestEvaluate(unittest.TestCase):
    """表达式求值测试。"""

    def test_basic_addition(self):
        self.assertEqual(evaluate("1+2"), "3")

    def test_basic_subtraction(self):
        self.assertEqual(evaluate("10-4"), "6")

    def test_basic_multiplication(self):
        self.assertEqual(evaluate("6*7"), "42")

    def test_basic_division(self):
        self.assertEqual(evaluate("9/4"), "2.25")

    def test_precedence(self):
        """乘除优先于加减。"""
        self.assertEqual(evaluate("2+3*4"), "14")
        self.assertEqual(evaluate("10-6/2"), "7")

    def test_parentheses(self):
        self.assertEqual(evaluate("(2+3)*4"), "20")

    def test_nested_parentheses(self):
        self.assertEqual(evaluate("((1+2)*(3+4))"), "21")

    def test_float_result(self):
        self.assertEqual(evaluate("0.1+0.2"), "0.3")
        self.assertEqual(evaluate("5/2"), "2.5")

    def test_unary_minus(self):
        self.assertEqual(evaluate("-5+3"), "-2")
        self.assertEqual(evaluate("(-5)*(-2)"), "10")

    def test_decimal_input(self):
        self.assertEqual(evaluate(".5+.5"), "1")
        self.assertEqual(evaluate("1."), "1")

    def test_percent(self):
        """百分比：200*10% 等价于 200*0.1。"""
        self.assertEqual(evaluate("200*10%"), "20")

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            evaluate("1/0")

    def test_consecutive_operators_after_number(self):
        """一元正负号是合法的，如 1++2 等价于 1+(+2)。"""
        self.assertEqual(evaluate("1++2"), "3")
        self.assertEqual(evaluate("1+-2"), "-1")

    def test_invalid_expression(self):
        with self.assertRaises(ValueError):
            evaluate("1+*2")
        with self.assertRaises(ValueError):
            evaluate("2*(3+4")
        with self.assertRaises(ValueError):
            evaluate("abc")
        with self.assertRaises(ValueError):
            evaluate("1.2.3")

    def test_empty_expression(self):
        self.assertEqual(evaluate(""), "0")

    def test_whitespace(self):
        self.assertEqual(evaluate("  2 + 3 "), "5")

    def test_large_number_overflow(self):
        """超出 float 范围时报溢出。"""
        with self.assertRaises(OverflowError):
            evaluate("9" * 400 + "*9")


class TestToggleSign(unittest.TestCase):
    """正负号切换测试。"""

    def test_empty(self):
        self.assertEqual(toggle_sign(""), "-")

    def test_single_dash(self):
        self.assertEqual(toggle_sign("-"), "")

    def test_positive_to_negative(self):
        self.assertEqual(toggle_sign("5"), "(-5)")
        self.assertEqual(toggle_sign("1+2"), "1+(-2)")

    def test_negative_to_positive(self):
        self.assertEqual(toggle_sign("(-5)"), "5")
        self.assertEqual(toggle_sign("1+(-2)"), "1+2")

    def test_decimal(self):
        self.assertEqual(toggle_sign("3.14"), "(-3.14)")
        self.assertEqual(toggle_sign("(-3.14)"), "3.14")

    def test_after_operator(self):
        self.assertEqual(toggle_sign("1+"), "1+-")


if __name__ == "__main__":
    unittest.main()
