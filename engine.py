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

    exchange1_tickers = exchange1_module.get_exchange_data()
    exchange2_tickers = exchange2_module.get_exchange_data()

    exchange1_trade_base_url = exchange1_config['trade_base_url']
    exchange2_trade_base_url = exchange2_config['trade_base_url']

    common_symbols = set(exchange1_tickers.keys()) & set(exchange2_tickers.keys())

    data = []
    for symbol in common_symbols:
        exchange1_price = float(exchange1_tickers[symbol]['last'])
        exchange2_price = float(exchange2_tickers[symbol]['last']) if exchange2_tickers[symbol]['last'] is not None else 0.0
        arbitrage = round((exchange2_price - exchange1_price) / exchange1_price * 100, 2)
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
            'exchange1_price': exchange1_price,
            'exchange2_price': exchange2_price,
            'arbitrage': arbitrage,
            'exchange1_trade_link': exchange1_trade_link,
            'exchange2_trade_link': exchange2_trade_link,
            'exchange1_name': exchange1_config['name'],
            'exchange2_name': exchange2_config['name']
        })

    # Sort data by arbitrage value
    data.sort(key=lambda x: x['arbitrage'], reverse=True)

    return data

