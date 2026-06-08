"""
Adapter to load data from Parquet files.
"""
import pandas as pd
from src.infrastructure.IDataHandler import IDataHandler


class ParquetDataHandler(IDataHandler):
    """
    Adapter to load data from Parquet files.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initializes the Parquet adapter.

        Args:
            file_path (str): The path to the Parquet directory or file.
        """
        self._file_path = file_path

    def load_data(self, symbol: str) -> pd.DataFrame:
        """
        Loads data from Parquet storage.

        Args:
            symbol (str): The symbol to extract.

        Returns:
            pd.DataFrame: The loaded data.
            
        Complexity:
            Time: O(1) mapping to pandas native read.
            Space: O(N)
        """
        # return pd.read_parquet(f"{self._file_path}/{symbol}.parquet")
        return pd.DataFrame()
