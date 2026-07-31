# Refactoring Roadmap

To elevate this codebase from a flawed script to an institutional-grade research repository, execute the following prioritized roadmap.

## 🔴 Critical Priority (Do This Immediately)
1. **Eliminate Look-Ahead Bias (Data Leakage):** 
   - Refactor `main.py` to implement a Walk-Forward Validation pipeline. 
   - Window 1: Train (Find cointegrated pairs, estimate initial hedge ratio). 
   - Window 2: Test (Generate signals and backtest on unseen data).
2. **Fix Backtester Position Sizing:**
   - Rewrite `backtester.py` to utilize the `hedge_ratio`. 
   - If Long Spread: Allocate capital proportional to $1$ unit of Y and $\beta$ units of X (adjusted for price). 
   - Do not use `0.5 * ret1 - 0.5 * ret2`.

## 🟠 High Priority (Technical & Quant Debt)
3. **Fix Transaction Cost Logic:**
   - Apply fees to **both legs** of the trade in `backtester.py`.
   - Ensure fees are multiplied by the size of the position change (e.g., flipping from -1 to 1 means paying fees on a size of 2, on both legs).
4. **Implement Symmetric Engle-Granger:**
   - In `cointegration.py`, modify the loops to test both $Y \sim X$ and $X \sim Y$. Select the direction that yields the lowest ADF p-value.
5. **Remove Synthetic Data Fallback:**
   - Delete the synthetic data generation in `data_loader.py`. If data is missing, `raise FileNotFoundError`. Silent failures ruin research.

## 🟡 Medium Priority (Engineering Debt)
6. **Vectorize Signal Generation:**
   - The `for` loop in `signals.py:61-79` is a massive bottleneck. Refactor using `numpy.select`, `pandas.cut`, or compile the loop using `@njit` from `numba`.
7. **Use Johansen Test:**
   - Make good on the README's promise. Implement `statsmodels.tsa.vector_ar.vecm.coint_johansen` to allow for multi-asset baskets (e.g., trading BTC vs an ETH/SOL/BNB basket).
8. **Configuration Management:**
   - Remove hardcoded paths and magic numbers. Implement a `config.yaml` or use `argparse` for hyperparameter injection (window size, z-score thresholds, fees).

## 🟢 Low Priority (Quick Wins)
9. **Fix Sharpe Ratio Calculation:**
   - Subtract a risk-free rate.
   - Stop annualizing 1m data using $\sqrt{365 \times 24 \times 60}$. Aggregate returns to daily before computing standard deviation, or apply an autocorrelation adjustment.
10. **Clean Up Error Handling:**
    - Explicitly format column names to lowercase in `data_loader.py` instead of relying on `try/except ValueError`.
