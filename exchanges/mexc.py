import ccxt

mexc = ccxt.mexc()

def get_exchange_tickers():
    try:
        mexc_markets = mexc.load_markets()
        mexc_spot_markets = {symbol: market for symbol, market in mexc_markets.items() if market['spot'] and market['active']}
        mexc_tickers = mexc.fetch_tickers(list(mexc_spot_markets.keys()))
        return mexc_tickers
    except Exception as e:
        return {"error": "Error retrieving ticker data from MEXC API: {}".format(e)}

def get_order_book(symbol):
    try:
        order_book = mexc.fetch_order_book(symbol)
        return order_book
    except Exception as e:
        return {"error": "Error retrieving order book data for symbol {} from MEXC API: {}".format(symbol, e)}
