import ccxt

gateio = ccxt.gateio()

def get_exchange_data():
    try:
        gateio_markets = gateio.load_markets()
        gateio_spot_markets = {symbol: market for symbol, market in gateio_markets.items() if market['spot'] and market['active']}
        gateio_tickers = gateio.fetch_tickers(list(gateio_spot_markets.keys()))
        return gateio_tickers
    except Exception as e:
        return None, "Error retrieving data from Gateio API: {}".format(e)
