from importlib import import_module
from config import EXCHANGES
from check import check_liquidity
from flask import request

def get_exchange_name(exchange_key):
    return EXCHANGES[exchange_key]['name']

def get_exchange_module(exchange_key):
    module_name = EXCHANGES[exchange_key]['module']
    return import_module(module_name)

def calculate_arbitrage(exchange1, exchange2, min_liquidity):
    exchange1_config = EXCHANGES.get(exchange1)
    exchange2_config = EXCHANGES.get(exchange2)

    if not exchange1_config or not exchange2_config:
        return []

    exchange1_module = get_exchange_module(exchange1_config['module'])
    exchange2_module = get_exchange_module(exchange2_config['module'])

    exchange1_tickers = exchange1_module.get_exchange_data()
    exchange2_tickers = exchange2_module.get_exchange_data()

    common_symbols = set(exchange1_tickers.keys()) & set(exchange2_tickers.keys())

    data = []
    for symbol in common_symbols:
        # Check for liquidity on both exchanges
        liquidity1 = check_liquidity(exchange1, symbol)
        liquidity2 = check_liquidity(exchange2, symbol)

        # Only include arbitrage opportunities where both exchanges have sufficient liquidity
        if liquidity1 >= min_liquidity and liquidity2 >= min_liquidity:

            exchange1_price = float(exchange1_tickers[symbol]['last'])
            exchange2_price = float(exchange2_tickers[symbol]['last']) if exchange2_tickers[symbol]['last'] is not None else 0.0
            arbitrage = round((exchange2_price - exchange1_price) / exchange1_price * 100, 2)

            # Add new updates
            # Calculate the spread between the two exchanges
            spread = round((exchange2_price - exchange1_price) / (exchange1_price + exchange2_price) * 2 * 100, 2)

            # Calculate the arbitrage opportunity in percentage terms
            arbitrage_opportunity = round(arbitrage - spread, 2)

            # Include base URLs for trading
            exchange1_trade_link = exchange1_config['trade_base_url'] + symbol.replace('/', '_')
            exchange2_trade_link = exchange2_config['trade_base_url'] + symbol.replace('/', '_')

            # Add the new fields to the data dictionary
            data.append({
                'symbol': symbol,
                'exchange1_price': exchange1_price,
                'exchange2_price': exchange2_price,
                'arbitrage': arbitrage,
                'spread': spread,
                'arbitrage_opportunity': arbitrage_opportunity,
                'exchange1_trade_link': exchange1_trade_link,
                'exchange2_trade_link': exchange2_trade_link,
                'exchange1_name': exchange1_config['name'],
                'exchange2_name': exchange2_config['name']
            })

    # Sort data by arbitrage opportunity value
    data.sort(key=lambda x: x['arbitrage_opportunity'], reverse=True)

    return data
