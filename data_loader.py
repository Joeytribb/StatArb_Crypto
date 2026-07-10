import pandas as pd
import glob
import os
import numpy as np

def load_data(data_dir, coins=None):
    """
    Loads 1m CSV data for specified coins, returning a dataframe of close prices.
    If no data is found, generates synthetic cointegrated data for demonstration.
    """
    print(f"Loading data from {data_dir}...")
    combined_closes = pd.DataFrame()
    
    if not coins:
        coins = ['BTC', 'ETH', 'SOL', 'BNB', 'ADA', 'XRP', 'DOT', 'DOGE', 'LTC', 'LINK']
        
    for coin in coins:
        patterns = [
            os.path.join(data_dir, f"{coin}USDT-1m.csv"),
            os.path.join(data_dir, f"{coin}-1m.csv"),
            os.path.join(data_dir, "1y", f"{coin}USDT-1m.csv")
        ]
        
        file_path = None
        for p in patterns:
            matched = glob.glob(p)
            if matched:
                file_path = matched[0]
                break
                
        if file_path:
            try:
                df = pd.read_csv(file_path, usecols=['timestamp', 'close'])
            except ValueError:
                df = pd.read_csv(file_path, usecols=['Timestamp', 'Close'])
                df.rename(columns={'Timestamp': 'timestamp', 'Close': 'close'}, inplace=True)
                
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
            df.set_index('datetime', inplace=True)
            df = df[~df.index.duplicated(keep='first')]
            combined_closes[coin] = df['close']
        else:
            print(f"Warning: Could not find 1m data for {coin}")
            
    if combined_closes.empty or combined_closes.shape[1] < 2:
        print("Generating synthetic cointegrated data for BTC and ETH...")
        n_samples = 100000
        np.random.seed(42)
        # Random walk for BTC
        btc = np.cumsum(np.random.randn(n_samples) * 5) + 50000
        # ETH is cointegrated with BTC (BTC * 0.05 + mean_reverting_noise)
        noise = np.zeros(n_samples)
        for i in range(1, n_samples):
            noise[i] = noise[i-1] * 0.95 + np.random.randn() * 10
        eth = (btc * 0.05) + noise
        
        dates = pd.date_range(end=pd.Timestamp.now(), periods=n_samples, freq='1min')
        combined_closes = pd.DataFrame({'BTC': btc, 'ETH': eth}, index=dates)

    combined_closes.ffill(limit=10, inplace=True)
    combined_closes.dropna(inplace=True)
    print(f"Loaded combined data with shape: {combined_closes.shape}")
    return combined_closes

if __name__ == "__main__":
    df = load_data(r"C:\Users\onepiece\Documents\_Garage\Ohhv2\data")
    print(df.head())
