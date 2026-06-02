import pandas as pd
import numpy as np

class DataService:
    def __init__(self, data_df):
        """
        data_df: 已清洗好的歷史收盤價 DataFrame (index=日期, columns=標的)
        """
        self.data = data_df
        self.returns = None
        self.expected_returns = None
        self.cov_matrix = None
        
    def process_data(self):
        # 確保沒有 NaN (前向填充再後向填充)
        df = self.data.ffill().bfill()
        self.data = df
        
        # 計算每日報酬率
        self.returns = df.pct_change().dropna()
        
        # 計算年化預期報酬率 (假設一年有 252 個交易日)
        self.expected_returns = self.returns.mean() * 252
        
        # 計算年化共變異數矩陣
        self.cov_matrix = self.returns.cov() * 252
        
        return self.expected_returns, self.cov_matrix
