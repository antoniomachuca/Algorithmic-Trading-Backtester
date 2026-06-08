# Algorithmic Trading Backtester

## Objective
A vectorized backtesting engine for evaluating algorithmic trading strategies using historical market data.

## Project Structure
- `src/`: Core implementation containing data loaders, strategies, backtesting engine, and performance metrics.
- `docs/architecture/`: UML diagrams and use cases defining the system architecture.
- `data/`: Directory for historical market data (Parquet / HDF5 format).
- `scripts/`: Auxiliary scripts for automation, such as the `mock_data_generator.py` for testing.
- `notebooks/`: Interactive documentation and visual results.
- `docs/memoria/`: Formal academic documentation built with LaTeX, detailing the theoretical foundations, $\mathcal{O}(1)$ vectorization proofs, and structural design.
## Documentation 
This project includes a formal academic report written in **LaTeX**. The documentation is compiled into [`docs/memoria/main.pdf`](docs/memoria/main.pdf) and thoroughly covers:
1. **Theoretical Foundations:** Strict stochastic and statistical definitions (e.g., Geometric Brownian Motion, Sharpe Ratio, Maximum Drawdown).
2. **Asymptotic Complexity:** Explanations of how the engine achieves $\mathcal{O}(1)$ execution time for array operations through `pandas` and `NumPy` vectorization, completely avoiding `for` and `while` loops.
3. **Architecture:** Defense of the Hexagonal architecture, Structured Programming paradigms, and SOLID principles employed.

## Class Diagram

The architecture follows SOLID principles (ISP and DIP) and the Hexagonal Architecture pattern. Recent updates separate reading (`IDataHandler`) from writing (`IDataWriter`) and use a `DataIngestionService` to decouple dependencies. 

<div style="overflow-x: auto; white-space: nowrap;">
  <a href="docs/architecture/ClassDiagram.svg" target="_blank">
    <img src="docs/architecture/ClassDiagram.svg" width="2500" alt="Class Diagram (Click to open full size)">
  </a>
</div>

*Tip: You can scroll horizontally to view the entire diagram, or click on it to open it in full size in a new tab.*