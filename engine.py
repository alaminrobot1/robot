# engine.py
from importlib import import_module
from config import EXCHANGES

def get_exchange_name(exchange_key):
    return EXCHANGES[exchange_key]['name']

def get_exchange_module(exchange_key):
    module_name = EXCHANGES[exchange_key]['module']
    return import_module(module_name)

def calculate_arbitrage(exchange1, exchange2):
    exchange1_config = EXCHANGES.get(exchange1)
    exchange2_config = EXCHANGES.get(exchange2)

    if not exchange1_config or not exchange2_config:
        return []

    exchange1_module = get_exchange_module(exchange1_config['module'])
    exchange2_module = get_exchange_module(exchange2_config['module'])

    exchange1_tickers = exchange1_module.get_exchange_tickers()
    exchange2_tickers = exchange2_module.get_exchange_tickers()

    exchange1_trade_base_url = exchange1_config['trade_base_url']
    exchange2_trade_base_url = exchange2_config['trade_base_url']

    common_symbols = set(exchange1_tickers.keys()) & set(exchange2_tickers.keys())

    data = []
    for symbol in common_symbols:
        # Get the order books from both exchanges
        order_book_exchange1 = exchange1_module.get_order_book(symbol)
        order_book_exchange2 = exchange2_module.get_order_book(symbol)

        # Calculate bid and ask prices
        exchange1_bid_price = sum(bid[0] * bid[1] for bid in order_book_exchange1['bids']) / sum(bid[1] for bid in order_book_exchange1['bids'])
        exchange1_ask_price = sum(ask[0] * ask[1] for ask in order_book_exchange1['asks']) / sum(ask[1] for ask in order_book_exchange1['asks'])
        exchange2_bid_price = sum(bid[0] * bid[1] for bid in order_book_exchange2['bids']) / sum(bid[1] for bid in order_book_exchange2['bids'])
        exchange2_ask_price = sum(ask[0] * ask[1] for ask in order_book_exchange2['asks']) / sum(ask[1] for ask in order_book_exchange2['asks'])

        # Calculate arbitrage percentage based on bid and ask prices
        arbitrage_percentage = calculate_arbitrage_percentage(exchange1_ask_price, exchange2_bid_price)

        # Construct trade links
        if exchange1 in ('exchanges.mexc', 'exchanges.gateio', 'exchanges.binance'):
            exchange1_symbol_link = symbol.replace('/', '_')
        elif exchange1 == 'exchanges.bybit':
            exchange1_symbol_link = symbol.replace('/', '/')
        elif exchange1 == 'exchanges.kucoin':
            exchange1_symbol_link = symbol.replace('/', '-')
       
           
            

        if exchange2 in ('exchanges.mexc', 'exchanges.gateio', 'exchanges.binance'):
            exchange2_symbol_link = symbol.replace('/', '_')
        elif exchange2 == 'exchanges.bybit':
            exchange2_symbol_link = symbol.replace('/', '/')
        elif exchange2 == 'exchanges.kucoin':
            exchange2_symbol_link = symbol.replace('/', '-')
        
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
