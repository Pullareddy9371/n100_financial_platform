import pandas as pd


class PresetScreeners:

    @staticmethod
    def quality_compounder(df):

        return df[
            (df["return_on_equity_pct"] > 15) &
            (df["debt_to_equity"] < 1.0) &
            (df["free_cash_flow_cr"] > 0)
        ]


    @staticmethod
    def value_pick(df):

        return df[
            (df["pe_ratio"] < 20) &
            (df["pb_ratio"] < 3) &
            (df["debt_to_equity"] < 2)
        ]


    @staticmethod
    def growth_accelerator(df):

        # Revenue CAGR & PAT CAGR are not available
        # Use ROE + Positive Cash Flow temporarily

        return df[
            (df["return_on_equity_pct"] > 20) &
            (df["free_cash_flow_cr"] > 0)
        ]


    @staticmethod
    def dividend_champion(df):

        return df[
            (df["dividend_yield_pct"] > 2) &
            (df["free_cash_flow_cr"] > 0)
        ]


    @staticmethod
    def debt_free_bluechip(df):

        return df[
            (df["debt_to_equity"] == 0) &
            (df["return_on_equity_pct"] > 12)
        ]


    @staticmethod
    def turnaround_watch(df):

        # Revenue CAGR unavailable
        # Use positive FCF instead

        return df[
            (df["free_cash_flow_cr"] > 0)
        ]