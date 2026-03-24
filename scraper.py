import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

# Define URLs to scrape (You can add up to 10 here)
SITES = {
    "ShareSansar": "https://www.sharesansar.com/today-share-price",
    # "MeroLagani": "https://merolagani.com/LatestMarket.aspx",
    # "NepseAlpha": "https://nepsealpha.com/trading-board",
}

def scrape_share_sansar():
    """
    Example scraper for ShareSansar Today's Share Price table.
    """
    try:
        response = requests.get(SITES["ShareSansar"], timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Finding the Today's Price Table
        table = soup.find('table', {'id': 'headertp'})
        
        if not table:
            return []

        rows = table.find_all('tr')[1:] # Skip header
        data = []
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 5:
                # Standardizing columns
                symbol = cols[1].text.strip()
                close_price = float(cols[6].text.replace(',', '').strip())
                volume = float(cols[8].text.replace(',', '').strip())
                high = float(cols[4].text.replace(',', '').strip())
                low = float(cols[5].text.replace(',', '').strip())
                
                data.append({
                    'Date': datetime.now().strftime('%Y-%m-%d'),
                    'Symbol': symbol,
                    'Close': close_price,
                    'Volume': volume,
                    'High': high,
                    'Low': low,
                    'RSI': 50.0, # Placeholder for Technicals
                    'PE_Ratio': 15.0 # Placeholder for Fundamentals
                })
        return data
    except Exception as e:
        print(f"Error scraping ShareSansar: {e}")
        return []

def main():
    print("🚀 Starting NEPSE data collection...")
    all_data = []
    
    # 1. Collect data from various scrapers
    all_data.extend(scrape_share_sansar())
    # all_data.extend(scrape_merolagani()) # Add more scrapers here!

    if not all_data:
        print("❌ No data collected.")
        return

    df_new = pd.DataFrame(all_data)
    
    # 2. Append to master CSV
    os.makedirs('data', exist_ok=True)
    csv_path = 'data/nepse_data.csv'
    
    if os.path.exists(csv_path):
        df_old = pd.read_csv(csv_path)
        df_combined = pd.concat([df_old, df_new]).drop_duplicates(subset=['Date', 'Symbol'])
    else:
        df_combined = df_new

    df_combined.to_csv(csv_path, index=False)
    print(f"✅ Successfully stored data for {len(df_new)} stocks in CSV.")

if __name__ == "__main__":
    main()
