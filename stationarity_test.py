import duckdb
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller

def check_stationarity(series, name):
    print(f"\n--- ADF Test for {name} ---")
    result = adfuller(series.dropna())
    print(f'ADF Statistic: {result[0]:.4f}')
    print(f'p-value: {result[1]:.4f}')
    print('Critical Values:')
    for key, value in result[4].items():
        print(f'\t{key}: {value:.3f}')
    
    return result[1] < 0.05

def run_stationarity_pipeline(db_path="stocks.db", ticker="NVDA"):
    # Load data
    con = duckdb.connect(db_path)
    df = con.execute(f"SELECT date, close FROM stock_prices WHERE ticker = '{ticker}' ORDER BY date").df()
    con.close()
    
    series = df['close']
    
    # 1. Test Raw Data
    is_stationary = check_stationarity(series, "Raw Close Price")
    
    if is_stationary:
        print("Raw data is already stationary. This is unusual for stock prices!")
        return

    # 2. Try Log Transform (to stabilize variance)
    print("\nApplying Log Transform...")
    log_series = np.log(series)
    is_stationary = check_stationarity(log_series, "Log Transformed Data")
    
    # 3. Iterative Differencing
    current_series = log_series
    diff_count = 0
    while not is_stationary and diff_count < 2:
        diff_count += 1
        print(f"\nApplying Difference #{diff_count}...")
        current_series = current_series.diff().dropna()
        is_stationary = check_stationarity(current_series, f"Difference #{diff_count}")
        
    if is_stationary:
        print(f"\nSuccess! Stationarity achieved after {diff_count} difference(s).")
    else:
        print("\nFailed to achieve stationarity within 2 differences. Further transforms may be needed.")

if __name__ == "__main__":
    run_stationarity_pipeline()
