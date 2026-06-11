"""
Unit tests for the Performance domain service.
Ensures mathematical exactness and algorithmic accuracy without iteration.
"""
import pytest
import pandas as pd
import numpy as np
import numpy.testing as npt

from src.core.Performance import Performance

class TestPerformance:
    """
    Test suite for Performance metrics calculation.
    """

    def test_calculate_sharpe_ratio(self) -> None:
        """
        Validates the Sharpe Ratio equation: SR = (E[R] - Rf) / sigma
        """
        returns = pd.Series([0.01, -0.005, 0.02, -0.01, 0.005])
        risk_free_rate = 0.02
        excess_returns = returns - (risk_free_rate / 252.0)
        expected_sr = float((excess_returns.mean() / excess_returns.std()) * np.sqrt(252.0))
        actual_sr = Performance.calculate_sharpe_ratio(returns, risk_free_rate)
        npt.assert_almost_equal(actual_sr, expected_sr, decimal=6)

    def test_calculate_max_drawdown(self) -> None:
        """
        Validates the Maximum Drawdown equation: MDD = min( (P_t - Peak_t) / Peak_t )
        """
        #peak at 120, trough at 90. MDD = (90 - 120) / 120 = -0.25 => 0.25 (abs)
        equity_curve = pd.Series([100.0, 110.0, 120.0, 100.0, 90.0, 105.0])
        expected_mdd = 0.25
        actual_mdd = Performance.calculate_max_drawdown(equity_curve)
        npt.assert_almost_equal(actual_mdd, expected_mdd, decimal=6)

    def test_calculate_annualized_volatility(self) -> None:
        """
        Validates Annualized Volatility: Vol = sigma * sqrt(252)
        """
        returns = pd.Series([0.01, -0.02, 0.015, -0.005, 0.008])
        expected_vol = float(returns.std() * np.sqrt(252.0))
        actual_vol = Performance.calculate_annualized_volatility(returns)
        npt.assert_almost_equal(actual_vol, expected_vol, decimal=6)

    def test_calculate_cagr(self) -> None:
        """
        Validates CAGR calculation: CAGR = (EV / BV)^(1 / n) - 1
        """
        # assuming 252 trading days in a year
        bv = 100.0
        ev = 110.0
        curve = np.linspace(bv, ev, 252)
        equity_curve = pd.Series(curve)
        expected_cagr = (ev / bv) ** (1.0 / (252 / 252.0)) - 1.0 # 0.1
        actual_cagr = Performance.calculate_cagr(equity_curve)
        npt.assert_almost_equal(actual_cagr, expected_cagr, decimal=6)
