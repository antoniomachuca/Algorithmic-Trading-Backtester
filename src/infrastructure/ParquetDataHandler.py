"""
Adapter to load and save data from/to Parquet files.
"""
import os
import pandas as pd
from src.infrastructure.IDataHandler import IDataHandler
from src.infrastructure.IDataWriter import IDataWriter


class ParquetDataHandler(IDataHandler, IDataWriter):
    """
    Adapter to handle data serialization using Parquet.
    Implements both IDataHandler and IDataWriter following ISP.
    """

    def __init__(self, dir_path: str) -> None:
        """
        Initializes the Parquet adapter.

        Args:
            dir_path (str): The path to the directory where Parquet files are stored.
        """
        self._dir_path = dir_path
        # Ensure the directory exists
        os.makedirs(self._dir_path, exist_ok=True)

    def load_data(self, symbol: str) -> pd.DataFrame:
        """
        Loads data from Parquet storage.

        Args:
            symbol (str): The symbol to extract.

        Returns:
            pd.DataFrame: The loaded data.
            
        Complexity:
            Time: O(1) mapping to pandas native read.
            Space: O(N) where N is the length of the time series.
        """
        safe_name = symbol.replace(" ", "_").replace("/", "_")
        file_path = os.path.join(self._dir_path, f"{safe_name}.parquet")
        try:
            return pd.read_parquet(file_path)
        except FileNotFoundError:
            return pd.DataFrame()

    def save_data(self, symbol: str, data: pd.DataFrame) -> None:
        """
        Saves historical data for a given symbol to Parquet storage.

        Args:
            symbol (str): The financial instrument ticker.
            data (pd.DataFrame): The vectorized time-series data to save.
            
        Complexity:
            Time: O(1) wrapper for highly optimized C-level Parquet write operations.
            Space: O(1) auxiliary space.
        """
        if data.empty:
            return
            
        safe_name = symbol.replace(" ", "_").replace("/", "_")
        file_path = os.path.join(self._dir_path, f"{safe_name}.parquet")
        data.to_parquet(file_path, engine='pyarrow', index=True)
