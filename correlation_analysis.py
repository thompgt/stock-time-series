import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

def run_correlation_analysis(db_path="stocks.db"):
    print("Loading data for correlation analysis...")
    with duckdb.connect(db_path) as con:
        # Load all data
        df = con.execute("SELECT date, close, ticker FROM stock_prices ORDER BY date").df()
    
    # Pivot to get tickers as columns
    pivot_df = df.pivot(index='date', columns='ticker', values='close').dropna()
    
    # 1. Pearson Correlation between Tickers
    print("\n--- Pearson Correlation Matrix ---")
    corr_matrix = pivot_df.corr()
    print(corr_matrix)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title("Ticker Price Correlation")
    plt.show()
    
    # 2. Autocorrelation Analysis (NVDA)
    if 'NVDA' in pivot_df.columns:
        print("\nPlotting ACF and PACF for NVDA...")
        series = pivot_df['NVDA']
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # ACF (Autocorrelation Function)
        plot_acf(series, ax=ax1, lags=40, title="NVDA Autocorrelation (ACF)")
        
        # PACF (Partial Autocorrelation Function)
        plot_pacf(series, ax=ax2, lags=40, title="NVDA Partial Autocorrelation (PACF)")
        
        plt.tight_layout()
        plt.show()
    else:
        print("NVDA data not found in pivot table.")

if __name__ == "__main__":
    run_correlation_analysis()
