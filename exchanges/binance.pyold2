import ccxt

binance = ccxt.binance()

def get_exchange_data():
    try:
        binance_markets = binance.load_markets()
        binance_spot_markets = {symbol: market for symbol, market in binance_markets.items() if market['spot'] and market['active']}
        binance_tickers = binance.fetch_tickers(list(binance_spot_markets.keys()))
        return binance_tickers
    except Exception as e:
        return None, "Error retrieving data from Binance API: {}".format(e)
