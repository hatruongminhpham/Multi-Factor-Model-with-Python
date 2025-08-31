import pandas as pd
import numpy as np

class Factor:
    def __init__(self, ticker, factor, time):
        # Cleaning the data
        self.ticker = ticker
        self.factor = factor
        self.time_df = time
        self.full_data = self.factor
        self.full_data = self.full_data.drop(["Event", "Survey", "Actual", "Prior", "Relevance"], axis = 1)
        
        # Normalize data to numeric filled in Na values
        self.full_data.replace("--", np.NaN, inplace = True)
        if self.full_data["Revised"].dtype != int and self.full_data["Revised"].dtype != float:
            self.full_data["Revised"] = self.full_data["Revised"].apply(lambda x: float(x[:-1]) if x is not np.NaN else 0.0)
        
        # sometimes the data became a pd.series instead of df so this is for safety measure
        if isinstance(self.full_data, pd.Series):
            self.full_data = self.full_data.to_frame()
        
        # fixing date to int
        if self.full_data["Date"].dtype != int:
            self.full_data["Date"] = self.full_data["Date"].dt.strftime('%Y%m%d').astype(int)
        self.full_data = self.full_data.rename({"Revised": ticker + "_data"}, axis = 1)
        self.full_data = self.full_data.set_index("Date")

        # Dropping dupplicate if needed
        self.full_data = self.full_data[~self.full_data.index.duplicated(keep='first')]

        # % change of the variables
        self.full_data["{}_pct_change".format(ticker)] = self.full_data.sort_values("Date").pct_change().sort_values("Date", ascending = False)

        # Add them all up to the entire data
        self.full_data = self.time_df.join(self.full_data)
        self.full_data = self.full_data.fillna(0)

        # Dummy variables dataframe
        self.full_data[ticker + "_dummy"] = self.full_data[ticker + "_pct_change"].apply(lambda x: 1 if x != 0 else 0)


    def __str__(self):
        return self.full_data.to_string()

    # get informations
    def get_dummy(self):
        return self.full_data[self.ticker + "_dummy"]

    def get_pct_change(self):
        return self.full_data[self.ticker + "_pct_change"]

    def get_df(self):
        return self.factor
    
    def get_all_df(self):
        return self.full_data

    def get_time(self):
        return self.time_df

    def to_csv(self):
        return self.full_data.to_csv("{}.csv".format(self.ticker))

# if __name__ == "__main__":
#     factor = pd.read_csv("Factor.csv")
#     stocks = pd.read_excel("Stock_Data.xlsx", sheet_name = None)
#     from Stocks import *
#     y = Stocks(stocks)
#     time = y.get_time_df()
#     print(time.index.dtype)
#     x = Factor("NFP", factor, time)
#     x.get_dummy()