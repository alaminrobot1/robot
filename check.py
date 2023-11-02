from config import EXCHANGES
import ccxt
import importlib


def check_liquidity(exchange_key, symbol, min_liquidity):
    exchange_info = EXCHANGES.get(exchange_key)
    if not exchange_info:
        return False, False

    # Create a CCXT exchange instance based on the exchange's module name
    exchange = importlib.import_module(exchange_info['module'])

    try:
        order_book = exchange.fetchOrderBook(symbol)
        liquidity = order_book['asks'][0][1] + order_book['bids'][0][1]

        # Check if liquidity meets the minimum requirement
        if liquidity >= min_liquidity:
            return liquidity, True
        else:
            return liquidity, False

    except Exception as e:
        return False, False
