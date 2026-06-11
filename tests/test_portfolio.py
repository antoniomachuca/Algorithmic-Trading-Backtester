"""
Unit tests for the Portfolio aggregate root.
Ensures correct vectorized translations of signals to equity curve.
"""
import pytest
import pandas as pd
import numpy as np
import numpy.testing as npt

from src.core.Portfolio import Portfolio
from src.core.IFrictionModel import IFrictionModel


class DummyZeroFriction(IFrictionModel):
    """
    Mock friction model simulating 0 transaction costs.
    """
    def calculate_friction(self, prices: pd.DataFrame, signals: pd.Series) -> pd.Series:
        return pd.Series(0.0, index=prices.index)


class DummyFixedFriction(IFrictionModel):
    """
    Mock friction model applying a fixed cost per signal change.
    """
    def calculate_friction(self, prices: pd.DataFrame, signals: pd.Series) -> pd.Series:
        trades = signals.diff().fillna(1.0) != 0.0
        return pd.Series(np.where(trades, 1.0, 0.0), index=prices.index)


class TestPortfolio:
    """
    Test suite for Portfolio state and equity calculations.
    """
    def test_update_from_signals_frictionless(self) -> None:
        """
        Validates equity calculation without transaction costs.
        Ensures O(1) vectorized logic equals theoretical expectation.
        """
        initial_capital = 100.0
        portfolio = Portfolio(initial_capital, DummyZeroFriction())
        
        prices = pd.DataFrame({'close': [100.0, 105.0, 102.0, 110.0]})
        signals = pd.Series([1, 1, -1, 0])

        portfolio.update_from_signals(signals, prices)
        equity_curve = portfolio.get_equity_curve()
        returns = prices['close'].pct_change()
        shifted_signals = signals.shift(1).fillna(0)
        expected_returns = shifted_signals * returns
        expected_equity = initial_capital * (1.0 + expected_returns).cumprod()
        
        npt.assert_array_almost_equal(equity_curve.values, expected_equity.values)

    def test_update_from_signals_with_friction(self) -> None:
        """
        Validates equity calculation applying dummy fixed transaction costs.
        """
        initial_capital = 1000.0
        portfolio = Portfolio(initial_capital, DummyFixedFriction())
        
        prices = pd.DataFrame({'close': [100.0, 110.0, 110.0]})
        signals = pd.Series([1, 1, 0]) 
        
        portfolio.update_from_signals(signals, prices)
        equity_curve = portfolio.get_equity_curve()
        returns = prices['close'].pct_change()
        shifted_signals = signals.shift(1).fillna(0)
        expected_returns = shifted_signals * returns
        costs = pd.Series([1.0, 0.0, 1.0])
        net_returns = expected_returns - costs
        expected_equity = initial_capital * (1.0 + net_returns).cumprod()
        npt.assert_array_almost_equal(equity_curve.values, expected_equity.values)
