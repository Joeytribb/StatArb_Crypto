# Academic & Research Critique

## Is this Novel?
**No.** The methodology implemented in this repository is identical to foundational pairs trading research published over two decades ago (e.g., *Gatev, Goetzmann, Rouwenhorst 2006*). Furthermore, applying Engle-Granger cointegration to crypto pairs is standard practice in undergraduate finance courses. There is zero algorithmic or mathematical novelty in this codebase.

## False Claims in the README
The `README.md` explicitly claims:
> *"this architecture relies strictly on rigorous econometric testing (Engle-Granger and Johansen procedures)"*

**Critique:** This is empirically false. The codebase only implements `statsmodels.tsa.stattools.coint`, which is the Engle-Granger two-step method. The Johansen test is entirely absent from the repository. Misrepresenting algorithms in an abstract is a severe violation of academic integrity.

## Missing Experiments & Ablations
If this were submitted as a research paper to the *Journal of Financial Data Science* or *Quantitative Finance*, it would be desk-rejected for the following missing analyses:
1. **Out-of-Sample Performance:** As noted in the ML review, the results are entirely in-sample.
2. **Transaction Cost Sensitivity Analysis:** The results rely on a hardcoded 0.02% maker fee. There is no ablation showing how alpha decays as a function of execution slippage or taker fees.
3. **Cointegration Decay Rate:** How long does a crypto pair remain cointegrated? The paper provides no half-life analysis of the mean-reverting spread (e.g., using the Ornstein-Uhlenbeck process).
4. **Impact of Rolling Window Size:** The rolling window is arbitrarily set to 1440. No sensitivity analysis is provided to justify this parameter, leaving the system highly vulnerable to curve-fitting.

## Academic Verdict
The repository lacks the scientific rigor required for publication. It functions as a rudimentary tutorial script rather than a rigorous research artifact. To elevate this to publication quality, the author must implement Walk-Forward Validation, Johansen Cointegration (for $N > 2$ assets), Half-Life of mean-reversion analysis, and proper modeling of high-frequency market microstructure frictions.
