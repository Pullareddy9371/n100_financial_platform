import pandas as pd


class RatioEngine:

    # -------------------------------
    # Profitability Ratios
    # -------------------------------

    @staticmethod
    def net_profit_margin(net_profit, sales):
        if sales == 0:
            return None
        return round((net_profit / sales) * 100, 2)

    @staticmethod
    def operating_profit_margin(op_profit, sales):
        if sales == 0:
            return None
        return round((op_profit / sales) * 100, 2)

    @staticmethod
    def return_on_equity(net_profit, equity, reserves):
        capital = equity + reserves

        if capital <= 0:
            return None

        return round((net_profit / capital) * 100, 2)

    @staticmethod
    def return_on_capital_employed(ebit, equity, reserves, borrowings):
        capital = equity + reserves + borrowings

        if capital <= 0:
            return None

        return round((ebit / capital) * 100, 2)

    @staticmethod
    def return_on_assets(net_profit, total_assets):
        if total_assets == 0:
            return None

        return round((net_profit / total_assets) * 100, 2)

    # -------------------------------
    # Liquidity Ratios
    # -------------------------------

    @staticmethod
    def current_ratio(current_assets, current_liabilities):
        if current_liabilities == 0:
            return None
        return round(current_assets / current_liabilities, 2)

    @staticmethod
    def quick_ratio(current_assets, inventory, current_liabilities):
        if current_liabilities == 0:
            return None
        return round((current_assets - inventory) / current_liabilities, 2)

    @staticmethod
    def cash_ratio(cash, current_liabilities):
        if current_liabilities == 0:
            return None
        return round(cash / current_liabilities, 2)
    
        # -------------------------------
    # Solvency Ratios
    # -------------------------------

    @staticmethod
    def debt_to_equity(total_debt, equity):
        if equity == 0:
            return None
        return round(total_debt / equity, 2)

    @staticmethod
    def interest_coverage(operating_profit, interest):
        if interest == 0:
            return None
        return round(operating_profit / interest, 2)

    @staticmethod
    def debt_ratio(total_liabilities, total_assets):
        if total_assets == 0:
            return None
        return round(total_liabilities / total_assets, 2)
    
        # -------------------------------
    # Efficiency Ratios
    # -------------------------------

    @staticmethod
    def asset_turnover(sales, total_assets):
        if total_assets == 0:
            return None
        return round(sales / total_assets, 2)

    @staticmethod
    def fixed_asset_turnover(sales, fixed_assets):
        if fixed_assets == 0:
            return None
        return round(sales / fixed_assets, 2)

    @staticmethod
    def investment_turnover(sales, investments):
        if investments == 0:
            return None
        return round(sales / investments, 2)
    
        # -------------------------------
    # Growth Ratios
    # -------------------------------

    @staticmethod
    def sales_growth(current_sales, previous_sales):
        if previous_sales == 0:
            return None
        return round(((current_sales - previous_sales) / previous_sales) * 100, 2)

    @staticmethod
    def profit_growth(current_profit, previous_profit):
        if previous_profit == 0:
            return None
        return round(((current_profit - previous_profit) / previous_profit) * 100, 2)

    @staticmethod
    def asset_growth(current_assets, previous_assets):
        if previous_assets == 0:
            return None
        return round(((current_assets - previous_assets) / previous_assets) * 100, 2)
    
        # -------------------------------
    # Valuation Ratios
    # -------------------------------

    @staticmethod
    def pe_ratio(market_price, eps):
        if eps == 0:
            return None
        return round(market_price / eps, 2)

    @staticmethod
    def pb_ratio(market_price, book_value):
        if book_value == 0:
            return None
        return round(market_price / book_value, 2)

    @staticmethod
    def earnings_yield(eps, market_price):
        if market_price == 0:
            return None
        return round((eps / market_price) * 100, 2)