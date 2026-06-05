import pytest
import numpy as np
import pandas as pd
from stationarity_test import check_stationarity

def test_check_stationarity_known_stationary():
    # Generate stationary white noise
    np.random.seed(42)
    stationary_series = pd.Series(np.random.normal(0, 1, 100))
    
    # White noise should be stationary
    is_stationary = check_stationarity(stationary_series, "White Noise")
    assert is_stationary == True

def test_check_stationarity_known_non_stationary():
    # Generate a random walk (non-stationary)
    np.random.seed(42)
    non_stationary_series = pd.Series(np.random.normal(0, 1, 100)).cumsum()
    
    # Random walk is non-stationary
    is_stationary = check_stationarity(non_stationary_series, "Random Walk")
    assert is_stationary == False
