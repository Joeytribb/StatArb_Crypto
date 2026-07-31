# Project Summary

## Project Objective
The repository implements a statistical arbitrage (StatArb) engine designed to extract alpha from cryptocurrency pairs via mean-reversion. It aims to identify cointegrated pairs of cryptocurrencies and trade the divergence of their spread using dynamic hedging.

## Problem Formulation
Financial time series are largely non-stationary. However, a linear combination of two non-stationary time series might be stationary (cointegrated). By modeling the spread between two cointegrated cryptocurrencies, the strategy aims to profit from temporary deviations from their historical equilibrium, betting on mean-reversion.

## Input Data
- **Source format:** 1-minute resolution CSV files containing OHLCV data.
- **Variables used:** Only `close` prices are extracted and processed.
- **Fallback:** If data is missing, the engine generates synthetic random-walk data for BTC and a cointegrated synthetic ETH series.

## Output
- **Console Metrics:** Prints the most cointegrated pair, p-value, and backtest performance metrics (Total Return, Annualized Return, Max Drawdown, Sharpe Ratio, Total Trades).
- **Visualization:** A 3-subplot PNG image (`backtest_results.png`) showing cumulative returns, rolling Z-score with trade entry/exit thresholds, and the raw spread value.

## Pipeline & Algorithms
1. **Data Loading (`data_loader.py`):** Ingests 1m close prices and aligns them onto a common datetime index.
2. **Cointegration Verification (`cointegration.py`):** Exhaustively scans all pair permutations using the **Engle-Granger Two-Step Method** (via Augmented Dickey-Fuller test on residuals) to find stationary spreads.
3. **Dynamic Hedging (`signals.py`):** Calculates a rolling Ordinary Least Squares (OLS) regression to dynamically update the hedge ratio (Beta). Computes the spread and normalizes it into a rolling Z-score.
4. **Signal Generation (`signals.py`):** Generates discrete states (-1, 0, 1) based on standard deviation thresholds (e.g., enter at $\pm2.0\sigma$, exit at $0.5\sigma$).
5. **Vectorized Simulation (`backtester.py`):** Simulates returns using the generated signals and applies a fixed transaction fee per trade.

## Dependencies & Configuration
- **Dependencies:** `pandas`, `numpy`, `statsmodels`, `matplotlib`.
- **Configuration:** Hardcoded paths to local directories, hardcoded asset lists, and hardcoded strategy parameters (e.g., 1440-minute window, $\pm2.0$ Z-score entry).

## Deployment
The project currently functions as a standalone local script (`main.py`) running sequential historical analysis. There is no live execution module, order routing, or production deployment containerization.
