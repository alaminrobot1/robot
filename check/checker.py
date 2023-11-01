# check/checker.py

def check_liquidity(exchange_data, symbol, threshold):
    if symbol in exchange_data:
        # Assuming exchange_data contains order book information for the symbol
        # Check the liquidity of the order book, for example, by summing the order quantities
        total_liquidity = sum(order['quantity'] for order in exchange_data[symbol]['order_book'])
        return total_liquidity >= threshold
    else:
        return False

def check_deposit_withdraw_match(exchange1_data, exchange2_data, symbol):
    if symbol in exchange1_data and symbol in exchange2_data:
        # Assuming exchange_data contains deposit and withdraw network information
        withdraw_network1 = exchange1_data[symbol]['withdraw_network']
        withdraw_network2 = exchange2_data[symbol]['withdraw_network']
        deposit_network1 = exchange1_data[symbol]['deposit_network']
        deposit_network2 = exchange2_data[symbol]['deposit_network']
        
        # Check if the withdrawal and deposit networks match
        if withdraw_network1 == deposit_network2 and withdraw_network2 == deposit_network1:
            return True
    return False

def calculate_arbitrage_with_fees(exchange1, exchange2, fee1, fee2, symbol):
    exchange1_price = ...  # Replace with actual price retrieval
    exchange2_price = ...  # Replace with actual price retrieval
    
    # Calculate the arbitrage opportunity including withdrawal fees
    arbitrage = ((exchange2_price - exchange1_price) / exchange1_price - fee1 - fee2) * 100
    return round(arbitrage, 2)
