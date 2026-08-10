"""
Adapter to load and save data from/to HDF5 files.
"""
import pandas as pd
from src.infrastructure.IDataHandler import IDataHandler
from src.infrastructure.IDataWriter import IDataWriter


class HDF5DataHandler(IDataHandler, IDataWriter):
    """
    Adapter to handle data serialization using HDF5.
    Implements both IDataHandler and IDataWriter following ISP.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initializes the HDF5 adapter.

        Args:
            file_path (str): The path to the HDF5 storage.
        """
        self._file_path = file_path

    def load_data(self, symbol: str) -> pd.DataFrame:
        """
        Loads data from the HDF5 store.

        Args:
            symbol (str): The symbol to extract.

        Returns:
            pd.DataFrame: The loaded data.
            
        Complexity:
            Time: O(N) mapping to pandas HDFStore native read.
            Space: O(N) where N is the length of the time series.
        """
        try:
            # We sanitize the symbol name to act as a valid HDF5 key
            safe_key = symbol.replace(" ", "_").replace("/", "_")
            return pd.read_hdf(self._file_path, key=safe_key)
        except (KeyError, FileNotFoundError):
            return pd.DataFrame()

    def save_data(self, symbol: str, data: pd.DataFrame) -> None:
        """
        Saves historical data for a given symbol to the HDF5 store.

        Args:
            symbol (str): The financial instrument ticker.
            data (pd.DataFrame): The vectorized time-series data to save.
            
        Complexity:
            Time: O(N) wrapper for highly optimized C-level HDF5 write operations.
            Space: O(N) auxiliary space (excluding the DataFrame).
        """
        if data.empty:
            return
            
        safe_key = symbol.replace(" ", "_").replace("/", "_")
        data.to_hdf(self._file_path, key=safe_key, mode='a', format='table')
