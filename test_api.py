import urllib.request
import json
import sys

def test_api(api_key, symbol="AAPL"):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    
    print(f"Testing Alpha Vantage API for symbol: {symbol}...")
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                print("Response data:")
                print(json.dumps(data, indent=2))
                
                if "Global Quote" in data:
                    quote = data["Global Quote"]
                    print("\nParsed Data:")
                    print(f"Price: {quote.get('05. price')}")
                    print(f"Change: {quote.get('09. change')}")
                    print(f"Change Percent: {quote.get('10. change percent')}")
                elif "Note" in data:
                    print(f"\nAPI Note (likely rate limit): {data['Note']}")
                elif "Error Message" in data:
                    print(f"\nAPI Error: {data['Error Message']}")
                else:
                    print("\nUnexpected response structure.")
            else:
                print(f"Error: {response.status}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test_api.py YOUR_API_KEY [SYMBOL]")
    else:
        api_key = sys.argv[1]
        symbol = sys.argv[2] if len(sys.argv) > 2 else "AAPL"
        test_api(api_key, symbol)
