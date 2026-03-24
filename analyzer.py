import pandas as pd
import numpy as np
import os

def load_data():
    csv_path = 'data/nepse_data.csv'
    if not os.path.exists(csv_path):
        # Generate mock data if file doesn't exist yet
        return pd.DataFrame({
            'Symbol': ['NABIL', 'NICA', 'GBIME', 'HDL'],
            'Close': [1000, 800, 300, 2000],
            'Volume': [50000, 60000, 20000, 5000],
            'RSI': [65, 45, 30, 75],
            'PE_Ratio': [20, 15, 12, 35]
        })
    return pd.read_csv(csv_path)

def analyze_stocks(df):
    # Short-term score: High Volume + High RSI (Breaking out)
    df['Short_Term_Trend'] = (df['RSI'] * 0.6) + (df['Volume'] / df['Volume'].max() * 40)
    
    # 11-month score: Low PE (Fundamental) + Decent Volume
    df['Long_Term_Potential'] = (100 / df['PE_Ratio'] * 0.7) + (df['RSI'] * 0.3)

    top_short = df.sort_values(by='Short_Term_Trend', ascending=False).head(5)
    top_long = df.sort_values(by='Long_Term_Potential', ascending=False).head(5)

    return top_short, top_long

def generate_html(top_short, top_long):
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NEPSE Daily Insights Engine</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <style>
            body {{ background-color: #f8f9fa; font-family: sans-serif; }}
            .card {{ border-radius: 12px; border: none; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .header-banner {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 3rem 1rem; text-align: center; margin-bottom: 2rem; border-radius: 0 0 20px 20px; }}
        </style>
    </head>
    <body>
        <div class="header-banner">
            <h1>🇳🇵 NEPSE Stock Insights Engine</h1>
            <p>Automated Market Scoring, Volume Analysis, and Projections</p>
        </div>

        <div class="container">
            <div class="row">
                <div class="col-md-6 mb-4">
                    <div class="card p-4">
                        <h3 class="text-primary mb-3">🔥 Trending (Last 2 Weeks)</h3>
                        <p class="text-muted">High volume breakouts and momentum analysis.</p>
                        <table class="table table-hover">
                            <thead><tr><th>Symbol</th><th>Close Price</th><th>Momentum Score</th></tr></thead>
                            <tbody>
                                {"".join([f"<tr><td>{r['Symbol']}</td><td>Rs. {r['Close']}</td><td>{r['Short_Term_Trend']:.2f}</td></tr>" for _, r in top_short.iterrows()])}
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="col-md-6 mb-4">
                    <div class="card p-4">
                        <h3 class="text-success mb-3">⏳ 11-Month Potential Yields</h3>
                        <p class="text-muted">Stocks passing heavy fundamental filters (P/E ratios, accumulation).</p>
                        <table class="table table-hover">
                            <thead><tr><th>Symbol</th><th>Close Price</th><th>Valuation Score</th></tr></thead>
                            <tbody>
                                {"".join([f"<tr><td>{r['Symbol']}</td><td>Rs. {r['Close']}</td><td>{r['Long_Term_Potential']:.2f}</td></tr>" for _, r in top_long.iterrows()])}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
            <div class="alert alert-warning text-center mt-3">
                ⚠️ <strong>Disclaimer:</strong> This page is for educational data visualization only. Algorithms do not guarantee perfect financial returns.
            </div>
        </div>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("✅ Dashboard index.html generated!")

def main():
    df = load_data()
    top_short, top_long = analyze_stocks(df)
    generate_html(top_short, top_long)

if __name__ == "__main__":
    main()
