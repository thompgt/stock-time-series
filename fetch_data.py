import yfinance as yf
import duckdb
import pandas as pd
import os

def fetch_and_save(ticker="AAPL", period="5y", db_path="stocks.db"):
    print(f"Fetching data for {ticker}...")
    # Fetch data
    df = yf.download(ticker, period=period)
    
    # Flatten multi-index columns if they exist (yfinance sometimes returns them)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    # Reset index to make 'Date' a column
    df = df.reset_index()
    
    # Clean column names (DuckDB prefers lowercase/no spaces)
    df.columns = [c.replace(' ', '_').lower() for c in df.columns]
    
    # Add ticker column
    df['ticker'] = ticker

    print(f"Saving to DuckDB: {db_path}...")
    # Connect to DuckDB and save
    con = duckdb.connect(db_path)
    con.execute("CREATE TABLE IF NOT EXISTS stock_prices AS SELECT * FROM df WHERE 1=0")
    con.execute("INSERT INTO stock_prices SELECT * FROM df")
    con.close()
    
    print("Data successfully saved.")

if __name__ == "__main__":
    fetch_and_save()
