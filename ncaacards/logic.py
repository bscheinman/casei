from casei.ncaacards.models import NcaaGame, TradeComponent, UserEntry, UserTeam

def get_game(game_id):
    try:
        return NcaaGame.objects.get(id=game_id)
    except NcaaGame.DoesNotExist:
        return None


def get_leaders(game):
    return UserEntry.objects.filter(game=game).order_by('-score')


def apply_trade_side(components, points, entry, holdings, addOrRemove):
    for component in components:
        holding = holdings.get(team__team=component.team)
        if addOrRemove:
            holding.count += component.count
        else:
            holding.count -= component.count
        holding.save()
    if addOrRemove:
        entry.extra_points += points
    else:
        entry.extra_points -= points
    entry.save()
        

def validate_trade_side(components, trade_points, entry, holdings):
    for component in components:
        if component.count > holdings.get(team__team=component.team).count:
            return False
    return entry.points >= trade_points



def accept_trade(trade, accepting_entry):
    if trade.is_accepted():
        raise Exception('Trade has already been accepted')

    if accepting_entry == trade.entry:
        raise Exception('Users cannot accept their own trades')

    bid_components = trade.bid_side.components
    ask_components = trade.ask_side.components
    
    bid_points = trade.bid_side.points
    ask_points = trade.ask_side.points

    seller = trade.entry
    buyer = accepting_entry

    seller_holdings = seller.teams
    buyer_holdings = buyer.teams

    if not (validate_trade_side(bid_components, bid_points, seller_holdings, seller.extra_points)\
            and validate_trade_side(ask_components, ask_points, buyer_holdings, buyer.extra_points)):
        raise Exception('Entries do not have sufficient resources to complete the trade')

    apply_trade_side(bid_components, bid_points, seller, seller_holdings, False)
    apply_trade_side(ask_components, ask_points, buyer, buyer_holdings, False)
    apply_trade_side(bid_components, bid_points, buyer, buyer_holdings, True)
    apply_trade_side(ask_components, ask_points, seller, seller_holdings, True)
