import plotly.graph_objects as go
import pandas as pd
import numpy as np

def plot_income_expense_pie(analyzer):
    labels = ['固定支出', '變動支出', '每月結餘']
    balance_for_chart = max(analyzer.monthly_balance, 0)
    values = [analyzer.fixed_expenses, analyzer.variable_expenses, balance_for_chart]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, 
                                 marker_colors=['#ff7f0e', '#d62728', '#2ca02c'],
                                 textinfo='label+percent')])
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e6edf3",
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=False
    )
    return fig

def plot_allocation_pie(weights, colors=None):
    labels = list(weights.keys())
    values = list(weights.values())
    
    # 針對標的給定一些預設顏色以求美觀
    if colors is None:
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values, 
        hole=.4,
        textinfo='label+percent',
        marker_colors=colors,
        hovertemplate="<b>%{label}</b><br>比例: %{percent}%<extra></extra>"
    )])
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e6edf3",
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=False
    )
    return fig

def plot_historical_backtest(data_df, weights):
    """
    繪製歷史回測走勢圖。
    data_df: 歷史收盤價 DataFrame
    weights: {ticker: weight} 字典
    """
    # 避免空資料
    if data_df is None or data_df.empty:
        return go.Figure()
        
    # 將價格正規化，基期設為 100
    normalized_data = data_df / data_df.iloc[0] * 100
    
    # 計算投資組合的總價值變化
    portfolio_value = pd.Series(0.0, index=data_df.index)
    for ticker, weight in weights.items():
        if ticker in normalized_data.columns:
            portfolio_value += normalized_data[ticker] * weight
            
    fig = go.Figure()
    # 投資組合線
    fig.add_trace(go.Scatter(x=portfolio_value.index, y=portfolio_value, 
                             mode='lines', name='您的專屬組合', 
                             line=dict(color='#00ff00', width=3)))
    
    # 大盤基準線 (假設取清單中的第一檔，通常是 0050.TW 作為基準)
    benchmark_ticker = list(weights.keys())[0]
    if benchmark_ticker in normalized_data.columns:
        fig.add_trace(go.Scatter(x=normalized_data.index, y=normalized_data[benchmark_ticker], 
                                 mode='lines', name=f'對比基準 ({benchmark_ticker})', 
                                 line=dict(color='#888888', width=1.5, dash='dash')))
        
    fig.update_layout(
        title="歷史回測走勢圖 (基期=100)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e6edf3",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#333333'),
        margin=dict(t=40, b=20, l=20, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig
