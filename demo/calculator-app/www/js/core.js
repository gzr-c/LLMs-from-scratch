/* 简易计算器 - 核心逻辑（无 DOM 依赖，浏览器/Node 通用）
 * 从 Python 版 calculator.py 移植，不使用 eval，安全。
 */
(function (global) {
  "use strict";

  class Parser {
    constructor(text) {
      this.text = text;
      this.pos = 0;
    }

    parse() {
      const value = this.parseExpr();
      if (!this.atEnd()) throw new Error("表达式格式错误");
      return value;
    }

    parseExpr() {
      let value = this.parseTerm();
      while (true) {
        const ch = this.peek();
        if (ch === "+") { this.pos++; value += this.parseTerm(); }
        else if (ch === "-") { this.pos++; value -= this.parseTerm(); }
        else return value;
      }
    }

    parseTerm() {
      let value = this.parseFactor();
      while (true) {
        const ch = this.peek();
        if (ch === "*") { this.pos++; value *= this.parseFactor(); }
        else if (ch === "/") {
          this.pos++;
          const rhs = this.parseFactor();
          if (rhs === 0) throw new Error("除数不能为0");
          value /= rhs;
        }
        else return value;
      }
    }

    parseFactor() {
      const ch = this.peek();
      if (ch === "(") {
        this.pos++;
        const value = this.parseExpr();
        if (this.peek() !== ")") throw new Error("括号不匹配");
        this.pos++;
        return value;
      }
      if (ch === "+") { this.pos++; return this.parseFactor(); }
      if (ch === "-") { this.pos++; return -this.parseFactor(); }
      return this.parseNumber();
    }

    parseNumber() {
      const start = this.pos;
      while (this.pos < this.text.length && /[0-9.]/.test(this.text[this.pos])) this.pos++;
      const token = this.text.slice(start, this.pos);
      if (token === "" || token === "." || token.split(".").length > 2) {
        throw new Error("数字格式错误");
      }
      return parseFloat(token);
    }

    peek() {
      while (this.pos < this.text.length && /\s/.test(this.text[this.pos])) this.pos++;
      return this.pos < this.text.length ? this.text[this.pos] : "";
    }

    atEnd() {
      while (this.pos < this.text.length && /\s/.test(this.text[this.pos])) this.pos++;
      return this.pos >= this.text.length;
    }
  }

  function formatResult(value) {
    if (Number.isInteger(value)) return String(value);
    return String(parseFloat(value.toFixed(10)));
  }

  function evaluate(expression) {
    let expr = expression.trim();
    if (!expr) return "0";

    expr = expr.replace(/×/g, "*").replace(/÷/g, "/").replace(/−/g, "-");
    // 百分比：10% -> (10/100)
    expr = expr.replace(/(\d+(?:\.\d+)?)%/g, "($1/100)");

    if (!/^[0-9+\-*/().\s]*$/.test(expr)) throw new Error("不支持的字符");

    const value = new Parser(expr).parse();
    if (!Number.isFinite(value)) throw new Error("数值溢出");
    return formatResult(value);
  }

  function toggleSign(expression) {
    if (expression === "") return "-";
    if (expression === "-") return "";
    const m2 = expression.match(/\(-(\d+(?:\.\d+)?)\)\s*$/);
    if (m2) return expression.slice(0, m2.index) + m2[1];
    const m = expression.match(/(\d+(?:\.\d+)?)\s*$/);
    if (m) return expression.slice(0, m.index) + "(-" + m[1] + ")";
    return expression + "-";
  }

  const api = { evaluate: evaluate, toggleSign: toggleSign };

  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  } else {
    global.CalcCore = api;
  }
})(typeof window !== "undefined" ? window : this);
