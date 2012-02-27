from casei.trading.models import Market, Security, Order, Execution


def process_new_order(order):
    def execute_orders(o1, o2):
        exec_quantity = min(o1.quantity, o2.quantity)
        o1.quantity_remaining -= exec_quantity
        o2.quantity_remaining -= exec_quantity
        o1.save()
        o2.save()

        if o1.is_buy:
            buy_order = o1
            sell_order = o2
        else:
            buy_order = o2
            sell_order = o1

        execution = Execution.objects.create(security=order.security, buy_order=buy_order, sell_order=sell_order, quantity=exec_quantity, price=order.price)
    
    if order.is_buy:
        comparer = lambda x: x.price <= order.price
        order_generator = lambda: order.get_top_asks()
    else:
        comparer = lambda x: x.price >= order.price
        order_generator = lambda: order.get_top_bids()

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


def place_order(placer_name, security_name, is_buy, price, quantity):
    try:
        security = Security.objects.get(name=security_name)
    except Security.DoesNotExist:
        raise Exception('No security exists with name %s' % security_name)

    order = Order.objects.create(placer=placer_name, security=security, price=price, quantity=quantity, quantity_remaining=quantity, is_buy=is_buy)
    
    
