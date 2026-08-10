"""
Interface representing a trading strategy.
"""
from abc import ABC, abstractmethod

import pandas as pd


class IStrategy(ABC):
    """
    Interface representing a trading strategy.
    """

    @abstractmethod
    def calculate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generates trading signals vectorially based on historical data.

        Args:
            data (pd.DataFrame): Historical market data (prices, volumes, etc.).

        Returns:
            pd.Series[int]: Series of signals (e.g., 1 for long, -1 for short, 0 for hold).
        """
