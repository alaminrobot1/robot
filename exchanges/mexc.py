import ccxt
import logging

# Create a logger specific to this module
logger = logging.getLogger(__name__)

# Create a custom module-specific name
__module_name__ = "mexc_module"

def get_exchange_data():
    try:
        # Initialize MXC exchange instance
        mxc = ccxt.mxc()

        # Load markets, fetch tickers, and other data
        mxc_markets = mxc.load_markets()
        mxc_spot_markets = {symbol: market for symbol, market in mxc_markets.items() if market['spot'] and market['active']}
        mxc_tickers = mxc.fetch_tickers(list(mxc_spot_markets.keys()))

        # Initialize dictionaries to store data
        order_books = {}
        deposit_withdraw_info = {}
        trading_fees = {}
        withdrawal_fees = {}

        # Loop through all available trading pairs
        for symbol in mxc_spot_markets:
            # Retrieve order book data for the current trading pair
            order_books[symbol] = mxc.fetch_order_book(symbol)

            # Retrieve deposit/withdraw network information for the current trading pair's assets
            base_asset, quote_asset = symbol.split('/')
            if base_asset not in deposit_withdraw_info:
                deposit_withdraw_info[base_asset] = mxc.fetch_deposit_and_withdraw(base_asset)
            if quote_asset not in deposit_withdraw_info:
                deposit_withdraw_info[quote_asset] = mxc.fetch_deposit_and_withdraw(quote_asset)

            # Retrieve trading fees for the current trading pair
            trading_fees[symbol] = mxc.fetch_trading_fees(symbol)

            # Retrieve withdrawal fees for the current trading pair's assets
            if base_asset not in withdrawal_fees:
                withdrawal_fees[base_asset] = mxc.fetch_withdraw_fees(base_asset)
            if quote_asset not in withdrawal_fees:
                withdrawal_fees[quote_asset] = mxc.fetch_withdraw_fees(quote_asset)

        return {
            'exchange_name': __module_name__,
            'tickers': mxc_tickers,
            'order_books': order_books,
            'deposit_withdraw_info': deposit_withdraw_info,
            'trading_fees': trading_fees,
            'withdrawal_fees': withdrawal_fees
        }
    except Exception as e:
        # Log the error and its context
        logger.error(f"Error retrieving data from MXC API: {e}")
        raise
