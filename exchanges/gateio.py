import ccxt
import logging

# Create a logger
logger = logging.getLogger(__name)

def get_exchange_data():
    try:
        # Initialize Gate.io exchange instance
        gateio = ccxt.gateio()

        # Load markets, fetch tickers, and other data
        gateio_markets = gateio.load_markets()
        gateio_spot_markets = {symbol: market for symbol, market in gateio_markets.items() if market['spot'] and market['active']}
        gateio_tickers = gateio.fetch_tickers(list(gateio_spot_markets.keys()))

        # Initialize dictionaries to store data
        order_books = {}
        deposit_withdraw_info = {}
        trading_fees = {}
        withdrawal_fees = {}

        # Loop through all available trading pairs
        for symbol in gateio_spot_markets:
            # Retrieve order book data for the current trading pair
            order_books[symbol] = gateio.fetch_order_book(symbol)

            # Retrieve deposit/withdraw network information for the current trading pair's assets
            base_asset, quote_asset = symbol.split('/')
            if base_asset not in deposit_withdraw_info:
                deposit_withdraw_info[base_asset] = gateio.fetch_deposit_and_withdraw(base_asset)
            if quote_asset not in deposit_withdraw_info:
                deposit_withdraw_info[quote_asset] = gateio.fetch_deposit_and_withdraw(quote_asset)

            # Retrieve trading fees for the current trading pair
            trading_fees[symbol] = gateio.fetch_trading_fees(symbol)

            # Retrieve withdrawal fees for the current trading pair's assets
            if base_asset not in withdrawal_fees:
                withdrawal_fees[base_asset] = gateio.fetch_withdraw_fees(base_asset)
            if quote_asset not in withdrawal_fees:
                withdrawal_fees[quote_asset] = gateio.fetch_withdraw_fees(quote_asset)

        return {
            'tickers': gateio_tickers,
            'order_books': order_books,
            'deposit_withdraw_info': deposit_withdraw_info,
            'trading_fees': trading_fees,
            'withdrawal_fees': withdrawal_fees
        }
    except Exception as e:
        # Log the error and its context
        logger.error(f"Error retrieving data from Gate.io API: {e}")
        raise

# If this file is run directly, you can add code to test the function
