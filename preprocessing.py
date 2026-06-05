import duckdb
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class TimeSeriesPreprocessor:
    def __init__(self, df, target_col='close'):
        self.df = df.copy()
        self.target_col = target_col
        self.scaler = None

    def log_transform(self):
        print("Applying log transform...")
        self.df[f'log_{self.target_col}'] = np.log(self.df[self.target_col])
        return self

    def difference(self, lags=1):
        print(f"Applying differencing (lags={lags})...")
        col_to_diff = f'log_{self.target_col}' if f'log_{self.target_col}' in self.df.columns else self.target_col
        self.df[f'diff_{col_to_diff}'] = self.df[col_to_diff].diff(lags)
        return self

    def add_lags(self, n_lags=5):
        print(f"Adding {n_lags} lags...")
        col = self.df.columns[-1] # Apply to the most recent transform
        for i in range(1, n_lags + 1):
            self.df[f'lag_{i}'] = self.df[col].shift(i)
        return self

    def add_rolling_features(self, windows=[5, 21]):
        print(f"Adding rolling features for windows: {windows}...")
        col = self.target_col
        for w in windows:
            self.df[f'rolling_mean_{w}'] = self.df[col].rolling(window=w).mean()
            self.df[f'rolling_std_{w}'] = self.df[col].rolling(window=w).std()
        return self

    def scale(self, method='standard'):
        print(f"Applying {method} scaling...")
        self.scaler = StandardScaler() if method == 'standard' else MinMaxScaler()
        # Scale only numeric columns, excluding date/ticker
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        self.df[numeric_cols] = self.scaler.fit_transform(self.df[numeric_cols])
        return self

    def get_data(self):
        return self.df.dropna()

def run_preprocessing_pipeline(db_path="stocks.db", ticker="NVDA"):
    print(f"Running preprocessing pipeline for {ticker}...")
    con = duckdb.connect(db_path)
    df = con.execute(f"SELECT * FROM stock_prices WHERE ticker = '{ticker}' ORDER BY date").df()
    con.close()
    
    preprocessor = TimeSeriesPreprocessor(df)
    
    processed_df = (preprocessor
                    .log_transform()
                    .difference()
                    .add_lags(n_lags=3)
                    .add_rolling_features(windows=[5, 10])
                    .scale(method='standard')
                    .get_data())
    
    print("\nPreprocessed Data Sample (First 5 rows):")
    print(processed_df.head())
    print(f"\nShape of processed data: {processed_df.shape}")
    
    return processed_df

if __name__ == "__main__":
    run_preprocessing_pipeline()
