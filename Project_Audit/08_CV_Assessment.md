# CV Assessment

**Assume Target:** PhD Application to Oxford-Man Institute of Quantitative Finance, or Quant Researcher role at Tier-1 Firm (Jane Street, Citadel).

## Ratings (1-10)

* **Novelty: 2/10** 
  Standard pairs trading is thoroughly exhausted in literature. There is no unique data source, no novel econometric model (e.g., copulas, machine learning hybrid), and no high-frequency microstructure edge.
* **Difficulty: 3/10**
  Implementation of basic `statsmodels` functions and simple pandas operations.
* **Engineering Quality: 4/10**
  The codebase runs, but relies on painfully slow Python `for` loops for logic that must be vectorized. Lack of OOP architecture, missing type hinting, and hardcoded absolute paths demonstrate a lack of software engineering maturity.
* **Research Quality: 1/10**
  Data leakage via in-sample pair selection completely invalidates the research output.
* **Code Quality: 4/10**
  Readable, but brittle. Silent failure modes (synthetic data generation) are red flags for serious engineering teams.
* **Quantitative Rigor: 1/10**
  The mathematical disconnect between the calculated hedge ratio and the backtester's 50/50 capital allocation shows a fundamental misunderstanding of portfolio math.
* **Documentation: 3/10**
  The README is aesthetically pleasing but mathematically misleading (claiming Johansen test when it is absent).
* **Overall Portfolio Value: 2.5/10**

## Impact on Application
If an Oxford professor or a Citadel interviewer read this repository line-by-line, it would be heavily detrimental to the application. The explicit data leakage (Look-Ahead Bias) and the failure to properly size positions using the computed beta coefficient suggest that the candidate does not understand the underlying mathematics of the models they are calling from `statsmodels`.

**Recommendation:** Do not put this on your CV in its current state. It will trigger immediate rejection from elite technical reviewers.
