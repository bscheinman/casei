from casei.trading.models import Market, Security, Order, Execution


def process_new_order(order):
    def execute_orders(accepting_order, existing_order):
        exec_quantity = min([accepting_order.quantity, existing_order.quantity])

        if accepting_order.is_buy:
            buy_order = accepting_order
            sell_order = existing_order
        else:
            buy_order = existing_order
            sell_order = accepting_order

        execution = Execution.objects.create(security=order.security, buy_order=buy_order, sell_order=sell_order, quantity=exec_quantity, price=order.price)

    if order.is_buy:
        comparer = lambda x: x.price <= order.price
        order_generator = lambda: order.security.get_top_asks()
    else:
        comparer = lambda x: x.price >= order.price
        order_generator = lambda: order.security.get_top_bids()

    while True:
        orders = order_generator()
        if not orders:
            return
        for matching_order in orders:
            if not comparer(order):
                return
            execute_orders(order, matching_order)
            if order.quantity_remaining <= 0:
                return


def get_security(market_name, security_name):
    try:
        market = Market.objects.get(name=market_name)
    except Market.DoesNotExist:
        return None
    try:
        security = Security.objects.get(market=market, name=security_name)
    except Security.DoesNotExist:
        return None
    else:
        return security


def place_order(market_name, placer_name, security_name, is_buy, price, quantity):
    security = get_security(market_name, security_name)
    if not security:
        raise Exception('No security %s exists in the market %s' % (security_name, market_name))

    if quantity <= 0:
        raise Exception('Offers must have a positive quantity')

    order = Order.objects.create(placer=placer_name, security=security, price=price, quantity=quantity, quantity_remaining=quantity, is_buy=is_buy)
    process_new_order(order)
    
