/* 简易计算器 - 界面交互（依赖 core.js 的 CalcCore） */
"use strict";

const state = {
  expression: "",
  justEvaluated: false,
  errorShown: false,
};

const displayEl = document.getElementById("display");

function updateDisplay() {
  let text = state.expression ? state.expression : "0";
  text = text.replace(/\*/g, "×").replace(/\//g, "÷");
  displayEl.textContent = text;
  displayEl.classList.remove("error");
  // 依据长度自适应字号
  const len = text.length;
  let size = 52;
  if (len > 12) size = 40;
  if (len > 18) size = 30;
  if (len > 26) size = 22;
  displayEl.style.fontSize = size + "px";
}

function showError(message) {
  state.expression = "";
  state.errorShown = true;
  state.justEvaluated = false;
  displayEl.textContent = message;
  displayEl.classList.add("error");
}

function pressKey(key) {
  // 归一化界面符号：减号按钮使用 Unicode −（U+2212），乘除为 × ÷
  key = key.replace("−", "-").replace("×", "*").replace("÷", "/");
  if (state.errorShown) {
    state.expression = "";
    state.errorShown = false;
  }
  if (state.justEvaluated) {
    if (/[0-9.%]/.test(key)) state.expression = "";
    state.justEvaluated = false;
  }

  if ("+-*/".includes(key)) {
    if (state.expression.endsWith("(")) {
      if (key !== "-") return;
    } else if (state.expression && "+-*/".includes(state.expression.slice(-1))) {
      state.expression = state.expression.slice(0, -1);
    } else if (!state.expression) {
      if (key === "-") state.expression = "-";
      else return;
    }
  } else if (key === ".") {
    const segment = state.expression.split(/[+\-*/()]/).pop();
    if (segment.includes(".")) return;
    if (segment === "") state.expression += "0";
  } else if (key === "0" && state.expression === "") {
    state.expression = "0";
  }

  if (state.expression.length < 60) state.expression += key;
  updateDisplay();
}

function calculate() {
  if (!state.expression || state.errorShown) return;
  try {
    const result = CalcCore.evaluate(state.expression);
    state.expression = result;
    state.justEvaluated = true;
    updateDisplay();
  } catch (e) {
    if (e.message.includes("除数")) showError("错误：除数不能为0");
    else if (e.message.includes("溢出")) showError("错误：数值溢出");
    else showError("错误：表达式有误");
  }
}

function clearAll() {
  state.expression = "";
  state.justEvaluated = false;
  state.errorShown = false;
  updateDisplay();
}

function backspace() {
  if (state.errorShown) { clearAll(); return; }
  state.expression = state.expression.slice(0, -1);
  state.justEvaluated = false;
  updateDisplay();
}

function toggleSignKey() {
  if (state.errorShown) return;
  state.expression = CalcCore.toggleSign(state.expression);
  state.justEvaluated = false;
  updateDisplay();
}

// 按键绑定
document.querySelectorAll(".key").forEach((btn) => {
  btn.addEventListener("click", () => {
    const k = btn.dataset.key;
    if (k === "C") clearAll();
    else if (k === "BS") backspace();
    else if (k === "PM") toggleSignKey();
    else if (k === "=") calculate();
    else pressKey(k);
  });
});

// 键盘支持（外接键盘时可用）
document.addEventListener("keydown", (e) => {
  const k = e.key;
  if (/^[0-9.+\-*/%]$/.test(k)) { e.preventDefault(); pressKey(k); }
  else if (k === "Enter" || k === "=") { e.preventDefault(); calculate(); }
  else if (k === "Backspace") { e.preventDefault(); backspace(); }
  else if (k === "Escape") { e.preventDefault(); clearAll(); }
});

// 阻止 WebView 中双击缩放
document.addEventListener("dblclick", (e) => e.preventDefault());

updateDisplay();
