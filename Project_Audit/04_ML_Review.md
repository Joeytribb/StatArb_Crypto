# Machine Learning & Econometrics Review

## 1. Massive Data Leakage (Look-Ahead Bias in Pair Selection)
This is the most fatal flaw in the repository. 
* **The Crime:** In `main.py`, the code passes the *entire* historical dataset into `find_cointegrated_pairs()` (Line 21). It finds the pair with the lowest p-value over the entire history. It then passes that *same dataset* into `run_backtest()` (Line 38) to evaluate performance.
* **Why it fails:** You are using future information to select your assets. In a real-world scenario in 2023, you do not know which pair will have been cointegrated over the 2023-2024 period. By selecting the pair with the best in-sample Engle-Granger p-value and trading it in-sample, your backtest is structurally compromised and your Sharpe ratio is a hallucination.
* **The Fix:** Walk-Forward Analysis. You must split the data. For example: Use Month 1 to find cointegrated pairs and calculate initial hedge ratios. Trade those pairs in Month 2. Re-evaluate at the end of Month 2.

## 2. Naive Econometric Assumptions
* **Rolling OLS:** The codebase relies on `RollingOLS` for the hedge ratio. OLS requires the independent variable to be deterministic (or strictly exogenous), which is false for crypto prices (both legs are stochastic). The correct methodology is **Total Least Squares (TLS)** or **Orthogonal Regression**, which minimizes perpendicular distance, accounting for variance in both X and Y.
* **Gaussian Spread Assumption:** The signal generation normalizes the spread into a Z-score, explicitly assuming the spread's residuals follow a Normal distribution. Financial time series are notorious for fat tails (leptokurtic). A $\pm2\sigma$ event in a Gaussian world is rare; in crypto, structural breaks will cause $10\sigma$ blowouts. The code has no stop-loss or regime-change detection to handle this.

## 3. Disconnect Between Price Spread and Return Backtest
* In `signals.py`, the spread is calculated on absolute prices: $Spread_t = P_{1,t} - \beta P_{2,t}$.
* In `backtester.py`, the returns are calculated using percentage changes: $Ret_t = 0.5 \times r_{1,t} - 0.5 \times r_{2,t}$.
* **The Problem:** A price-based spread implies a fixed nominal dollar allocation (e.g., Buy 1 BTC, Sell $\beta$ ETH). A percentage-based return implies continuous rebalancing to a specific weighting. The backtester uses a 50/50 weight, completely divorcing the simulation from the statistical logic that generated the signals.

## 4. Missing Statistical Rigor
* **No Multiple Testing Correction:** The cointegration scanner tests $N(N-1)/2$ pairs. At a 95% confidence interval ($p < 0.05$), testing 45 pairs guarantees several false positives purely by random chance. The codebase fails to implement the Bonferroni correction or False Discovery Rate (FDR) adjustments.
* **Annualization of High-Frequency Data:** `annualized_vol = strategy_returns.std() * np.sqrt(365 * 24 * 60)`. Multiplying 1m variance by the square root of time assumes returns are independently and identically distributed (i.i.d.). 1m crypto returns exhibit extreme autocorrelation and volatility clustering (GARCH effects). This annualization formula wildly distorts risk metrics.
