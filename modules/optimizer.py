import numpy as np
import pandas as pd
from scipy.optimize import minimize

class PortfolioOptimizer:
    def __init__(self, expected_returns, cov_matrix, risk_free_rate=0.015):
        self.expected_returns = expected_returns
        self.cov_matrix = cov_matrix
        self.risk_free_rate = risk_free_rate
        self.num_assets = len(expected_returns)

    def optimize(self, profile_type):
        """
        根據使用者的理財類型，選擇不同的最佳化目標。
        """
        # 動態調整權重上限：如果標的池很大，強制要求分散化
        max_weight = min(1.0, 3.0 / max(1, self.num_assets)) if self.num_assets > 5 else 1.0
        
        if profile_type in ["優先儲蓄型", "債務整理型", "消費控管型", "保守型"]:
            return self._minimize_volatility(weight_bounds=(0.0, max_weight))
        elif profile_type in ["穩健理財型", "穩健型"]:
            # 折衷：夏普值最佳化，但設定個別資產權重上限，避免過度集中高風險資產
            return self._maximize_sharpe(weight_bounds=(0.0, min(0.4, max_weight)))
        else:
            # 偏積極 (成長投資型)，最大化夏普值
            return self._maximize_sharpe(weight_bounds=(0.0, max_weight))

    def _portfolio_annualised_performance(self, weights):
        returns = np.sum(self.expected_returns * weights)
        std = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
        return std, returns

    def _neg_sharpe_ratio(self, weights):
        p_var, p_ret = self._portfolio_annualised_performance(weights)
        # 避免 p_var 過小導致除以零錯誤
        if p_var == 0:
            return 0
        return -(p_ret - self.risk_free_rate) / p_var

    def _portfolio_volatility(self, weights):
        return self._portfolio_annualised_performance(weights)[0]

    def _maximize_sharpe(self, weight_bounds=(0.0, 1.0)):
        args = ()
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple(weight_bounds for _ in range(self.num_assets))
        
        init_guess = self.num_assets * [1. / self.num_assets]
        
        result = minimize(self._neg_sharpe_ratio, init_guess, args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
        
        # 轉成 Dictionary
        return {idx: round(weight, 4) for idx, weight in zip(self.expected_returns.index, result.x)}

    def _minimize_volatility(self, weight_bounds=(0.0, 1.0)):
        args = ()
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple(weight_bounds for _ in range(self.num_assets))
        
        init_guess = self.num_assets * [1. / self.num_assets]
        
        result = minimize(self._portfolio_volatility, init_guess, args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
                          
        return {idx: round(weight, 4) for idx, weight in zip(self.expected_returns.index, result.x)}
