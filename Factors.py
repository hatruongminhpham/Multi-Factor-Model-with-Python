import pandas as pd
from Factor import *

class Factors:
    def __init__(self, factor_dict, time_df):
        self.factors = factor_dict
        self.time_df = time_df
        for ticker, df in self.factors.items():
            self.factors[ticker] = Factor(ticker, df, self.time_df)

    def merge_dummy(self):
        full_data = self.time_df
        for factor in self.factors.values():
            full_data = full_data.join(factor.get_dummy())
        return full_data
    
    def merge_pct_change(self):
        full_data = self.time_df
        for factor in self.factors.values():
            full_data = full_data.join(factor.get_pct_change())
        return full_data

    def merge_all(self):
        full_data = self.time_df
        for factor in self.factors.values():
            full_data = full_data.join(factor.get_all_df())
        return full_data

    # Todos: 
    def __str__(self):
        return None

    def fix_date(self, df):
        return None
    
    def create_data_frame(self):
        return None
    
# if __name__ == "__main__":
#     factors = pd.read_excel("Factors_Example.xlsx", sheet_name=None)
#     from Stocks import *
#     stocks = pd.read_excel("Stock_Data.xlsx",  sheet_name=None)
#     y = Stocks(stocks)
#     print(y.time_df)
#     time = y.get_time_df()
#     x = Factors(factors, time)
#     print(x.merge_all().to_csv(".csv"))