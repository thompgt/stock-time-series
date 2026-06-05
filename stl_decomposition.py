import duckdb
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL

def run_stl_decomposition(db_path="stocks.db", ticker="NVDA"):
    print(f"Running STL Decomposition for {ticker}...")
    
    # Load data using context manager
    with duckdb.connect(db_path) as con:
        df = con.execute(f"SELECT date, close FROM stock_prices WHERE ticker = '{ticker}' ORDER BY date").df()
    
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    
    # STL requires a fixed frequency. Stock data has gaps (weekends).
    # We'll reindex to business days and interpolate.
    df = df.asfreq('B').ffill()
    
    # Run STL
    # Period 252 for annual seasonality in daily data
    stl = STL(df['close'], period=252)
    res = stl.fit()
    
    # Plot
    fig = res.plot()
    fig.suptitle(f'STL Decomposition: {ticker}', fontsize=16)
    plt.tight_layout()
    plt.show()
    
    print("Decomposition complete. Plot generated.")

if __name__ == "__main__":
    run_stl_decomposition()
