import ccxt

mexc = ccxt.mexc()

def get_exchange_data():
    try:
        mexc_markets = mexc.load_markets()
        mexc_spot_markets = {symbol: market for symbol, market in mexc_markets.items() if market['spot'] and market['active']}
        mexc_tickers = mexc.fetch_tickers(list(mexc_spot_markets.keys()))
        return mexc_tickers
    except Exception as e:
        return None, "Error retrieving data from MEXC API: {}".format(e)
