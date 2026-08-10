"""
Momentum strategy implementation.
"""
import pandas as pd
import numpy as np
from src.core.IStrategy import IStrategy


class MomentumStrategy(IStrategy):
    """
    Momentum-based trading strategy.
    Generates signals based on the rate of change over a specific period.
    """

    def __init__(self, period: int) -> None:
        """
        Initializes the momentum strategy.

        Args:
            period (int): The lookback period to calculate momentum.
        """
        if period <= 0:
            raise ValueError("Period must be a strictly positive integer.")
            
        self._period = period

    def calculate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Calculates trading signals vectorially based on momentum.

        Args:
            data (pd.DataFrame): Must contain a 'close' price column.

        Returns:
            pd.Series[int]: Vectorized trading signals.

        Complexity:
            Time: O(N) asymptotically via pandas vectorization.
            Space: O(N) where N is the length of the time series.
        """
        close_prices = data['close']
        momentum = close_prices.pct_change(periods=self._period)
        
        signals = np.where(momentum > 0, 1, -1)
        signals = np.where(momentum.isna(), 0, signals)
        
        return pd.Series(signals, index=data.index).astype(int)
