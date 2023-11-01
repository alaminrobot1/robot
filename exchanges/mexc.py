import ccxt

mexc = ccxt.mexc()

def get_exchange_data():
    try:
        mexc_markets = mexc.load_markets()
        mexc_spot_markets = {symbol: market for symbol, market in mexc_markets.items() if market['spot'] and market['active']}
        mexc_tickers = mexc.fetch_tickers(list(mexc_spot_markets.keys()))

        # Initialize dictionaries to store order book, deposit/withdraw, trading fee, and withdrawal fee data
        order_books = {}
        deposit_withdraw_info = {}
        trading_fees = {}
        withdrawal_fees = {}

        # Loop through all available trading pairs
        for symbol in mexc_spot_markets:
            # Retrieve order book data for the current trading pair
            order_books[symbol] = mexc.fetch_order_book(symbol)

            # Retrieve deposit/withdraw network information for the current trading pair's assets
            base_asset, quote_asset = symbol.split('/')
            if base_asset not in deposit_withdraw_info:
                deposit_withdraw_info[base_asset] = mexc.fetch_deposit_and_withdraw(base_asset)
            if quote_asset not in deposit_withdraw_info:
                deposit_withdraw_info[quote_asset] = mexc.fetch_deposit_and_withdraw(quote_asset)

            # Retrieve trading fees for the current trading pair
            trading_fees[symbol] = mexc.fetch_trading_fees(symbol)

            # Retrieve withdrawal fees for the current trading pair's assets
            if base_asset not in withdrawal_fees:
                withdrawal_fees[base_asset] = mexc.fetch_withdraw_fees(base_asset)
            if quote_asset not in withdrawal_fees:
                withdrawal_fees[quote_asset] = mexc.fetch_withdraw_fees(quote_asset)

        return {
            'tickers': mexc_tickers,
            'order_books': order_books,
            'deposit_withdraw_info': deposit_withdraw_info,
            'trading_fees': trading_fees,
            'withdrawal_fees': withdrawal_fees
        }
    except Exception as e:
        return None, "Error retrieving data from MEXC API: {}".format(e)
