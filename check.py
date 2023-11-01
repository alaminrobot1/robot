import ccxt

def check_liquidity_and_network(exchange, symbol):
    """
    Checks the liquidity and deposit/withdraw network availability for a given symbol on an exchange.

    Args:
        exchange: The exchange object.
        symbol: The symbol to check.

    Returns:
        A tuple of two booleans, where the first boolean indicates whether or not the symbol has sufficient liquidity and the second boolean indicates whether or not the deposit/withdraw network is available for the symbol.
    """

    # Check for liquidity
    order_book = exchange.fetchOrderBook(symbol)
    liquidity = order_book['asks'][0][1] + order_book['bids'][0][1]

    # Check for deposit/withdraw network availability
    deposit_methods = exchange.fetchDepositMethods(symbol)
    withdrawal_methods = exchange.fetchWithdrawalMethods(symbol)

    if symbol in deposit_methods and symbol in withdrawal_methods:
        deposit_withdraw_network_available = True
    else:
        deposit_withdraw_network_available = False

    return liquidity, deposit_withdraw_network_available

