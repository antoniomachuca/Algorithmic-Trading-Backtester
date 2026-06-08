"""
Portfolio Aggregate Root class.
"""
import pandas as pd
from src.core.IFrictionModel import IFrictionModel


class Portfolio:
    """
    Aggregate Root representing the trading portfolio.
    Manages the translation of strategy signals into actual positions and equity curve,
    while applying transaction costs via the injected IFrictionModel.
    """

    def __init__(self, initial_capital: float, friction_model: IFrictionModel) -> None:
        """
        Initializes the portfolio state.

        Args:
            initial_capital (float): The starting capital in the base currency.
            friction_model (IFrictionModel): Injected friction model for cost calculation.
        """
        self._initial_capital = initial_capital
        self._positions: pd.DataFrame = pd.DataFrame()
        self._equity_curve: pd.Series = pd.Series(dtype=float)
        self._friction_model = friction_model

    def update_from_signals(self, signals: pd.Series, prices: pd.DataFrame) -> None:
        """
        Updates the portfolio state based on signals and price data in a strictly vectorized manner.

        Args:
            signals (pd.Series[int]): Series of target positions (+1, -1, 0).
            prices (pd.DataFrame): Historical market prices.

        Complexity:
            Time: O(1) asymptotically via pandas vectorization.
            Space: O(N) where N is the length of the time series.
        """
        returns = prices['close'].pct_change()
        
        # Shift signals by 1 to prevent look-ahead bias (trade at tomorrow's open based on today's close signal)
        shifted_signals = signals.shift(1).fillna(0)
        
        # Calculate gross returns vectorially
        strategy_returns = shifted_signals * returns
        
        # Calculate friction costs vectorially
        costs = self._friction_model.calculate_friction(prices, signals)
        
        # Net returns
        net_returns = strategy_returns - costs
        
        # Cumulative compounding for equity curve
        self._equity_curve = self._initial_capital * (1.0 + net_returns).cumprod()
        self._positions = pd.DataFrame({'signal': signals, 'shifted_signal': shifted_signals})

    def get_equity_curve(self) -> pd.Series:
        """
        Retrieves the computed equity curve.

        Returns:
            pd.Series[float]: Time-series of portfolio equity.
            
        Complexity:
            Time: O(1)
            Space: O(N) by reference
        """
        return self._equity_curve
