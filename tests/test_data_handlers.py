import os
import tempfile
import unittest
from unittest.mock import MagicMock

import pandas as pd

from src.infrastructure.DataIngestionService import DataIngestionService
from src.infrastructure.HDF5DataHandler import HDF5DataHandler
from src.infrastructure.IDataHandler import IDataHandler
from src.infrastructure.IDataWriter import IDataWriter
from src.infrastructure.ParquetDataHandler import ParquetDataHandler


class TestDataHandlers(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_df = pd.DataFrame({'close': [100.0, 105.0]}, index=pd.date_range('2023-01-01', periods=2))
        
        # Create parquet file
        self.parquet_path = os.path.join(self.temp_dir.name, 'TEST.parquet')
        self.test_df.to_parquet(self.parquet_path)
        
        # Create hdf5 file
        self.hdf5_path = os.path.join(self.temp_dir.name, 'TEST.h5')
        self.test_df.to_hdf(self.hdf5_path, key='TEST')

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_parquet_data_handler(self):
        handler = ParquetDataHandler(self.temp_dir.name)
        df = handler.load_data('TEST')
        self.assertTrue('close' in df.columns)
        self.assertEqual(len(df), 2)
        
        # Test missing file returns empty df
        missing_df = handler.load_data('MISSING')
        self.assertTrue(missing_df.empty)

    def test_hdf5_data_handler(self):
        # HDF5DataHandler takes a file path, not a dir path
        handler = HDF5DataHandler(self.hdf5_path)
        df = handler.load_data('TEST')
        self.assertTrue('close' in df.columns)
        self.assertEqual(len(df), 2)
        
        # Test missing file returns empty df
        missing_df = handler.load_data('MISSING')
        self.assertTrue(missing_df.empty)

    def test_data_ingestion_service(self):
        mock_reader = MagicMock(spec=IDataHandler)
        mock_writer = MagicMock(spec=IDataWriter)
        service = DataIngestionService(mock_reader, mock_writer)
        
        mock_data = pd.DataFrame({'close': [100.0]})
        mock_reader.load_data.return_value = mock_data
        
        service.ingest(['SYM1', 'SYM2'])
        self.assertEqual(mock_writer.save_data.call_count, 2)

if __name__ == '__main__':
    unittest.main()
