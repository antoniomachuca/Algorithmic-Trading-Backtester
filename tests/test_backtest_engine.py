import unittest
from unittest.mock import MagicMock

import pandas as pd

from src.application.BacktestEngine import BacktestEngine
from src.core.IStrategy import IStrategy
from src.core.Portfolio import Portfolio
from src.core.ProportionalFrictionModel import ProportionalFrictionModel
from src.infrastructure.IDataHandler import IDataHandler


class TestBacktestEngine(unittest.TestCase):
    def setUp(self):
        self.mock_data = pd.DataFrame({'close': [100.0, 105.0, 110.0]})
        self.mock_signals = pd.Series([1, -1, 0])
        
        self.mock_handler = MagicMock(spec=IDataHandler)
        self.mock_handler.load_data.return_value = self.mock_data
        
        self.mock_strategy = MagicMock(spec=IStrategy)
        self.mock_strategy.calculate_signals.return_value = self.mock_signals
        
        friction = ProportionalFrictionModel(0.0)
        self.portfolio = Portfolio(initial_capital=1000.0, friction_model=friction)
        
        self.engine = BacktestEngine(self.mock_handler, self.mock_strategy, self.portfolio)

    def test_run_backtest(self):
        self.engine.run_backtest('TEST_SYMBOL')
        
        self.mock_handler.load_data.assert_called_once_with('TEST_SYMBOL')
        self.mock_strategy.calculate_signals.assert_called_once_with(self.mock_data)
        
        # Portfolio should have processed the signals
        equity = self.portfolio.get_equity_curve()
        self.assertEqual(len(equity), 3)

if __name__ == '__main__':
    unittest.main()
