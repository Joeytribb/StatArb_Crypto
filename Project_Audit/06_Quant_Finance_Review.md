# Quantitative Finance & Trading Review

## Would a Hedge Fund Care?
**No. This strategy would hemorrhage money in production.**

## 1. Market Microstructure & Execution Reality
* **Adverse Selection:** The backtest assumes a 0.02% "Maker Fee". If you are executing via limit orders to capture maker rebates/low fees, your orders are passive. When the spread blows out past $2.0\sigma$, it is often due to a structural break (e.g., toxic order flow hitting one asset). Your passive limit orders will only get filled when you are wrong (adverse selection). When mean-reversion is highly probable, the market moves away from you, and you get no fill.
* **Taker Fees Destroy Alpha:** If you use market orders to guarantee execution (Taker), Binance/Bybit taker fees are typically 0.04% to 0.07%. Paying this on *both* legs equates to ~0.10% total friction per round trip. For a 1m frequency mean-reversion strategy, this transaction cost barrier is impassable. The alpha mathematically evaporates.
* **Bid-Ask Bounce:** The backtest relies strictly on `Close` prices. In 1m data, simply crossing the spread to execute will incur slippage roughly equivalent to half the bid-ask spread. This is ignored entirely.

## 2. Invalid Capital Allocation
* **The Error:** `strategy_returns = positions * (0.5 * ret1 - 0.5 * ret2)`.
* **The Implication:** If BTC is trading at $50,000 and DOGE at $0.10, and you calculate a hedge ratio ($\beta$). A true stat-arb pairs trade requires dollar-neutrality or beta-neutrality. By arbitrarily allocating 50% capital to Asset A and 50% to Asset B, you are heavily exposed to directional market risk (Beta). You are not trading the synthetic stationary spread you modeled; you are trading a loosely correlated long/short basket with massive unhedged residual risk.

## 3. Ignored Risk Management
* **Unbounded Drawdowns:** Cointegration guarantees that the series will *eventually* revert, but it does not bound the maximum divergence. In crypto, spreads can gap infinitely (e.g., LUNA collapse). The system has no stop-loss mechanism, invalidation criteria, or time-based exits.
* **Sharpe Ratio Hallucination:** The Sharpe ratio calculation does not subtract the risk-free rate, and utilizes an invalid annualized volatility scalar for 1m data. 

## Verdict for Production
This codebase represents "paper alpha." The lack of bid-ask spread modeling, the in-sample pair selection, and the broken beta-weighting mean the reported historical returns are entirely fictitious. Deploying this code would result in immediate capital destruction.
