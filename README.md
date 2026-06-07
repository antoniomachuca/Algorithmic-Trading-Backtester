# Algorithmic Trading Backtester

## Objective
To demonstrate an impeccable software architecture and efficient time-series processing for algorithmic trading backtesting.

## Project Structure
- `src/`: Core implementation containing data loaders, strategies, backtesting engine, and performance metrics.
- `docs/architecture/`: UML diagrams and use cases defining the system architecture.
- `data/`: Directory for historical market data (Parquet / HDF5 format).
- `notebooks/`: Interactive documentation and visual results.

## Roadmap
- **Week 1 (Docs & Data)**: Architecture design, UML diagrams, and data acquisition pipeline.
- **Week 2 (Vectorization)**: Implementation of Moving Average (SMA) and Momentum strategies using $\mathcal{O}(1)$ complexity operations via vectorization (pandas/NumPy).
- **Week 3 (The Engine)**: Construction of the backtesting simulator with strict separation between execution logic and visualization.
- **Week 4 (Metrics)**: Implementation of Sharpe Ratio and Maximum Drawdown metrics, along with interactive Jupyter Notebooks for results visualization.
