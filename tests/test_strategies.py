"""
Unit tests for the trading strategies.
Ensures correct vectorized signal generation without NaNs causing logic breaks.
"""
import numpy.testing as npt
import pandas as pd

from src.core.MomentumStrategy import MomentumStrategy
from src.core.SMAStrategy import SMAStrategy


class TestStrategies:
    """
    Test suite for algorithm signal logic.
    """

    def test_sma_strategy_signals(self) -> None:
        """
        Validates the Simple Moving Average Strategy signals.
        """
        strategy = SMAStrategy(short_window=2, long_window=3)
        prices = pd.DataFrame({'close': [10.0, 10.0, 12.0, 15.0, 10.0]})
        signals = strategy.calculate_signals(prices)
        # idx 0: long_sma is NaN -> signal 0
        # idx 1: long_sma is NaN -> signal 0
        # idx 2: short(2)=11.0, long(3)=10.66 -> short > long -> 1
        # idx 3: short(2)=13.5, long(3)=12.33 -> short > long -> 1
        # idx 4: short(2)=12.5, long(3)=12.33 -> short > long -> 1
        expected_signals = pd.Series([0, 0, 1, 1, 1], dtype=int)
        npt.assert_array_equal(signals.values, expected_signals.values)
        
    def test_momentum_strategy_signals(self) -> None:
        """
        Validates the Momentum Strategy signals.
        """
        strategy = MomentumStrategy(period=2)
        prices = pd.DataFrame({'close': [100.0, 105.0, 95.0, 110.0, 108.0]})
        signals = strategy.calculate_signals(prices)
        # idx 0: momentum NaN -> signal 0
        # idx 1: momentum NaN -> signal 0
        # idx 2: 95 / 100 - 1 = -0.05 -> < 0 -> -1
        # idx 3: 110 / 105 - 1 = +0.047 -> > 0 -> 1
        # idx 4: 108 / 95 - 1 = +0.136 -> > 0 -> 1
        expected_signals = pd.Series([0, 0, -1, 1, 1], dtype=int)
        npt.assert_array_equal(signals.values, expected_signals.values)
