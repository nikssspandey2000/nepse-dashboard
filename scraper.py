import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_nepse_data():
    # Target: ShareSansar (Reliable for Today's Price)
    url = "https://www.sharesansar.com/today-share-price"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print("🔍 Accessing Live NEPSE Data...")
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ Site blocked access (Status: {response.status_code})")
            return None

        # Extracting the table
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'headertfixed'})
        
        # Read the table into Pandas
        df = pd.read_html(str(table))[0]
        
        # Clean columns (ShareSansar often has extra spaces)
        df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
        
        # Keep only useful columns for Analysis
        # We need Symbol, LTP, Volume, and % Change
        essential_cols = ['symbol', 'ltp', 'volume', 'conf._index']
        df = df[[c for c in df.columns if any(e in c for e in essential_cols)]]
        
        df.to_csv('nepse_data.csv', index=False)
        print(f"✅ Scraped {len(df)} stocks successfully.")
        return df

    except Exception as e:
        print(f"⚠️ Scraping Error: {e}")
        return None

if __name__ == "__main__":
    get_nepse_data()
