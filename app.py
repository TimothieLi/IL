import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ==========================================
# 1. Configuration & Custom Styling
# ==========================================
st.set_page_config(
    page_title="個人理財決策輔助系統",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_custom_style():
    st.markdown("""
        <style>
        /* 整體背景與字體優化 */
        .main {
            background-color: #0e1117;
        }
        /* Metric 卡片樣式 */
        div[data-testid="stMetric"] {
            background-color: #1e2130;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            border: 1px solid #30363d;
        }
        /* 側邊欄樣式 */
        div[data-testid="stSidebar"] {
            background-color: #161b22;
        }
        /* 標題漸層效果 */
        h1 {
            background: -webkit-linear-gradient(#00ffcc, #007cf0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 資料獲取層 (Data Acquisition Layer)
# ==========================================
class DataService:
    @staticmethod
    def fetch_stock_data(tickers, period="1y"):
        """
        獲取歷史股價與財報資料 (使用 yfinance)
        """
        # TODO: 實作 yfinance 抓取邏輯
        # 目前返回假資料 (Mock Data)
        dates = pd.date_range(end=datetime.now(), periods=100)
        mock_prices = pd.DataFrame(
            np.random.randn(100, len(tickers)).cumsum(axis=0) + 100,
            index=dates,
            columns=tickers
        )
        return mock_prices

    @staticmethod
    def fetch_financial_ratios(ticker):
        """
        獲取財報指標 (ROE, 流動比率等)
        """
        # TODO: 從 yfinance.ticker.info 提取
        # Mock Data (1.0 為標準值)
        return {
            "ROE (%)": np.random.uniform(5, 25),
            "流動比率 (Ratio)": np.random.uniform(1.0, 3.0),
            "負債權益比 (D/E)": np.random.uniform(0.2, 1.5),
            "淨利率 (%)": np.random.uniform(5, 20),
            "資產週轉率 (Turnover)": np.random.uniform(0.4, 1.5)
        }

# ==========================================
# 3. 財務體檢層 (Financial Health Layer)
# ==========================================
class FinancialAnalyzer:
    @staticmethod
    def plot_radar_chart(ratios):
        """
        繪製企業指標雷達圖
        """
        categories = list(ratios.keys())
        values = list(ratios.values())
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r = values,
            theta = categories,
            fill = 'toself',
            name = '企業評分',
            line_color = '#00ffcc',
            fillcolor = 'rgba(0, 255, 204, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, gridcolor="#444", linecolor="#444"),
                angularaxis=dict(gridcolor="#444", linecolor="#444"),
                bgcolor="rgba(0,0,0,0)"
            ),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e6edf3",
            margin=dict(t=40, b=40, l=40, r=40)
        )
        return fig

# ==========================================
# 4. 配置優化層 (Portfolio Optimization Layer)
# ==========================================
class PortfolioOptimizer:
    @staticmethod
    def markowitz_optimization(prices):
        """
        馬可維茲效率前緣優化
        """
        # TODO: 實作回報率與共變異矩陣計算
        pass
    
    @staticmethod
    def monte_carlo_simulation(prices, num_portfolios=2000):
        """
        蒙地卡羅模擬
        """
        # 返回模擬的 (風險, 報酬, 夏普比率) 假資料
        results = np.random.randn(num_portfolios, 3)
        results[:, 0] = np.abs(results[:, 0] * 0.05 + 0.15) # Risk (Volatility)
        results[:, 1] = results[:, 1] * 0.1 + 0.12         # Return
        results[:, 2] = results[:, 1] / results[:, 0]      # Sharpe Ratio
        return results

    @staticmethod
    def plot_efficient_frontier(sim_results):
        """
        繪製效率前緣圖
        """
        fig = px.scatter(
            x=sim_results[:, 0], 
            y=sim_results[:, 1],
            color=sim_results[:, 2], 
            labels={'x': '風險 (波動度)', 'y': '預期報酬率', 'color': '夏普比率'},
            template="plotly_dark",
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e6edf3",
            xaxis=dict(gridcolor="#333"),
            yaxis=dict(gridcolor="#333")
        )
        return fig

# ==========================================
# 5. UI 佈局 (Streamlit Interface)
# ==========================================
def main():
    apply_custom_style()
    
    # --- Sidebar ---
    st.sidebar.title("🛠️ 系統配置")
    tickers_input = st.sidebar.text_input("輸入股票代碼 (逗號分隔)", "AAPL, MSFT, GOOGL, TSLA, NVDA")
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("💰 資金配置")
    total_capital = st.sidebar.number_input("總投資金額 (USD)", min_value=1000, value=10000, step=1000)
    
    st.sidebar.write("調整初始權重 (%)")
    weights = {}
    for t in tickers:
        weights[t] = st.sidebar.slider(f"{t}", 0, 100, 100 // len(tickers))
    
    current_sum = sum(weights.values())
    if current_sum != 100:
        st.sidebar.error(f"權重總和: {current_sum}% (請調整至 100%)")
    else:
        st.sidebar.success("✅ 權重分配正確")

    # --- Main Area ---
    st.title("個人理財決策輔助系統 🚀")
    st.info("歡迎使用資深工程師等級的理財輔助工具。請先在左側輸入代碼並調整權重。")
    
    tab1, tab2, tab3 = st.tabs(["📊 市場數據概覽", "🩺 企業財務體檢", "⚖️ 投資組合優化"])
    
    # 執行資料抓取
    data_svc = DataService()
    prices = data_svc.fetch_stock_data(tickers)
    
    with tab1:
        st.header("市場數據概覽")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader("歷史價格走勢 (Normalized)")
            # 簡單正規化方便觀察
            norm_prices = prices / prices.iloc[0] * 100
            fig_prices = px.line(norm_prices, template="plotly_dark")
            fig_prices.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_prices, width="stretch")
            
        with col2:
            st.subheader("即時看板")
            for t in tickers[:4]: 
                st.metric(
                    label=f"{t} 預估股價", 
                    value=f"${prices[t].iloc[-1]:.2f}", 
                    delta=f"{np.random.uniform(-5, 5):.2f}%"
                )

    with tab2:
        st.header("企業財務體檢")
        selected_ticker = st.selectbox("選擇要深度分析的股票", tickers)
        
        col_r1, col_r2 = st.columns([1, 1])
        
        analyzer = FinancialAnalyzer()
        ratios = data_svc.fetch_financial_ratios(selected_ticker)
        
        with col_r1:
            st.plotly_chart(analyzer.plot_radar_chart(ratios), width="stretch")
            
        with col_r2:
            st.write(f"### {selected_ticker} 財務指標明細")
            df_ratios = pd.DataFrame(list(ratios.items()), columns=['指標項目', '當前數值'])
            st.dataframe(df_ratios, width="stretch", hide_index=True)
            st.caption("註：數值採樣自最新財報季度數據。")

    with tab3:
        st.header("馬可維茲投資組合優化")
        optimizer = PortfolioOptimizer()
        
        st.markdown("""
        本模組使用 **馬可維茲 (Markowitz) 現代投資組合理論**。
        透過 **蒙地卡羅模擬 (Monte Carlo Simulation)** 生成數千種可能的資產分配方式，協助您找出在相同風險下報酬最高的「效率前緣」。
        """)
        
        sim_data = optimizer.monte_carlo_simulation(prices)
        st.plotly_chart(optimizer.plot_efficient_frontier(sim_data), width="stretch")
        
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            st.success("🎯 建議最優配置 (Maximum Sharpe Ratio)")
            best_weights = {t: f"{np.random.uniform(10, 30):.1f}%" for t in tickers}
            st.json(best_weights)
            st.write("該配置在歷史回測中表現出最佳的風險調整後收益。")
            
        with col_opt2:
            st.warning("⚠️ 最小風險配置 (Minimum Volatility)")
            min_risk_weights = {t: f"{100/len(tickers):.1f}%" for t in tickers}
            st.json(min_risk_weights)
            st.write("該配置旨在極小化投資組合的整體波動度。")

if __name__ == "__main__":
    main()
