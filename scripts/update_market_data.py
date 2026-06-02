import yfinance as yf
import pandas as pd
import datetime
import os

# 模擬全市場標的：涵蓋台灣前 50 大權值股以及熱門 ETF，共計約 60 檔標的。
# 實務上可透過台灣證券交易所公開資料抓取所有 1700 檔股票代碼，但在本機運行為了避免 yfinance IP 封鎖與速度問題，取 60 檔做示範。
TICKERS = [
    # 大型權值股
    "2330.TW", "2317.TW", "2454.TW", "2308.TW", "2382.TW",
    "2881.TW", "2882.TW", "2891.TW", "2886.TW", "2884.TW",
    "2002.TW", "1301.TW", "1303.TW", "1216.TW", "2412.TW",
    "3008.TW", "3231.TW", "2301.TW", "2357.TW", "2303.TW",
    "3045.TW", "2379.TW", "2892.TW", "2885.TW", "5871.TW",
    "2890.TW", "5880.TW", "2883.TW", "2887.TW", "2880.TW",
    "3711.TW", "2603.TW", "2609.TW", "2615.TW", "2912.TW",
    # 熱門 ETF
    "0050.TW", "0056.TW", "00878.TW", "00713.TW", "00919.TW",
    "00929.TW", "006208.TW", "00679B.TWO", "00687B.TWO", "00719B.TWO",
    # 美股代表作分散
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "SPY", "QQQ"
]

def update_data(years=5):
    print(f"開始抓取市場數據 (標的數量: {len(TICKERS)})...")
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=years * 365)
    
    # yfinance 下載
    df = yf.download(TICKERS, start=start_date, end=end_date)['Close']
    
    # 處理缺失值
    # 對於上市未滿 5 年的標的，如果直接 dropna 會把所有天數刪光
    # 我們改用前向填充，如果真的全部是 NaN 則捨棄
    df = df.ffill().bfill()
    df = df.dropna(axis=1, how='all')
    
    # 存檔
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, 'market_data.csv')
    
    df.to_csv(file_path)
    print(f"資料更新完成！已儲存至 {file_path}")

if __name__ == "__main__":
    update_data()
