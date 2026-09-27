/* 简易计算器移动版核心逻辑测试（Node 运行） */
"use strict";
const assert = require("assert");
const { evaluate, toggleSign } = require("./www/js/core.js");

let passed = 0;
function eq(actual, expected, name) {
  assert.strictEqual(actual, expected, name);
  passed++;
  console.log("ok -", name);
}
function throws(fn, name) {
  assert.throws(fn, name);
  passed++;
  console.log("ok -", name);
}

// 四则运算与优先级
eq(evaluate("1+2"), "3", "1+2=3");
eq(evaluate("10-4"), "6", "10-4=6");
eq(evaluate("6*7"), "42", "6*7=42");
eq(evaluate("9/4"), "2.25", "9/4=2.25");
eq(evaluate("2+3*4"), "14", "2+3*4=14（优先级）");
eq(evaluate("10-6/2"), "7", "10-6/2=7（优先级）");
// 界面按钮使用 Unicode 减号 −（U+2212），求值器必须正确归一化（历史 bug）
eq(evaluate("5−3"), "2", "5−3=2（U+2212 减号按钮）");
eq(evaluate("10−4−3"), "3", "连续 U+2212 减法");
eq(evaluate("7−(−2)"), "9", "7−(−2)=9（U+2212 与括号）");
eq(evaluate("2+5−1"), "6", "加减混合 U+2212");
// 括号
eq(evaluate("(2+3)*4"), "20", "(2+3)*4=20");
eq(evaluate("((1+2)*(3+4))"), "21", "嵌套括号=21");
// 小数
eq(evaluate("0.1+0.2"), "0.3", "0.1+0.2=0.3");
eq(evaluate("5/2"), "2.5", "5/2=2.5");
// 一元负号
eq(evaluate("-5+3"), "-2", "-5+3=-2");
eq(evaluate("(-5)*(-2)"), "10", "(-5)*(-2)=10");
eq(evaluate(".5+.5"), "1", ".5+.5=1");
// 百分比
eq(evaluate("200*10%"), "20", "200*10%=20（百分比）");
// 一元正负号连续
eq(evaluate("1++2"), "3", "1++2=3");
eq(evaluate("1+-2"), "-1", "1+-2=-1");
// 空白
eq(evaluate("  2 + 3 "), "5", "含空白=5");
eq(evaluate(""), "0", "空表达式=0");

// 异常
throws(() => evaluate("1/0"), "除数为0报错");
throws(() => evaluate("1+*2"), "非法运算符报错");
throws(() => evaluate("2*(3+4"), "括号不匹配报错");
throws(() => evaluate("abc"), "非法字符报错");
throws(() => evaluate("1.2.3"), "多小数点报错");
throws(() => evaluate("9".repeat(400) + "*9"), "溢出报错");

// 正负号切换
eq(toggleSign(""), "-", "空->-");
eq(toggleSign("-"), "", "- -> 空");
eq(toggleSign("5"), "(-5)", "5->(-5)");
eq(toggleSign("1+2"), "1+(-2)", "1+2->1+(-2)");
eq(toggleSign("(-5)"), "5", "(-5)->5");
eq(toggleSign("1+(-2)"), "1+2", "1+(-2)->1+2");
eq(toggleSign("3.14"), "(-3.14)", "3.14->(-3.14)");
eq(toggleSign("1+"), "1+-", "1+ -> 1+-");

console.log("\n全部通过:", passed, "个用例");
