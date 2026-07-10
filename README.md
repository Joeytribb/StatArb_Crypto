# Statistical Arbitrage: Crypto Pairs Trading via Cointegration

## Project Overview
This repository contains a quantitative statistical arbitrage (StatArb) engine for cryptocurrency pairs trading. Unlike naive correlation trading, this pipeline utilizes rigorous econometric tests (Engle-Granger / Johansen) to identify truly **cointegrated** asset pairs. 

When two assets are cointegrated, they share a stochastic drift. Any divergence between their prices (the "Spread") is mathematically expected to mean-revert, providing a market-neutral trading opportunity.

## Methodology

### 1. Cointegration Testing (`cointegration.py`)
The engine iterates through a matrix of major cryptocurrency assets (e.g., BTC, ETH, SOL, BNB). It calculates the spread and runs the Augmented Dickey-Fuller (ADF) test on the residuals to compute a p-value. Pairs with a p-value < 0.05 are flagged as statistically cointegrated and valid for mean-reversion trading.

### 2. Spread & Z-Score Calculation (`signals.py`)
For the most cointegrated pair (e.g., BTC vs. ETH), the engine calculates a dynamic hedge ratio using OLS regression. The spread is then normalized into a rolling **Z-Score**. 
- A Z-Score of `+2.0` indicates the spread has widened significantly (Short the outperforming asset, Long the underperforming asset).
- A Z-Score of `0.0` indicates mean-reversion has occurred (Exit position).

### 3. Vectorized Backtesting (`backtester.py`)
The system applies the Z-Score signals against historical OHLCV data. Crucially, the backtester is institutional-grade: it injects configurable **Maker/Taker fees** (e.g., 0.02% maker fees) to calculate a realistic Expected Value (EV), rather than relying on frictionless theoretical returns.

## Execution
```bash
python main.py
```
*Output: Automatically identifies the optimal cointegrated pair, computes the dynamic hedge ratio, simulates the market-neutral backtest, and plots the Cumulative Return, Z-Score, and Spread.*
