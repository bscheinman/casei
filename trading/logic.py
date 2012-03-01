from casei.trading.models import Market, Security, Order, Execution

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
