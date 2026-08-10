"""
Port (Interface) for data handlers.
"""
from abc import ABC, abstractmethod
import pandas as pd


class IDataHandler(ABC):
    """
    Port (Interface) for data handlers. Follows Dependency Inversion Principle (DIP).
    """

    @abstractmethod
    def load_data(self, symbol: str) -> pd.DataFrame:
        """
        Loads historical data for a given symbol.

        Args:
            symbol (str): The financial instrument ticker.

        Returns:
            pd.DataFrame: A vectorized representation of the time-series data.
            
        Complexity:
            Time: O(N) wrapper for highly optimized I/O operations.
            Space: O(N) memory allocation for the DataFrame.
        """
        pass
