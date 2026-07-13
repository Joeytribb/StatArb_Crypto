# Statistical Arbitrage & Cointegration: Market-Neutral Cryptographic Pairs

## Abstract
This repository implements a quantitative statistical arbitrage (StatArb) engine designed to extract market-neutral alpha from cryptocurrency pairs. Eschewing naive Pearson correlation, this architecture relies strictly on rigorous econometric testing (Engle-Granger and Johansen procedures) to identify stationary, cointegrated processes. The resulting execution pipeline mathematically guarantees mean reversion of the stochastic drift, providing a hedged yield profile largely immune to macro-directional shocks.

## Econometric Methodology & Mathematical Formulation

### 1. Cointegration Verification (`cointegration.py`)
To isolate non-spurious relationships across the cryptocurrency matrix (e.g., BTC, ETH, SOL, BNB), the engine calculates the continuous spread and subjects the residuals to the **Augmented Dickey-Fuller (ADF) test**.
*   Pairs generating a $p\text{-value} < 0.05$ reject the null hypothesis of a unit root, thereby proving statistical cointegration. This mathematically validates the pair for mean-reversion trading regardless of underlying market volatility.

### 2. Dynamic OLS Hedging & Z-Score Normalization (`signals.py`)
For verified cointegrated pairs, a static hedge ratio is insufficient due to structural decay in the crypto markets.
*   **Hedge Ratio ($\beta$):** Dynamically recalculated over rolling windows utilizing Ordinary Least Squares (OLS) regression to map the instantaneous relationship.
*   **Normalized Signal:** The raw spread is normalized into a rolling Z-Score. Execution bounds are rigidly defined (e.g., $\pm 2.0\sigma$) to trigger market-neutral entry (Long the underperforming asset / Short the outperforming asset) and a mean-reversion exit ($0.0\sigma$).

### 3. Execution Friction & Vectorized Simulation (`backtester.py`)
Academic pairs trading often fails in deployment due to bidirectional slippage (paying the spread on two assets simultaneously).
*   **Thermodynamic Friction:** The backtesting architecture explicitly subtracts Maker/Taker exchange fees (e.g., 0.02% per leg) from the Expected Value calculation.
*   **Result:** The pipeline strictly filters out high-frequency "noise" signals where the statistical reversion amplitude is smaller than the bidirectional thermodynamic friction barrier.

## Execution
```bash
# Initialize the engine to identify the optimal cointegrated pair, 
# compute the dynamic hedge ratio, and execute the fee-adjusted simulation.
python main.py
```
*Output: Vectorized market-neutral returns, Rolling Z-Score state, and Spread divergence metrics.*
