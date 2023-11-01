import ccxt
import importlib


def check_liquidity_and_network(exchange_key, symbol):
    exchange_info = EXCHANGES.get(exchange_key)
    if not exchange_info:
        return False, False

    # Create a CCXT exchange instance based on the exchange's module name
    exchange = importlib.import_module(exchange_info['module'])

    try:
        order_book = exchange.fetchOrderBook(symbol)
        liquidity = order_book['asks'][0][1] + order_book['bids'][0][1]

        deposit_methods = exchange.fetchDepositMethods(symbol)
        withdrawal_methods = exchange.fetchWithdrawalMethods(symbol)

        if symbol in deposit_methods and symbol in withdrawal_methods:
            deposit_withdraw_network_available = True
        else:
            deposit_withdraw_network_available = False

        return liquidity, deposit_withdraw_network_available

    except Exception as e:
        return False, False
