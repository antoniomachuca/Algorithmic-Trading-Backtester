"""
Service layer for coordinating data ingestion, applying Dependency Inversion Principle (DIP).
"""
from typing import List
from src.infrastructure.IDataHandler import IDataHandler
from src.infrastructure.IDataWriter import IDataWriter


class DataIngestionService:
    """
    Coordinates the extraction of data from a source (IDataHandler) 
    and loads it into a high-performance destination (IDataWriter).
    """

    def __init__(self, reader: IDataHandler, writer: IDataWriter) -> None:
        """
        Initializes the ingestion service with abstract dependencies.

        Args:
            reader (IDataHandler): The source of the historical data.
            writer (IDataWriter): The destination for the historical data.
        """
        self._reader = reader
        self._writer = writer

    def ingest(self, symbols: List[str]) -> None:
        """
        Executes the ingestion pipeline for a list of symbols.
        
        Args:
            symbols (List[str]): List of instrument tickers to ingest.
            
        Complexity:
            Time: O(K) where K is the number of symbols. 
                  (No iteration over the actual time-series length N occurs here, 
                   strictly adhering to vectorization rules).
            Space: O(N) max memory usage at any given time for the current dataframe being processed.
        """

        for symbol in symbols:
            df = self._reader.load_data(symbol)
            if not df.empty:
                self._writer.save_data(symbol, df)
