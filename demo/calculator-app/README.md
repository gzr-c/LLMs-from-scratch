# 简易计算器 · 安卓移动版（Cordova）

桌面版（tkinter）的同款计算器移植为安卓 APK。核心求值逻辑为纯 JavaScript（`www/js/core.js`），
使用递归下降解析器，**不使用 `eval`**，安全无注入风险。界面为触屏优化的单页 Web 应用，
通过 Apache Cordova 打包为安卓安装包。

## 项目结构

```
calculator-app/
├── config.xml          # Cordova 配置（应用名/包名/竖屏/图标）
├── test_core.js        # 核心逻辑单元测试（Node 运行，36 个用例）
├── www/                # 移动端网页（即 APK 内运行的界面）
│   ├── index.html      # 页面结构
│   ├── css/style.css   # 触屏样式
│   └── js/
│       ├── core.js     # 求值核心（Parser / evaluate / toggleSign）
│       └── app.js      # 界面交互（按键绑定 / 状态机）
└── README.md           # 本说明
```

## 功能

- 四则运算（乘除优先）、括号、百分比（`200×10%` = 20）
- 正负号切换（±）、退格（⌫）、清空（C）
- 触屏大按钮 + 外接键盘支持
- 错误提示：除数为 0、格式错误、数值溢出
- Unicode 符号归一化：界面减号 `−`（U+2212）、`×`、`÷` 在求值前统一转为 ASCII（v1.1 修复）

## 环境要求（构建 APK 需要）

- Node.js 16+（运行测试）
- JDK 17（构建用）
- Android SDK（platform 35/36、build-tools 36）+ Gradle 8.14
- Cordova 12+（`npm install -g cordova`）

## 运行测试

```bash
node test_core.js
```

覆盖四则运算、优先级、括号、小数、百分比、除零、格式错误、溢出、正负号切换及 U+2212 减号归一化。

## 构建 APK

```bash
# 1. 同步网页到安卓平台资源
cordova prepare android
# 2. 构建 debug 包（产物在 platforms/android/app/build/outputs/apk/debug/）
cd platforms/android
gradle assembleDebug
```

> 提示：Windows 下若项目路径含非 ASCII 字符（如中文用户名），需在
> `platforms/android/gradle.properties` 中保留 `android.overridePathCheck=true`。

## 网页预览

`www/index.html` 可直接用浏览器打开调试，无需安装任何依赖。

## 许可

本 demo 仅供学习交流使用，代码基于 MIT 协议开源。
