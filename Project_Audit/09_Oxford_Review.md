# Oxford Review Panel Notes

**Reviewer:** Professor of Quantitative Finance, Oxford-Man Institute
**Candidate Project:** Statistical Arbitrage & Cointegration: Market-Neutral Cryptographic Pairs

## Initial Impressions
"The abstract reads quite well—promising a rigorous econometric approach over naive correlation. However, upon reviewing the `main.py` and simulation architecture, I am deeply concerned by fundamental methodological errors."

## Interview Questions I Would Ask the Candidate:
1. **The Leakage Problem:** "I see in `main.py` that you pass your entire historical dataset to `find_cointegrated_pairs`, select the best pair, and then run your backtest on that exact same dataset. Can you explain how you intend to trade this in the real world without a time machine?"
2. **The Beta Disconnect:** "In `signals.py`, you correctly compute a rolling OLS hedge ratio to calculate the spread as $Y - \beta X$. But in `backtester.py`, you calculate returns as $0.5 \times Ret_Y - 0.5 \times Ret_X$. Why did you completely discard your beta coefficient when allocating capital?"
3. **The Microstructure Reality:** "You've assumed a 0.02% maker fee. Given the adverse selection inherent in limit orders during structural breaks, how realistic is it that your passive orders will be filled exactly at the `Close` price when the Z-score crosses your threshold?"
4. **Asymmetric Cointegration:** "The Engle-Granger test is order-dependent. Why did you only test `ts.coint(S1, S2)` and not `ts.coint(S2, S1)`? How many cointegrated relationships did you miss by relying on the alphabetical sorting of your DataFrame columns?"
5. **False Claims:** "Your README explicitly states you utilize the Johansen procedure. I ran a `grep` on your repository and found no implementation of it. Can you explain this discrepancy?"

## Final Verdict from the Panel
"The candidate shows enthusiasm and understands the *vocabulary* of quantitative finance, but lacks the rigorous mathematical discipline required for PhD-level research. The presence of look-ahead bias and mathematical inconsistencies in portfolio weighting indicates surface-level knowledge. Application rejected."
