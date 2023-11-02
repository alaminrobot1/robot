import ccxt

gateio = ccxt.gateio()

def get_exchange_tickers():
    try:
        gateio_markets = gateio.load_markets()
        gateio_spot_markets = {symbol: market for symbol, market in gateio_markets.items() if market['spot'] and market['active']}
        gateio_tickers = gateio.fetch_tickers(list(gateio_spot_markets.keys()))
        return gateio_tickers
    except Exception as e:
        return {"error": "Error retrieving ticker data from Gate.io API: {}".format(e)}

def get_order_book(symbol):
    try:
        order_book = gateio.fetch_order_book(symbol)
        return order_book
    except Exception as e:
        return {"error": "Error retrieving order book data for symbol {} from Gate.io API: {}".format(symbol, e)}
