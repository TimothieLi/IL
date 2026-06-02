class FinancialProfileAnalyzer:
    def __init__(self, income, fixed_expenses, variable_expenses, savings, debt, investable, goal_years):
        self.income = income
        self.fixed_expenses = fixed_expenses
        self.variable_expenses = variable_expenses
        self.savings = savings
        self.debt = debt
        self.investable = investable
        self.goal_years = goal_years
        
        # 計算衍生指標
        self.total_expenses = self.fixed_expenses + self.variable_expenses
        self.monthly_balance = self.income - self.total_expenses
        
        # 避免除以 0
        self.savings_rate = self.monthly_balance / self.income if self.income > 0 else 0
        self.expense_rate = self.total_expenses / self.income if self.income > 0 else 0
        self.debt_to_income = self.debt / self.income if self.income > 0 else 0
        self.emergency_fund_months = self.savings / self.total_expenses if self.total_expenses > 0 else 0
        
        # 自動推估
        self.profile_type, self.profile_advice = self._determine_profile_type()
        self.risk_tolerance = self._infer_risk_tolerance()
        self.health_score = self._calculate_health_score()

    def _infer_risk_tolerance(self):
        # 根據緊急預備金、儲蓄狀況與投資年限推估風險能力
        if self.profile_type in ["優先儲蓄型", "債務整理型", "消費控管型"]:
            return "保守型"
        if self.goal_years in ["1 年內", "3 年"]:
            return "保守型"
        elif self.goal_years == "10 年以上" and self.emergency_fund_months >= 6 and self.savings_rate >= 0.2:
            return "積極型"
        else:
            return "穩健型"

    def _calculate_health_score(self):
        score = 0
        if self.savings_rate >= 0.20:
            score += 25
        if self.emergency_fund_months >= 3:
            score += 25
        if self.debt_to_income <= 6:
            score += 20
        if self.monthly_balance > 0:
            score += 20
        if self.investable > 0:
            score += 10
        return min(score, 100)

    def _determine_profile_type(self):
        if self.emergency_fund_months < 3:
            return "優先儲蓄型", "先建立 3 到 6 個月緊急預備金，避免過早投入高風險投資。"
        elif self.debt_to_income > 6:
            return "債務整理型", "優先降低高利率負債，減少利息壓力後再進行投資。"
        elif self.savings_rate < 0.2:
            return "消費控管型", "檢視非必要支出，提高每月結餘與儲蓄率。"
        elif self.goal_years in ["5 年", "10 年以上"] and self.emergency_fund_months >= 6:
            return "成長投資型", "可提高長期 ETF 或股票型資產比例，但仍需保留緊急預備金。"
        else:
            return "穩健理財型", "可採用定期定額、定存、債券型基金或穩健 ETF。"
