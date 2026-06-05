import duckdb
import pandas as pd

def read_stock_data(db_path="stocks.db"):
    print(f"Reading data from DuckDB: {db_path}...")
    # Connect to DuckDB
    con = duckdb.connect(db_path)
    
    # Query data
    df = con.execute("SELECT * FROM stock_prices LIMIT 10").df()
    
    print("\nFirst 10 rows of stock data:")
    print(df)
    
    # Get total count
    count = con.execute("SELECT COUNT(*) FROM stock_prices").fetchone()[0]
    print(f"\nTotal rows in table: {count}")
    
    con.close()

if __name__ == "__main__":
    read_stock_data()
