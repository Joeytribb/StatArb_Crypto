import os
import matplotlib.pyplot as plt
from data_loader import load_data
from cointegration import find_cointegrated_pairs
from signals import calculate_spread_and_zscore, generate_signals
from backtester import run_backtest

def main():
    data_dir = r"C:\Users\onepiece\Documents\_Garage\Ohhv2\data"
    
    # 1. Load Data
    # To keep the test fast, we'll pick a few major coins
    coins = ['BTC', 'ETH', 'SOL', 'BNB', 'ADA', 'XRP', 'DOGE', 'LINK']
    df = load_data(data_dir, coins)
    
    if df.empty or df.shape[1] < 2:
        print("Not enough data loaded to run pairs trading backtest.")
        return
        
    # 2. Find Cointegrated Pairs
    pairs = find_cointegrated_pairs(df)
    
    if not pairs:
        print("No cointegrated pairs found with p < 0.05.")
        return
        
    best_pair = pairs[0]
    coin1, coin2, pvalue = best_pair
    print(f"\nBest Pair: {coin1} and {coin2} (p-value: {pvalue:.5f})")
    
    # 3. Calculate Spread & Signals
    # Use a rolling window of 1440 minutes (1 day) for z-score and dynamic hedge ratio
    window = 1440 
    zscore_df, hedge_ratio = calculate_spread_and_zscore(df, coin1, coin2, window=window)
    signals = generate_signals(zscore_df['zscore'], entry_threshold=2.0, exit_threshold=0.5)
    
    # 4. Backtest (Using Maker Fees: 0.02%)
    cum_returns, metrics = run_backtest(df, coin1, coin2, signals, hedge_ratio, fee_pct=0.0002)
    
    # 5. Output Results
    print("\n--- Backtest Results ---")
    for k, v in metrics.items():
        print(f"{k}: {v:.2f}")
        
    # 6. Plotting
    plt.figure(figsize=(14, 10))
    
    # Subplot 1: Cumulative Returns
    plt.subplot(3, 1, 1)
    plt.plot(cum_returns.index, cum_returns.values, label='Strategy Cumulative Return', color='green')
    plt.title(f'Statistical Arbitrage Backtest: {coin1} vs {coin2}')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.grid(True)
    
    # Subplot 2: Z-Score
    plt.subplot(3, 1, 2)
    plt.plot(zscore_df.index, zscore_df['zscore'], label='Z-Score', color='blue')
    plt.axhline(2.0, color='red', linestyle='--', label='Short Spread Entry')
    plt.axhline(-2.0, color='green', linestyle='--', label='Long Spread Entry')
    plt.axhline(0.0, color='black', linestyle='--', label='Exit')
    plt.ylabel('Z-Score')
    plt.legend()
    plt.grid(True)
    
    # Subplot 3: Spread
    plt.subplot(3, 1, 3)
    plt.plot(zscore_df.index, zscore_df['spread'], label='Spread', color='purple')
    plt.ylabel('Spread Value')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plot_path = os.path.join(os.path.dirname(__file__), 'backtest_results.png')
    plt.savefig(plot_path)
    print(f"\nSaved plot to {plot_path}")

if __name__ == "__main__":
    main()
