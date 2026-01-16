import urllib.request
import json
import sys

def test_batch_api(api_key, symbols="AAPL,MSFT,TSLA"):
    url = f"https://www.alphavantage.co/query?function=BATCH_STOCK_QUOTES&symbols={symbols}&apikey={api_key}"
    
    print(f"Testing Alpha Vantage BATCH_STOCK_QUOTES for symbols: {symbols}...")
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                print("Response data:")
                print(json.dumps(data, indent=2))
            else:
                print(f"Error: {response.status}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test_batch.py YOUR_API_KEY [SYMBOLS]")
    else:
        api_key = sys.argv[1]
        symbols = sys.argv[2] if len(sys.argv) > 2 else "AAPL,MSFT,TSLA"
        test_batch_api(api_key, symbols)
