"""
Adapter to load data directly via the Bloomberg API.
"""
import pandas as pd
try:
    from xbbg import blp
except ImportError:
    blp = None

from src.infrastructure.IDataHandler import IDataHandler


class BloombergDataHandler(IDataHandler):
    """
    Adapter to load data directly via the Bloomberg Terminal.
    Uses 'xbbg' under the hood to interface with blpapi and return vectorized DataFrames.
    """

    def __init__(self, api_connection: object, start_date: str, end_date: str) -> None:
        """
        Initializes the Bloomberg API adapter.

        Args:
            api_connection (object): An injected connection instance (e.g., blpapi.Session or xbbg blp module).
            start_date (str): Start date for data extraction (e.g., '2020-01-01').
            end_date (str): End date for data extraction (e.g., '2023-01-01').
        """
        if blp is None:
            raise ImportError(
                "The 'xbbg' and 'blpapi' libraries must be installed (pip install xbbg blpapi) "
                "to interact with the Bloomberg Terminal."
            )
            
        self._api_connection = api_connection
        self._start_date = start_date
        self._end_date = end_date

    def load_data(self, symbol: str) -> pd.DataFrame:
        """
        Retrieves historical data from the Bloomberg Terminal.

        Args:
            symbol (str): The Bloomberg ticker (e.g., 'AAPL US Equity').

        Returns:
            pd.DataFrame: The extracted historical data with standard column names.
            
        Complexity:
            Time: Network-bound constant asymptotic overhead. O(N) local runtime.
            Space: O(N) where N is the length of the time series.
        """
        # Fetching data directly to a pandas DataFrame purely vectorially via xbbg
        df = blp.bdh(
            tickers=symbol, 
            flds=['PX_OPEN', 'PX_HIGH', 'PX_LOW', 'PX_LAST', 'PX_VOLUME'], 
            start_date=self._start_date, 
            end_date=self._end_date
        )
        
        if df.empty:
            return pd.DataFrame()
            
        # xbbg returns MultiIndex columns (Ticker, Field). We vectorize the flattening and renaming.
        df.columns = df.columns.droplevel(0)
        
        df = df.rename(columns={
            'PX_OPEN': 'open',
            'PX_HIGH': 'high',
            'PX_LOW': 'low',
            'PX_LAST': 'close',
            'PX_VOLUME': 'volume'
        })
        
        return df
