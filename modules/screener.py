import pandas as pd
import numpy as np
import os

class MarketScreener:
    def __init__(self, data_path=None):
        if data_path is None:
            self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'market_data.csv')
        else:
            self.data_path = data_path
            
    def screen(self, top_n=15, strategy="momentum"):
        """
        過濾標的。
        strategy: 
        - "momentum": 過去半年報酬率最高
        - "low_volatility": 過去半年波動度最低
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError("找不到本地市場資料庫，請先執行 scripts/update_market_data.py")
            
        # 第一列通常是 Date，且 header 有可能是多層次，要處理 yfinance 帶下來的格式
        # 我們在 update_market_data 時有直接 to_csv()
        # pandas 預設讀取 yf.download['Close']
        df = pd.read_csv(self.data_path, index_col=0, parse_dates=True)
        
        # 為了計算動能，取最近半年的交易日 (約 126 天)
        # 如果總資料不足 126 天，就取全部
        days = min(126, len(df))
        
        recent_data = df.iloc[-days:]
        
        # 計算報酬率
        returns = (recent_data.iloc[-1] - recent_data.iloc[0]) / recent_data.iloc[0]
        
        # 計算波動度 (日報酬標準差)
        daily_returns = recent_data.pct_change().dropna()
        volatility = daily_returns.std() * np.sqrt(252) # 年化
        
        if strategy == "momentum":
            # 排除負報酬的標的，然後取最高
            returns = returns[returns > 0]
            selected = returns.sort_values(ascending=False).head(top_n).index.tolist()
        elif strategy == "low_volatility":
            # 取波動最低的
            selected = volatility.sort_values(ascending=True).head(top_n).index.tolist()
        else:
            # 預設：全拿前 N 檔 (這裡直接照原順序取，實務不建議)
            selected = df.columns[:top_n].tolist()
            
        # 確保選出來的標的至少大於等於 2，才能做組合
        if len(selected) < 2:
            selected = df.columns[:min(top_n, len(df.columns))].tolist()
            
        return selected, df[selected]

