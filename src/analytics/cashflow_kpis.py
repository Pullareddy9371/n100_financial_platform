class CashFlowKPIs:

    @staticmethod
    def free_cash_flow(operating_activity, investing_activity):
        """
        Free Cash Flow = Operating Cash Flow + Investing Cash Flow
        """
        if operating_activity is None or investing_activity is None:
            return None

        return operating_activity + investing_activity


    @staticmethod
    def cfo_quality_score(cfo, net_profit):
        """
        CFO Quality = CFO / Net Profit
        """
        if net_profit == 0 or net_profit is None:
            return None

        return round(cfo / net_profit, 2)


    @staticmethod
    def capex_intensity(investing_activity, sales):
        """
        CapEx Intensity = |Investing Cash Flow| / Sales × 100
        """
        if sales == 0 or sales is None:
            return None

        return round(abs(investing_activity) / sales * 100, 2)


    @staticmethod
    def fcf_conversion_rate(free_cash_flow, operating_profit):
        """
        FCF Conversion Rate = Free Cash Flow / Operating Profit × 100
        """
        if operating_profit == 0 or operating_profit is None:
            return None

        return round(
            free_cash_flow / operating_profit * 100,
            2
        )


    @staticmethod
    def cashflow_pattern(cfo, cfi, cff):
        """
        Returns cash flow pattern.
        """

        sign = (
            "+" if cfo >= 0 else "-",
            "+" if cfi >= 0 else "-",
            "+" if cff >= 0 else "-"
        )

        patterns = {
            ("+", "-", "-"): "Reinvestor",
            ("+", "-", "+"): "Growth Funded by Debt",
            ("+", "+", "+"): "Cash Accumulator",
            ("-", "+", "+"): "Distress Signal",
            ("-", "-", "-"): "Pre-Revenue",
            ("+", "+", "-"): "Liquidating Assets",
            ("-", "-", "+"): "Mixed",
            ("+", "+", "+"): "Cash Rich"
        }

        return patterns.get(sign, "Unknown")