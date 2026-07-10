import pandas as pd
import numpy as np

def run_backtest(df, coin1, coin2, signals, hedge_ratio, fee_pct=0.001):
    """
    Simulates trades based on signals.
    fee_pct: 0.1% default spot fee for crypto.
    """
    print("Running backtest simulation...")
    
    # Align data
    prices1 = df[coin1]
    prices2 = df[coin2]
    
    # Calculate returns of the individual assets
    ret1 = prices1.pct_change()
    ret2 = prices2.pct_change()
    
    # The return of the spread depends on the position and hedge ratio.
    # If we are long the spread (+1), we buy 1 unit of coin1 and sell `hedge_ratio` units of coin2.
    # Actually, easier to calculate portfolio returns:
    # Portfolio value change = Position * (Ret1 - hedge_ratio * Ret2)  (approximate)
    
    # More precisely:
    # Let's allocate capital evenly (e.g., $1000 total -> $500 long, $500 short)
    # So if long spread: Long coin1, Short coin2.
    # Return = 0.5 * ret1 - 0.5 * ret2
    
    portfolio_ret = pd.Series(0.0, index=df.index)
    
    # Shift signals by 1 to avoid lookahead bias (trade is entered at the close of the signal bar, 
    # so return is realized on the NEXT bar)
    positions = signals.shift(1).fillna(0)
    
    # Calculate returns
    # Long spread: long coin1, short coin2
    # Short spread: short coin1, long coin2
    # Assuming capital is split 50/50
    strategy_returns = positions * (0.5 * ret1 - 0.5 * ret2)
    
    # Calculate transaction costs (only when position changes)
    trade_flags = positions.diff().abs() > 0
    strategy_returns[trade_flags] -= fee_pct
    
    # Cumulative returns
    cum_returns = (1 + strategy_returns).cumprod()
    
    # Calculate metrics
    total_return = cum_returns.iloc[-1] - 1 if len(cum_returns) > 0 else 0
    annualized_vol = strategy_returns.std() * np.sqrt(365 * 24 * 60) # 1m data annualized
    annualized_ret = (1 + total_return) ** ( (365*24*60) / len(df) ) - 1
    
    sharpe_ratio = annualized_ret / annualized_vol if annualized_vol > 0 else 0
    
    # Max Drawdown
    running_max = cum_returns.cummax()
    drawdown = (cum_returns - running_max) / running_max
    max_dd = drawdown.min()
    
    metrics = {
        'Total Return %': total_return * 100,
        'Annualized Return %': annualized_ret * 100,
        'Max Drawdown %': max_dd * 100,
        'Sharpe Ratio': sharpe_ratio,
        'Total Trades': trade_flags.sum()
    }
    
    return cum_returns, metrics
