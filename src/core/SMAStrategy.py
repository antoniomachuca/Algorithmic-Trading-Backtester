"""
Simple Moving Average strategy implementation.
"""
import pandas as pd
import numpy as np
from src.core.IStrategy import IStrategy


class SMAStrategy(IStrategy):
    """
    Simple Moving Average (SMA) crossover strategy.
    Generates a +1 signal when the short SMA is above the long SMA, and -1 otherwise.
    """

    def __init__(self, short_window: int, long_window: int) -> None:
        """
        Initializes the SMA strategy.

        Args:
            short_window (int): The lookback period for the short moving average.
            long_window (int): The lookback period for the long moving average.
        """
        self._short_window = short_window
        self._long_window = long_window

    def calculate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Calculates trading signals using vectorized operations.

        Args:
            data (pd.DataFrame): Must contain a 'close' price column.

        Returns:
            pd.Series[int]: Vectorized trading signals (1, -1, or 0).

        Complexity:
            Time: O(1) asymptotically via pandas vectorization (internally O(N)).
            Space: O(N) for rolling calculations and resulting Series.
        """
        close_prices = data['close']
        short_sma = close_prices.rolling(window=self._short_window).mean()
        long_sma = close_prices.rolling(window=self._long_window).mean()
        
        # Using numpy where for fully vectorized conditional assignment
        signals = np.where(short_sma > long_sma, 1, -1)
        # Handle NaNs from rolling window explicitly without control flow breaks
        signals = np.where(short_sma.isna() | long_sma.isna(), 0, signals)
        
        return pd.Series(signals, index=data.index).astype(int)
