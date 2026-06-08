"""
Application Layer implementing the Backtest Engine.
"""
from src.infrastructure.IDataHandler import IDataHandler
from src.core.IStrategy import IStrategy
from src.core.Portfolio import Portfolio


class BacktestEngine:
    """
    The orchestrator of the backtesting process.
    Connects the data source, strategy, and portfolio
    """

    def __init__(self, data_handler: IDataHandler, strategy: IStrategy, portfolio: Portfolio) -> None:
        """
        Initializes the BacktestEngine with its dependencies.

        Args:
            data_handler (IDataHandler): Adapter to fetch historical data.
            strategy (IStrategy): The trading logic algorithm.
            portfolio (Portfolio): The managing positions and capital.
        """
        self._data_handler = data_handler
        self._strategy = strategy
        self._portfolio = portfolio

    def run_backtest(self, symbol: str) -> None:
        """
        Executes the backtest pipeline through vectorization.
        No iterative loops are used over the time-series.

        Args:
            symbol (str): The financial instrument to backtest.
            
        Complexity:
            Time: O(1) asymptotic execution of composed vectorized functions.
            Space: O(N) scaling with the loaded dataset length.
        """
        # 1. Fetch data via the Port (IDataHandler)
        historical_data = self._data_handler.load_data(symbol)
        
        # 2. Calculate signals (IStrategy)
        signals = self._strategy.calculate_signals(historical_data)
        
        # 3. Update the Portfolio state and apply frictions (Portfolio)
        self._portfolio.update_from_signals(signals, historical_data)
