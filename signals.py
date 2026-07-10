import pandas as pd
import numpy as np
import statsmodels.api as sm

def calculate_spread_and_zscore(df, coin1, coin2, window=1000):
    """
    Calculates the spread using a rolling linear regression to find the hedge ratio,
    and normalizes the spread to a Z-score over the given window.
    """
    print(f"Calculating spread and z-score for {coin1} vs {coin2}...")
    
    # We use a rolling window to calculate the dynamic hedge ratio
    # To keep it simple and fast for 1m data, we can calculate a static hedge ratio
    # over a training period, or use a rolling window. Here we use rolling.
    
    y = df[coin1]
    x = df[coin2]
    
    from statsmodels.regression.rolling import RollingOLS
    
    x_with_const = sm.add_constant(x)
    # Calculate a dynamic hedge ratio using a rolling window
    model = RollingOLS(y, x_with_const, window=window).fit()
    
    # The hedge ratio is now a time series. We forward fill any NaNs from the initial window.
    hedge_ratio = model.params[coin2].ffill().fillna(1.0) 
    
    spread = y - hedge_ratio * x
    
    # Calculate rolling Z-score
    rolling_mean = spread.rolling(window=window).mean()
    rolling_std = spread.rolling(window=window).std()
    zscore = (spread - rolling_mean) / rolling_std
    
    result = pd.DataFrame(index=df.index)
    result['spread'] = spread
    result['zscore'] = zscore
    return result, hedge_ratio

def generate_signals(zscore, entry_threshold=2.0, exit_threshold=0.0):
    """
    Generates trading signals based on z-score thresholds.
    +1 means LONG the spread (Buy coin1, Sell coin2)
    -1 means SHORT the spread (Sell coin1, Buy coin2)
    0 means FLAT
    """
    signals = pd.Series(0, index=zscore.index)
    position = 0
    
    # Vectorized signal generation
    # Go short spread if z-score > entry_threshold
    # Go long spread if z-score < -entry_threshold
    # Exit if z-score crosses exit_threshold
    
    # Note: A full vectorized backtest with state is complex, so we approximate or use a loop.
    # For a robust simulation, we iterate:
    sig_array = np.zeros(len(zscore))
    z_array = zscore.values
    
    current_pos = 0
    for i in range(len(z_array)):
        z = z_array[i]
        if np.isnan(z):
            sig_array[i] = 0
            continue
            
        if current_pos == 0:
            if z > entry_threshold:
                current_pos = -1
            elif z < -entry_threshold:
                current_pos = 1
        elif current_pos == 1:
            if z >= exit_threshold:
                current_pos = 0
        elif current_pos == -1:
            if z <= -exit_threshold:
                current_pos = 0
                
        sig_array[i] = current_pos
        
    return pd.Series(sig_array, index=zscore.index)
