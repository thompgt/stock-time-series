import duckdb
import pandas as pd

def read_stock_data(db_path="stocks.db"):
    print(f"Reading data from DuckDB: {db_path}...")
    # Connect to DuckDB using context manager
    with duckdb.connect(db_path) as con:
        # Query data
        df = con.execute("SELECT * FROM stock_prices WHERE ticker = 'NVDA' ORDER BY date DESC LIMIT 10").df()
        
        print("\nLast 10 rows of NVDA stock data:")
        print(df)
        
        # Get total count
        count = con.execute("SELECT COUNT(*) FROM stock_prices").fetchone()[0]
        print(f"\nTotal rows in table: {count}")

if __name__ == "__main__":
    read_stock_data()
