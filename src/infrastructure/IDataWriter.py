"""
Port (Interface) for data writers.
"""
from abc import ABC, abstractmethod
import pandas as pd


class IDataWriter(ABC):
    """
    Port (Interface) for data writers. Follows Interface Segregation Principle (ISP).
    """

    @abstractmethod
    def save_data(self, symbol: str, data: pd.DataFrame) -> None:
        """
        Saves historical data for a given symbol.

        Args:
            symbol (str): The financial instrument ticker.
            data (pd.DataFrame): The vectorized time-series data to save.
            
        """
        pass
