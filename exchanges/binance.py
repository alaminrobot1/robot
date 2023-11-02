import ccxt

binance = ccxt.binance()

def get_exchange_tickers():
    try:
        binance_markets = binance.load_markets()
        binance_spot_markets = {symbol: market for symbol, market in binance_markets.items() if market['spot'] and market['active']}
        binance_tickers = binance.fetch_tickers(list(binance_spot_markets.keys()))
        return binance_tickers
    except Exception as e:
        return {"error": "Error retrieving ticker data from Binance API: {}".format(e)}

def get_order_book(symbol):
    try:
        order_book = binance.fetch_order_book(symbol)
        return order_book
    except Exception as e:
        return {"error": "Error retrieving order book data for symbol {} from Binance API: {}".format(symbol, e)}
