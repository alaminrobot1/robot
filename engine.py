# engine.py
from importlib import import_module
from config import EXCHANGES

def get_exchange_name(exchange_key):
    return EXCHANGES.get(exchange_key, {}).get('name', 'Unknown')

def get_exchange_module(exchange_key):
    module_name = EXCHANGES.get(exchange_key, {}).get('module')
    if module_name:
        return import_module(module_name)
    return None

def calculate_arbitrage(exchange1, exchange2):
    exchange1_config = EXCHANGES.get(exchange1)
    exchange2_config = EXCHANGES.get(exchange2)

    if not exchange1_config or not exchange2_config:
        return []

    exchange1_module = get_exchange_module(exchange1_config['module'])
    exchange2_module = get_exchange_module(exchange2_config['module'])

    if not exchange1_module or not exchange2_module:
        return []

    exchange1_tickers = exchange1_module.get_exchange_tickers()
    exchange2_tickers = exchange2_module.get_exchange_tickers()

    if not exchange1_tickers or not exchange2_tickers:
        return []

    exchange1_trade_base_url = exchange1_config.get('trade_base_url', '')
    exchange2_trade_base_url = exchange2_config.get('trade_base_url', '')

    common_symbols = set(exchange1_tickers.keys()) & set(exchange2_tickers.keys())

    data = []
    for symbol in common_symbols:
        # Get the order books from both exchanges
        try:
            order_book_exchange1 = exchange1_module.get_order_book(symbol)
            order_book_exchange2 = exchange2_module.get_order_book(symbol)
        except Exception as e:
            continue  # Skip this symbol if there's an error

        # Check if order books are empty
        if not order_book_exchange1 or not order_book_exchange2:
            continue

        # Calculate bid and ask prices
        exchange1_bid_price = order_book_exchange1['bids'][0][0]
        exchange1_ask_price = order_book_exchange1['asks'][0][0]
        exchange2_bid_price = order_book_exchange2['bids'][0][0]
        exchange2_ask_price = order_book_exchange2['asks'][0][0]

        # Calculate arbitrage percentage based on bid and ask prices
        try:
            arbitrage_percentage = calculate_arbitrage_percentage(exchange1_ask_price, exchange2_bid_price)
        except ZeroDivisionError:
            continue  # Skip this symbol if there's a division by zero error

        # Construct trade links
        exchange1_symbol_link = symbol.replace('/', '_')
        exchange2_symbol_link = symbol.replace('/', '_')
        
        exchange1_trade_link = "{}{}".format(exchange1_trade_base_url, exchange1_symbol_link)
        exchange2_trade_link = "{}{}".format(exchange2_trade_base_url, exchange2_symbol_link)
        
        data.append({
            'symbol': symbol,
            'exchange1_bid_price': exchange1_bid_price,
            'exchange2_ask_price': exchange2_ask_price,
            'arbitrage_percentage': arbitrage_percentage,
            'exchange1_trade_link': exchange1_trade_link,
            'exchange2_trade_link': exchange2_trade_link,
            'exchange1_name': exchange1_config['name'],
            'exchange2_name': exchange2_config['name']
        })

    # Sort data by arbitrage percentage
    data.sort(key=lambda x: x['arbitrage_percentage'], reverse=True)

    return data

def calculate_arbitrage_percentage(ask_price, bid_price):
    if ask_price > 0 and bid_price > 0:
        return ((bid_price - ask_price) / ask_price) * 100
    return 0
