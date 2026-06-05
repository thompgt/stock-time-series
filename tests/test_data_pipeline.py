import pytest
import os
import duckdb
import pandas as pd
from fetch_data import fetch_and_save

def test_fetch_and_save():
    test_db = "test_stocks.db"
    test_ticker = "MSFT"
    
    # Clean up before test
    if os.path.exists(test_db):
        os.remove(test_db)
    
    try:
        # Run fetch
        fetch_and_save(ticker=test_ticker, period="1mo", db_path=test_db)
        
        # Verify database exists
        assert os.path.exists(test_db)
        
        # Verify data content
        con = duckdb.connect(test_db)
        df = con.execute(f"SELECT * FROM stock_prices WHERE ticker = '{test_ticker}'").df()
        con.close()
        
        assert not df.empty
        assert 'ticker' in df.columns
        assert (df['ticker'] == test_ticker).all()
        
    finally:
        # Clean up after test
        if os.path.exists(test_db):
            os.remove(test_db)

def test_read_data_output():
    # Verify the read_data script doesn't crash
    from read_data import read_stock_data
    # We'll use the existing stocks.db if it exists, otherwise skip
    if os.path.exists("stocks.db"):
        read_stock_data("stocks.db")
    else:
        pytest.skip("stocks.db not found for integration test")
