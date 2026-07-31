# System Documentation

This document serves as the formal specification for the codebase as it is currently implemented.

## `data_loader.py`

### `load_data(data_dir: str, coins: list = None) -> pd.DataFrame`
Reads 1-minute OHLCV CSV files from the specified directory and extracts the `Close` prices. 
* **Parameters:**
  * `data_dir`: Absolute path to the directory containing CSVs.
  * `coins`: List of ticker symbols to load. Defaults to a hardcoded top-10 list.
* **Returns:** A pandas DataFrame indexed by datetime, containing the aligned close prices for all successfully loaded coins.
* **Note:** If sufficient data cannot be found, it defaults to generating synthetic, pseudo-cointegrated data for BTC and ETH.

## `cointegration.py`

### `find_cointegrated_pairs(dataframe: pd.DataFrame) -> list`
Iterates through all possible unique pairs of columns in the dataframe and applies the Engle-Granger augmented Dickey-Fuller test.
* **Parameters:**
  * `dataframe`: DataFrame of asset prices.
* **Returns:** A list of tuples in the format `(coin_A, coin_B, p_value)`, sorted in ascending order of the p-value. Only pairs with $p < 0.05$ are returned.

## `signals.py`

### `calculate_spread_and_zscore(df: pd.DataFrame, coin1: str, coin2: str, window: int = 1000) -> tuple[pd.DataFrame, pd.Series]`
Computes a dynamic hedge ratio using Rolling Ordinary Least Squares and derives the normalized Z-score.
* **Parameters:**
  * `df`: DataFrame containing price histories.
  * `coin1`: Ticker of the dependent variable (Y).
  * `coin2`: Ticker of the independent variable (X).
  * `window`: The lookback period for the Rolling OLS and Z-score normalization.
* **Returns:** 
  * A DataFrame containing the raw `spread` and normalized `zscore`.
  * A Series representing the dynamic `hedge_ratio`.

### `generate_signals(zscore: pd.Series, entry_threshold: float = 2.0, exit_threshold: float = 0.0) -> pd.Series`
Converts continuous Z-scores into discrete trading states using a state-machine.
* **Parameters:**
  * `zscore`: Time series of the normalized spread.
  * `entry_threshold`: Z-score absolute value required to open a position.
  * `exit_threshold`: Z-score absolute value required to close a position.
* **Returns:** A Series of integer states (-1 for short spread, 1 for long spread, 0 for flat).

## `backtester.py`

### `run_backtest(df: pd.DataFrame, coin1: str, coin2: str, signals: pd.Series, hedge_ratio: pd.Series, fee_pct: float = 0.001) -> tuple[pd.Series, dict]`
Simulates historical performance of the generated signals.
* **Parameters:**
  * `df`: Price dataframe.
  * `coin1`: Ticker 1.
  * `coin2`: Ticker 2.
  * `signals`: The position state array.
  * `hedge_ratio`: The dynamic beta (Note: currently unused in internal logic).
  * `fee_pct`: Friction applied upon position changes.
* **Returns:**
  * A Series of cumulative portfolio returns.
  * A dictionary of performance metrics (Total Return, Annualized Return, Max Drawdown, Sharpe, Trades).
