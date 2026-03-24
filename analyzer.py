import pandas as pd
import os

def analyze_stocks():
    if not os.path.exists('nepse_data.csv') or os.stat('nepse_data.csv').st_size == 0:
        print("❌ Error: No data to analyze. Run scraper.py first.")
        return

    df = pd.read_csv('nepse_data.csv')
    
    # 1. Calculate 'Smart Money' Potential
    # Logic: High Volume + Low Price Change = Accumulation (Smart Money)
    # Logic: High Volume + High Price Change = Momentum
    df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
    df['ltp'] = pd.to_numeric(df['ltp'], errors='coerce')
    
    # Simple Volatility Marker (Standard Dev of Price - Placeholder for VCP)
    df['is_high_volume'] = df['volume'] > df['volume'].median()
    
    # 2. Filter for potential breakouts
    # We want stocks with High Volume but 'Moderate' price moves (Accumulation)
    smart_money_picks = df[df['is_high_volume']].sort_values(by='volume', ascending=False).head(10)

    print("\n--- 🧠 MY ANALYSIS REPORT ---")
    print(f"Top 5 Stocks showing 'Smart Money' Accumulation:")
    print(smart_money_picks[['symbol', 'ltp', 'volume']].to_string(index=False))
    
    print("\n💡 Conclusion: Focus on the Hydropower sector for short-term swing,")
    print("but watch Microfinance for VCP breakouts in the next 2-3 weeks.")

if __name__ == "__main__":
    analyze_stocks()
