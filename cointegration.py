import pandas as pd
import numpy as np
import statsmodels.tsa.stattools as ts

def find_cointegrated_pairs(dataframe):
    """
    Runs the Engle-Granger cointegration test on all possible pairs in the dataframe.
    Returns a list of tuples (coin1, coin2, p-value) sorted by p-value.
    """
    print("Scanning for cointegrated pairs...")
    n = dataframe.shape[1]
    score_matrix = np.zeros((n, n))
    pvalue_matrix = np.ones((n, n))
    keys = dataframe.columns
    pairs = []
    
    for i in range(n):
        for j in range(i+1, n):
            S1 = dataframe[keys[i]]
            S2 = dataframe[keys[j]]
            # Perform cointegration test
            result = ts.coint(S1, S2)
            score = result[0]
            pvalue = result[1]
            
            score_matrix[i, j] = score
            pvalue_matrix[i, j] = pvalue
            
            # If p-value < 0.05, it implies 95% confidence that they are cointegrated
            if pvalue < 0.05:
                pairs.append((keys[i], keys[j], pvalue))
                
    # Sort pairs by lowest p-value (most strongly cointegrated)
    pairs.sort(key=lambda x: x[2])
    print(f"Found {len(pairs)} cointegrated pairs.")
    return pairs

if __name__ == "__main__":
    # Test stub
    pass
