# 個人理財決策輔助系統 (Personal Financial Decision Support System) 📈

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)

這是一個基於 **Streamlit** 開發的專業級個人理財決策輔助工具。系統採用「自頂向下 (Top-Down)」的架構設計，整合了資料獲取、財務指標分析以及投資組合優化（馬可維茲模型）等核心功能。

## 🌟 核心功能

*   **📊 市場數據概覽**：即時視覺化多檔股票的歷史走勢，並提供關鍵價格指標。
*   **🩺 企業財務體檢**：利用雷達圖 (Radar Chart) 多維度分析企業獲利能力、償債能力與經營效率（如 ROE、流動比率等）。
*   **⚖️ 投資組合優化**：基於**現代投資組合理論 (MPT)**，透過蒙地卡羅模擬找出效率前緣，提供最優夏普比率配置建議。
*   **💎 現代化 UI/UX**：美觀的深色模式設計，具備互動式圖表與響應式佈局。

## 🏗️ 技術架構

系統分為以下四個層級：
1.  **UI 介面層**：使用 Streamlit 構建前端。
2.  **資料獲取層**：整合 `yfinance` 獲取全球市場數據。
3.  **財務分析層**：計算關鍵財務比率與生成統計圖表。
4.  **優化運算層**：執行馬可維茲模型與風險模擬。

## 🚀 快速開始

### 環境需求
*   Python 3.9+
*   pip

### 安裝步驟

1.  **複製專案**：
    ```bash
    git clone https://github.com/TimothieLi/IL.git
    cd IL
    ```

2.  **安裝依賴套件**：
    ```bash
    pip install -r requirements.txt
    ```

3.  **啟動系統**：
    ```bash
    streamlit run app.py
    ```

## 🛠️ 開發藍圖 (Roadmap)

- [x] 系統基礎骨架與 UI 佈局
- [x] 財務指標雷達圖實作
- [x] 蒙地卡羅模擬與效率前緣視覺化
- [ ] 整合真實 `yfinance` 資料 API
- [ ] 加入 AI 投資建議助手 (LLM Integration)
- [ ] 支援 CSV/PDF 報表匯出

## 📄 授權協議

本專案採用 MIT 授權協議。

---
*Developed with ❤️ by Timothy Li*
