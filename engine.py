import ccxt
from .check_liquidity_and_network import check_liquidity_and_network

class Engine:

    def __init__(self, exchanges):
        self.exchanges = exchanges

    def get_all_symbols(self):
        """
        Gets a list of all the symbols that are supported by all exchanges.

        Returns:
            A list of symbols.
        """

        symbols = set()

        for exchange in self.exchanges:
            symbols.update(exchange.get_symbols())

        return list(symbols)

    def calculate_arbitrage(self, exchange1, exchange2, symbol):
        """
        Calculates the arbitrage between two exchanges for a given symbol.

        Args:
            exchange1: The first exchange.
            exchange2: The second exchange.
            symbol: The symbol to check.

        Returns:
            A float representing the arbitrage percentage.
        """

        exchange1_price = exchange1.get_price(symbol)
        exchange2_price = exchange2.get_price(symbol)

        arbitrage = (exchange2_price - exchange1_price) / exchange1_price * 100

        return arbitrage

    def scan_arbitrage(self):
        """
        Scans for arbitrage opportunities across all exchanges.

        Returns:
            A list of arbitrage opportunities.
        """

        arbitrage_opportunities = []

        symbols = self.get_all_symbols()

        for exchange1 in self.exchanges:
            for exchange2 in self.exchanges:
                if exchange1 is not exchange2:
                    for symbol in symbols:
                        liquidity, deposit_withdraw_network_available = check_liquidity_and_network(exchange1, symbol)

                        # Only include arbitrage opportunities where both exchanges have sufficient liquidity and have deposit/withdraw network availability
                        if liquidity > 0 and deposit_withdraw_network_available:
                            arbitrage = self.calculate_arbitrage(exchange1, exchange2, symbol)

                            arbitrage_opportunities.append({
                                'symbol': symbol,
                                'exchange1': exchange1.name,
                                'exchange2': exchange2.name,
                                'arbitrage': arbitrage
                            })

        return arbitrage_opportunities

