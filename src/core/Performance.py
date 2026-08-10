"""
Performance calculation domain service.
"""
import pandas as pd
import numpy as np


class Performance:
    """
    Value Object / Domain Service for calculating backtest performance metrics.
    All calculations are strictly vectorized for performance.
    """

    @staticmethod
    def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float) -> float:
        """
        Calculates the annualized Sharpe Ratio.
        Mathematical definition: SR = (E[R] - Rf) / sigma
        
        Args:
            returns (pd.Series[float]): Time-series of periodic returns.
            risk_free_rate (float): The annualized risk-free rate.

        Returns:
            float: The annualized Sharpe Ratio.
            
        Complexity:
            Time: O(N) array operation.
            Space: O(N) scalar aggregation.
        """
        excess_returns = returns - (risk_free_rate / 252.0)
        mean_excess_return = float(excess_returns.mean())
        std_excess_return = float(excess_returns.std())
        
        # Avoid division by zero
        if std_excess_return == 0.0:
            return 0.0
        else:
            sharpe_ratio = (mean_excess_return / std_excess_return) * np.sqrt(252.0)
            return float(sharpe_ratio)

    @staticmethod
    def calculate_max_drawdown(equity_curve: pd.Series) -> float:
        """
        Calculates the Maximum Drawdown (MDD).
        Mathematical definition: MDD = min( (P_t - Peak_t) / Peak_t )
        
        Args:
            equity_curve (pd.Series[float]): The portfolio equity curve.

        Returns:
            float: The maximum drawdown percentage.
            
        Complexity:
            Time: O(N) array rolling maximum.
            Space: O(N) temporary array allocation.
        """
        rolling_max = equity_curve.cummax()
        drawdown = (equity_curve - rolling_max) / rolling_max
        max_dd = float(drawdown.min())
        return abs(max_dd)

    @staticmethod
    def calculate_annualized_volatility(returns: pd.Series) -> float:
        """
        Calculates the annualized volatility of the strategy.
        Mathematical definition: Vol = sigma * sqrt(252)
        
        Args:
            returns (pd.Series[float]): Time-series of periodic returns.

        Returns:
            float: Annualized volatility.
            
        Complexity:
            Time: O(N) vector operation.
            Space: O(N) scalar aggregation.
        """
        volatility = float(returns.std() * np.sqrt(252.0))
        return volatility

    @staticmethod
    def calculate_cagr(equity_curve: pd.Series) -> float:
        """
        Calculates the Compound Annual Growth Rate (CAGR).
        Mathematical definition: CAGR = (EV / BV)^(1 / n) - 1
        
        Args:
            equity_curve (pd.Series[float]): The portfolio equity curve.

        Returns:
            float: The CAGR.
            
        Complexity:
            Time: O(N)
            Space: O(N)
        """
        if len(equity_curve) == 0:
            return 0.0
            
        beginning_value = float(equity_curve.iloc[0])
        ending_value = float(equity_curve.iloc[-1])
        
        if beginning_value == 0.0:
            return 0.0
            
        years = len(equity_curve) / 252.0
        
        # Avoid division by zero or negative values
        if years <= 0.0:
            return 0.0
        else:
            cagr = (ending_value / beginning_value) ** (1.0 / years) - 1.0
            return float(cagr)
