import streamlit as st
import pandas as pd

from modules.analyzer import FinancialProfileAnalyzer
from modules.data_service import DataService
from modules.optimizer import PortfolioOptimizer
from modules.visualizer import plot_income_expense_pie, plot_allocation_pie, plot_historical_backtest

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
        /* 全局字體設定，Vercel 愛用系統無襯線字體 */
        html, body, [class*="css"]  {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            color: #ffffff;
        }
        /* 整體背景與字體優化 - 極簡純黑 */
        .main {
            background-color: #000000;
        }
        /* Metric 卡片樣式 - 極簡無背景，微圓角，細灰框 */
        div[data-testid="stMetric"] {
            background-color: transparent;
            padding: 16px;
            border-radius: 6px;
            border: 1px solid #333333;
            box-shadow: none;
        }
        /* 側邊欄樣式 */
        div[data-testid="stSidebar"] {
            background-color: #0a0a0a;
            border-right: 1px solid #333333;
        }
        /* 標題 - 取消漸層，改為純白 */
        h1 {
            color: #ffffff !important;
            font-weight: 700;
            background: none !important;
            -webkit-text-fill-color: initial !important;
        }
        h2, h3, h4, h5, h6 {
            color: #fafafa;
        }
        /* 隱藏預設的主題邊框與顏色，改為 1px Vercel 風格 */
        .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select {
            border: 1px solid #333333 !important;
            border-radius: 6px !important;
            background-color: #000000 !important;
            color: #ffffff !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. Main App
# ==========================================
def main():
    apply_custom_style()
    
    st.title("理財分析報告")
    st.write("這是一個基於資料驅動的個人理財與資產配置建議系統。請在下方輸入您的財務概況，系統將為您生成客製化的報告。")
    
    # 使用 session_state 來保存狀態，避免每次互動重新計算
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = None
        
    with st.form("financial_form"):
        st.markdown("### 基本財務資料")
        col1, col2, col3 = st.columns(3)
        with col1:
            income = st.number_input("每月固定收入 (稅後)", min_value=0, value=50000, step=1000)
            savings = st.number_input("目前可動用存款總額", min_value=0, value=150000, step=10000)
        with col2:
            fixed_expenses = st.number_input("每月固定支出 (房租/貸款/保險等)", min_value=0, value=20000, step=1000)
            debt = st.number_input("目前負債總額", min_value=0, value=50000, step=10000)
        with col3:
            variable_expenses = st.number_input("每月變動支出 (餐飲/娛樂/購物等)", min_value=0, value=15000, step=1000)
            investable = st.number_input("每月可投資金額", min_value=0, value=10000, step=1000)
            
        st.markdown("---")
        st.markdown("### 理財規劃")
        col4, col5 = st.columns(2)
        with col4:
            goal = st.selectbox("主要理財目標", ["建立緊急預備金", "長期資產成長", "買房準備", "退休規劃", "教育基金"])
        with col5:
            goal_years = st.selectbox("投資期限", ["1 年內", "3 年", "5 年", "10 年以上"], index=2)
            
        st.markdown("<br>", unsafe_allow_html=True)
        # 送出按鈕
        submitted = st.button("開始分析", use_container_width=True)

    # 點擊分析按鈕後切換到結果頁面
    if submitted:
        analyzer = FinancialProfileAnalyzer(
            income, fixed_expenses, variable_expenses, savings, debt, investable, goal_years
        )
        st.session_state.analyzer = analyzer
        
        with st.spinner("正在從全市場資料庫執行第一層量化選股，並進行最佳化演算法訓練..."):
            from modules.screener import MarketScreener
            screener = MarketScreener()
            
            # 根據用戶理財屬性決定選股策略
            if analyzer.profile_type in ["優先儲蓄型", "債務整理型", "消費控管型", "保守型", "穩健理財型", "穩健型"]:
                screen_strategy = "low_volatility"
            else:
                screen_strategy = "momentum"
                
            screen_top_n = 10
            
            try:
                selected_tickers, df = screener.screen(top_n=screen_top_n, strategy=screen_strategy)
                
                ds = DataService(df)
                exp_ret, cov = ds.process_data()
                st.session_state.data_df = ds.data
                
                optimizer = PortfolioOptimizer(exp_ret, cov)
                weights = optimizer.optimize(analyzer.profile_type)
            except Exception as e:
                st.error(f"資料處理錯誤: {e}")
                weights = {}
                
            # 每支最低不能低於 10%
            filtered_weights = {k: v for k, v in weights.items() if v >= 0.10}
            # 重新歸一化讓總和為 100%
            total_w = sum(filtered_weights.values())
            if total_w > 0:
                st.session_state.opt_weights = {k: v / total_w for k, v in filtered_weights.items()}
            else:
                st.session_state.opt_weights = {}
                
    # ==========================================
    # 呈現結果
    # ==========================================
    if st.session_state.analyzer:
        analyzer = st.session_state.analyzer
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["收支總覽", "理財建議"])
        
        with tab1:
            st.header("財務健康總覽")
            
            # 顯示 KPI 卡片
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric("健康分數", f"{analyzer.health_score} / 100", 
                        delta="良好" if analyzer.health_score >= 70 else "需注意",
                        delta_color="normal" if analyzer.health_score >= 70 else "inverse")
            kpi2.metric("每月結餘", f"${analyzer.monthly_balance:,}")
            kpi3.metric("儲蓄率", f"{analyzer.savings_rate * 100:.1f}%")
            kpi4.metric("緊急預備金", f"{analyzer.emergency_fund_months:.1f} 個月")
            
            st.markdown("---")
            st.write(f"**根據您目前的理財狀況：**")
            
            if analyzer.savings_rate < 0.2:
                st.write(f"- 儲蓄率偏低，建議尋找開源節流機會，將儲蓄率提升至 20% 以上。")
            else:
                st.write(f"- 儲蓄率表現良好，維持此紀律將有助於長期資產累積。")
                
            if analyzer.emergency_fund_months < 6:
                st.write(f"- 緊急預備金略顯不足，建議優先將存款拉高至可涵蓋 6 個月的生活開銷，以提升財務安全感。")
            else:
                st.write(f"- 目前的存款約可支撐 {analyzer.emergency_fund_months:.1f} 個月，緊急預備金十分充裕，已有足夠的安全網。")
                
            st.markdown("---")
            st.header("收支結構分析")
            
            fig1 = plot_income_expense_pie(analyzer)
            
            col_c1, col_c2 = st.columns([2, 1])
            with col_c1:
                st.plotly_chart(fig1, use_container_width=True)
                
            with col_c2:
                st.write("### 核心指標")
                st.write(f"- **支出率**: {analyzer.expense_rate * 100:.1f}%")
                st.write(f"- **儲蓄率**: {analyzer.savings_rate * 100:.1f}%")
                
                if analyzer.expense_rate > 0.8:
                    st.warning("數據顯示您的支出佔比已逾 80%，高於多數理財法建議的安全水位。就財務健康指標而言，需優先檢視變動支出項目，以尋求提升現金流的空間。")
                elif analyzer.expense_rate > 0.6:
                    st.info("數據顯示您的支出佔比為 60%-80% 區間。雖然仍在可控範圍，但根據主流理財指標，具備進一步優化收支結構與提升儲蓄率的潛力。")
                else:
                    st.success("數據顯示您的支出佔比控制在 60% 以下。符合主流財務健康指標建議的良好範圍，具備高度資金彈性與抗風險能力。")

        with tab2:
            st.header("理財策略")
            
            if analyzer.profile_type == "優先儲蓄型":
                strategy_text = "從前面的收支情況來看，您目前的**緊急預備金嚴重不足**。因此，理財策略應以「建立財務安全網」為出發點。現階段建議暫緩高風險投資，優先將資金存入銀行活存，直到存滿 3-6 個月的預備金為止。"
            elif analyzer.profile_type == "債務整理型":
                strategy_text = "從前面的收支情況來看，您的**負債比例過高**，每月可能被沉重的利息侵蝕。因此，理財策略應以「理債優先」為出發點。建議使用雪球還款法，集中火力先清償利率最高的債務（如信用卡循環、信貸）。"
            elif analyzer.profile_type == "消費控管型":
                strategy_text = "從前面的收支情況來看，您的**每月儲蓄率偏低**，難以累積本金。因此，理財策略應以「抓漏與節流」為出發點。建議嚴格實行記帳，找出隱形花費，先將儲蓄率拉高到 20% 以上，再來進行投資配置。"
            elif analyzer.profile_type == "穩健理財型":
                strategy_text = "從前面的收支情況來看，您的**財務體質健康且穩定**，有穩定的結餘與基本預備金。因此，理財策略可將重心轉向「對抗通膨與穩健增值」。建議可開始定期定額投入大盤型 ETF，並搭配部分債券降低投資組合波動。"
            elif analyzer.profile_type == "成長投資型":
                strategy_text = "從前面的收支情況來看，您的**資金充裕且安全網極為堅固**。因此，理財策略可將重心轉向「資本大幅成長」。在您能承受風險的前提下，可提高股票型資產的比重（如科技股），長期持有以享受複利效果。"
            else:
                strategy_text = "根據您的財務現況，建議保持穩健的收支管理與適度的資產配置。"
                
            st.write(strategy_text)

            st.markdown("---")
            st.header("資產配置建議")
            st.markdown("### 量化最佳化投資組合")
            
            if analyzer.profile_type in ["優先儲蓄型", "債務整理型"]:
                st.warning("系統提醒：您目前的財務階段不建議投入高風險投資。建議將資金 100% 放置於銀行高利活存中，待建立起基本安全網後再行投資。")
            else:
                weights = st.session_state.get('opt_weights', {})
                data_df = st.session_state.get('data_df', None)
                
                if weights:
                    # 顯示動態計算的標的與比例
                    chart_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
                    for i, (ticker, w) in enumerate(weights.items()):
                        color = chart_colors[i % len(chart_colors)]
                        st.markdown(f"""
                        <div style="background-color: transparent; padding: 16px; border-radius: 6px; margin-bottom: 12px; border-left: 5px solid {color}; border-top: 1px solid #333; border-right: 1px solid #333; border-bottom: 1px solid #333;">
                            <h4 style="margin: 0; color: #e6edf3;">{ticker}</h4>
                            <p style="margin: 5px 0 0 0; color: #a1aebf;">建議配置比例：<strong>{w * 100:.1f}%</strong></p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    st.markdown("#### 🤖 系統量化配置解析")
                    
                    # 產生動態客觀分析 (針對標的本身數據)
                    top_ticker = max(weights, key=weights.get)
                    top_weight = weights[top_ticker] * 100
                    
                    if data_df is not None and top_ticker in data_df.columns:
                        price_series = data_df[top_ticker].dropna()
                        total_return = (price_series.iloc[-1] / price_series.iloc[0] - 1) * 100
                        years = len(price_series) / 252
                        ann_return = ((price_series.iloc[-1] / price_series.iloc[0]) ** (1 / years) - 1) * 100 if years > 0 else 0
                        volatility = price_series.pct_change().std() * (252 ** 0.5) * 100
                        
                        analysis_text = f"**配置理由：** 客觀數據顯示，本次配置的核心重倉標的 **{top_ticker}** (資金佔比 {top_weight:.1f}%) 在過去的歷史區間內，累積成長報酬達 **{total_return:.1f}%** (年化報酬約 {ann_return:.1f}%)，且其年化波動度為 {volatility:.1f}%。\\n\\n"
                        analysis_text += f"系統演算法偵測到 **{top_ticker}** 的歷史走勢具備優異的表現，因此賦予最高權重。同時為了避免單一資產風險過高，系統自動挑選了其餘 {len(weights)-1} 檔標的與之搭配。透過資產間漲跌互補的特性，在維持獲利成長空間的同時，數學化地壓低整體組合的下跌風險。"
                    else:
                        analysis_text = f"**配置理由：** 客觀數據顯示，核心標的 **{top_ticker}** (資金佔比 {top_weight:.1f}%) 具備良好的風險報酬特徵。系統透過將其與其餘 {len(weights)-1} 檔標的進行搭配，利用資產間漲跌互補的特性來分散單一股價下跌的風險。"
                    
                    st.info(analysis_text)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    col_chart, col_summary = st.columns([1, 1.2])
                    with col_chart:
                        st.markdown("### 投資組合圓餅圖")
                        fig2 = plot_allocation_pie(weights, chart_colors)
                        st.plotly_chart(fig2, use_container_width=True)
                    
                    with col_summary:
                        st.markdown("### 歷史回測表現")
                        if data_df is not None:
                            fig3 = plot_historical_backtest(data_df, weights)
                            st.plotly_chart(fig3, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
