# Algorithmic Trading Backtester

## Objective
A vectorized backtesting engine for evaluating algorithmic trading strategies using historical market data.

## Project Structure
- `src/`: Core implementation containing data loaders, strategies, backtesting engine, and performance metrics.
- `docs/architecture/`: UML diagrams and use cases defining the system architecture.
- `data/`: Directory for historical market data (Parquet / HDF5 format).
- `notebooks/`: Interactive documentation and visual results.

## Class Diagram

The architecture follows SOLID principles (ISP and DIP) and the Hexagonal Architecture pattern. Recent updates separate reading (`IDataHandler`) from writing (`IDataWriter`) and use a `DataIngestionService` to decouple dependencies. 

<div style="overflow-x: auto; white-space: nowrap;">
  <a href="docs/architecture/ClassDiagram.svg" target="_blank">
    <img src="docs/architecture/ClassDiagram.svg" width="2500" alt="Class Diagram (Click to open full size)">
  </a>
</div>

*Tip: You can scroll horizontally to view the entire diagram, or click on it to open it in full size in a new tab.*