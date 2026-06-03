# 理財決策輔助系統 (Financial Decision Support System)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://hellotim.streamlit.app)

👉 **Live Demo 線上體驗**：[https://hellotim.streamlit.app](https://hellotim.streamlit.app)

> **專案定位**：本專案定位為個人理財決策輔助系統，核心目標是協助使用者理解自身財務狀況，並透過客觀的數據運算與量化模型，提供符合其風險承受度的投資組合建議。

這是一個基於 **Streamlit** 開發的專業級個人理財決策輔助工具。系統採用「漏斗式量化選股架構」，結合了離線市場資料庫、動態策略篩選器 (Screener) 以及現代投資組合理論 (MPT) 最佳化模型。

## 🌟 核心特色與功能

*   **🩺 財務健康體檢與雙頁面架構**：依據使用者的收支與資產負債狀況，精確運算出財務健康分數，並透過優雅的雙頁面切換機制，提供乾淨無干擾的輸入體驗。
*   **📡 即時全市場量化選股 (Screener)**：
    * 採用 on-demand 架構，當使用者點擊分析時即時透過 `yfinance` API 抓取最新市場價格，確保配置分析永遠採用最新數據。
    * 系統自動根據使用者的理財屬性，套用「動能策略」或「低波防禦策略」，從海選標的池中精煉出菁英標的。
*   **🧠 MPT 演算法優化**：
    * 採用 `scipy.optimize` 實作 SLSQP 演算法。
    * 具備「自動風險分散」約束機制（任何入選標的權重不低於 10%），尋找最小化波動度或最大化夏普值的最佳權重。
*   **📊 動態客觀解析**：系統會即時分析最高權重標的的歷史年化報酬與波動度，並產出完全基於客觀數據的配置理由說明。
*   **🛡️ 智慧表單防呆機制**：內建原生 JavaScript 事件攔截器，自動阻擋非預期的 Enter 送出動作，並具備智慧型格式修正與預設值還原功能。

## 🏗️ 系統架構

系統分為以下四個核心模組：
1.  **`app.py` (UI 控制層)**：基於 Streamlit 的前端介面與雙頁面流程邏輯，整合客製化 CSS/JS。
2.  **`modules/screener.py` (策略過濾層)**：負責從全市場資料庫中撈取符合策略條件的前 N 大標的。
3.  **`modules/optimizer.py` (量化運算層)**：包含 MPT 模型，負責共變異數矩陣運算與權重最佳化。
4.  **`scripts/update_market_data.py` (資料管線)**：即時資料爬蟲腳本，當使用者開始分析時，負責動態抓取 `yfinance` 最新市場行情並提供給系統運算。

## 🚀 快速開始

### 環境需求
*   Python 3.9+
*   pip

### 安裝依賴套件
```bash
pip install -r requirements.txt
```

### 啟動應用程式
```bash
streamlit run app.py
```
