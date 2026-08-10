import os

import numpy as np
import pandas as pd


def generate_geometric_brownian_motion(
    S0: float, 
    mu: float, 
    sigma: float, 
    T: int, 
    dt: float
) -> np.ndarray:
    """
    Generates a vectorized Geometric Brownian Motion path.
    
    Formula:
        S_t = S_{t-1} * exp((mu - sigma^2 / 2) * dt + sigma * sqrt(dt) * Z)
        
    Algorithmic Complexity: O(N) for vectorized array operations.
    
    Args:
        S0 (float): Initial price.
        mu (float): Expected return.
        sigma (float): Volatility.
        T (int): Number of time steps.
        dt (float): Time increment.
        
    Returns:
        np.ndarray: Simulated price path vector.
    """
    np.random.seed(42)
    Z = np.random.standard_normal(T)
    returns = np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
    price_path = S0 * np.cumprod(returns)
    return price_path

def create_mock_ohlcv() -> None:
    """
    Generates a mock OHLCV DataFrame using GBM and saves it to a Parquet file.
    
    Algorithmic Complexity: O(N) vectorized pandas operations.
    """
    periods = 5000
    dates = pd.date_range(start="2010-01-01", periods=periods, freq="B")
    
    close_prices = generate_geometric_brownian_motion(
        S0=100.0, mu=0.05, sigma=0.2, T=periods, dt=1.0/252.0
    )
    
    high_prices = close_prices * (1 + np.abs(np.random.standard_normal(periods)) * 0.01)
    low_prices = close_prices * (1 - np.abs(np.random.standard_normal(periods)) * 0.01)
    open_prices = close_prices * (1 + np.random.standard_normal(periods) * 0.005)
    volume = np.random.randint(1000, 1000000, size=periods)
    
    df = pd.DataFrame({
        "open": open_prices,
        "high": high_prices,
        "low": low_prices,
        "close": close_prices,
        "volume": volume
    }, index=dates)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(project_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    file_path = os.path.join(data_dir, "mock_data.parquet")
    df.to_parquet(file_path, engine="pyarrow")
    print(f"Mock data successfully written to {file_path}")

create_mock_ohlcv()
