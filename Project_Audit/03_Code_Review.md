# Code Review

The codebase exhibits severe structural flaws, silent failures, and logical inconsistencies that disqualify it from production use.

## Critical Issues & Bugs

### 1. Broken Hedge Ratio in Backtester (Fatal Logical Flaw)
* **Location:** `backtester.py:39` -> `strategy_returns = positions * (0.5 * ret1 - 0.5 * ret2)`
* **Issue:** The `backtester.py` accepts `hedge_ratio` as an argument but **never uses it**. It explicitly hardcodes a `50/50` capital allocation. If the OLS regression calculates a beta of `0.05`, you are trading a spread of $Y - 0.05X$. However, the backtester evaluates the PnL as if you traded $0.5Y - 0.5X$. The strategy generated signals for one asset combination, but simulated returns for a completely different one. This renders the entire backtest mathematically invalid.

### 2. Flawed Transaction Cost Logic
* **Location:** `backtester.py:42-43` -> `trade_flags = positions.diff().abs() > 0`
* **Issue:** 
  1. A position flipping from `-1` to `+1` represents a `diff().abs()` of `2`. This requires closing a short and opening a long (double the volume), but the code subtracts the fee (`fee_pct`) only once.
  2. A pairs trade involves trading *two separate assets*. The fee should be applied to both legs of the trade. The current implementation effectively understates slippage/fees by a factor of 2 to 4.

### 3. Asymmetric Cointegration Testing
* **Location:** `cointegration.py:22` -> `result = ts.coint(S1, S2)`
* **Issue:** The Engle-Granger test is order-dependent. Regressing Y on X yields different residuals than X on Y. The code only checks one arbitrary direction (alphabetical order of columns) and ignores the inverse. This means you might miss highly cointegrated pairs simply due to column ordering.

### 4. Synthetic Data Obfuscation
* **Location:** `data_loader.py:45-58`
* **Issue:** If the hardcoded data directory (`C:\Users\onepiece\Documents\_Garage\Ohhv2\data`) is missing, the code silently generates synthetic data and proceeds. While there's a print statement, this is a terrible practice. A missing data pipeline should raise a `FileNotFoundError`, not fabricate perfect normally-distributed cointegrated data that will guarantee a flawless (but fake) backtest.

## Code Smells & Inefficiencies

### 1. Hardcoded Paths and Magic Numbers
* **Location:** `main.py:9`, `data_loader.py:66`
* **Issue:** Absolute paths specific to a local Windows machine are hardcoded. This prevents reproducibility.
* **Location:** `main.py:33`, `main.py:38`, `signals.py:40`
* **Issue:** Magic numbers (`1440` window, `0.0002` fee, `2.0` z-score) are scattered without a centralized config file.

### 2. Extreme Inefficiency in Signal Generation
* **Location:** `signals.py:61-79`
* **Issue:** The state machine is implemented as a pure Python `for` loop iterating over NumPy arrays (`for i in range(len(z_array)):`). For 1-minute data across multiple years, this is agonizingly slow. This should be refactored using Numba (`@njit`), Cython, or optimized Pandas vectorization techniques.

### 3. Dangerous Data Imputation
* **Location:** `signals.py:26` -> `hedge_ratio = model.params[coin2].ffill().fillna(1.0)`
* **Issue:** Assuming a default hedge ratio of `1.0` during the initial rolling window phase is mathematically ungrounded. If the true beta is `0.01` (e.g., BTC vs DOGE), forcing it to `1.0` will create massive, artificial spikes in the spread, triggering spurious trades.

### 4. Poor Error Handling
* **Location:** `data_loader.py:32-36`
* **Issue:** Blindly catching `ValueError` to try capitalized column names is brittle. It should explicitly normalize headers via `df.columns = df.columns.str.lower()`.
