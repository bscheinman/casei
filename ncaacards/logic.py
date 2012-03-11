from casei.ncaacards.models import NcaaGame, Team, TradeComponent, UserEntry, UserTeam
from django.db.models import Q
import datetime

def get_game(game_id):
    try:
        return NcaaGame.objects.get(id=game_id)
    except NcaaGame.DoesNotExist:
        return None


def get_entry(game, user):  
    try:
        return UserEntry.objects.get(game=game, user=user)
    except UserEntry.DoesNotExist:
        return None


def get_leaders(game):
    return UserEntry.objects.filter(game=game).order_by('-score')


def check_limits(entry, teams):
    game = entry.game
    if game.position_limit:
        for team in teams:
            check_position_limits(entry, team)
    if game.points_limit:
        check_points_limit(entry)


def check_position_limits(entry, team):
    game = entry.game
    position_limit = game.position_limit
    if not position_limit:
        return

    team_count = UserTeam.objects.get(entry=entry, team=team).count
    if game.supports_cards:
        bid_components = TradeComponent.objects.filter(offer__bid_offer__is_active=True, offer__bid_offer__entry=entry, team=team)
        for component in bid_components:
            if team_count - component.count < -1 * position_limit:
                offer = component.offer.bid_offer
                offer.is_active = False
                offer.save()
        ask_components = TradeComponent.objects.filter(offer__ask_offer__is_active=True, offer__ask_offer__entry=entry, team=team)
        for component in ask_components:
            if team_count + component.count > position_limit:
                offer = component.offer.ask_offer
                offer.is_active = False
                offer.save()

    if game.supports_stocks:
        orders = Order.objects.filter(placer=entry.entry_name, security__name=team.team.abbrev_name, is_active=True, quantity_remaining__gt=0)
        for order in orders:
            if (order.is_buy and team_count - bid.quantity_remaining < -1 * position_limit) or\
                (not order.is_buy and team_count + order.quantity_remaining > position_limit):
                    order.is_active = False
                    order.save()


def check_point_limits(entry):
    game = entry.game
    points_limit = game.points_limit
    if not points_limit:
        return

    entry_points = entry.extra_points
    if game.supports_cards:
        offers = TradeOffer.objects.filter(entry=entry, is_active=True)
        for offer in offers:
            bid_points = offer.bid_side.points
            if bid_points > 0 and entry_points - bid_points < -1 * points_limit:
                offer.is_active = False
                offer.save()

    if game.supports_stocks:
        orders = Order.objects.filter(placer=entry.entry_name, is_active=True, quantity_remaining__gt=0)
        for order in orders:
            if order.is_buy and entry_points - order.price * order.quantity_remaining < -1 * points_limit:
                order.is_active = False
                order.save()



def apply_trade_side(components, points, entry, holdings, addOrRemove):
    for component in components:
        holding = holdings.get(team=component.team)
        if addOrRemove:
            holding.count += component.count
            component.team.volume += component.count
            component.team.save()
        else:
            holding.count -= component.count
        holding.save()
    if points:
        if addOrRemove:
            entry.extra_points += points
        else:
            entry.extra_points -= points
    entry.save()
        

def validate_trade_side(components, entry, positions, is_buying, position_limit):
    for component in components:
        position = positions.get(team=component.team)
        if is_buying:
            if position.count + component.count > position_limit:
                raise Exception('%s would acquire %s shares of %s but their current position is %s and the position limit is %s' %\
                    (entry.entry_name, component.count, component.team.team.abbrev_name, position.count, position_limit))
        else:
            if position.count - component.count < -1 * position_limit:
                raise Exception('%s would give up %s shares of %s but their current position is %s and the position limit is %s' %\
                    (entry.entry_name, component.count, component.team.team.abbrev_name, position.count, position_limit))


def accept_trade(trade, accepting_entry):
    if trade.is_accepted():
        raise Exception('Trade has already been accepted')

    if accepting_entry == trade.entry:
        raise Exception('Users cannot accept their own trades')

    bid_components = trade.bid_side.components.all()
    ask_components = trade.ask_side.components.all()
    
    bid_points = trade.bid_side.points
    ask_points = trade.ask_side.points

    seller = trade.entry
    buyer = accepting_entry

    seller_holdings = seller.teams.all()
    buyer_holdings = buyer.teams.all()

    position_limit = seller.game.position_limit
    if position_limit:
        validate_trade_side(bid_components, seller, seller_holdings, False, position_limit)
        validate_trade_side(bid_components, buyer, buyer_holdings, True, position_limit)
        validate_trade_side(ask_components, seller, seller_holdings, True, position_limit)
        validate_trade_side(ask_components, buyer, buyer_holdings, False, position_limit)

    if trade.entry.game.points_limit:
        points_short_limit = -1 * trade.entry.game.points_limit
        points_error_info = None
        if ask_points > 0:
            if buyer.extra_points - ask_points < points_short_limit:
                points_error_info = (buyer.entry_name, ask_points, buyer.extra_points, points_short_limit)
        elif ask_points and ask_points < 0:
            if seller.extra_points + ask_points < points_short_limit:
                points_error_info = (seller.entry_name, ask_points, seller.extra_points, points_short_limit)
        elif bid_points > 0:
            if seller.extra_points - bid_points < points_short_limit:
                points_error_info = (seller.entry_name, bid_points, seller.extra_points, points_short_limit)
        elif bid_points and bid_points < 0:
            if buyer.extra_points + bid_points < points_short_limit:
                points_error_info = (buyer.entry_name, bid_points, buyer.extra_points, points_short_limit)
        
        if points_error_info:
            raise Exception('%s would give up %s points but they have %s and the points short limit is %s' % points_error_info)
            

    apply_trade_side(bid_components, bid_points, seller, seller_holdings, False)
    apply_trade_side(ask_components, ask_points, buyer, buyer_holdings, False)
    apply_trade_side(bid_components, bid_points, buyer, buyer_holdings, True)
    apply_trade_side(ask_components, ask_points, seller, seller_holdings, True)
    trade.accepting_user = accepting_entry
    trade.accept_time = datetime.datetime.now()
    trade.save()

    teams = []
    for component in bid_components:
        teams.append(component.team)
    for component in ask_components:
        teams.append(component.team)
    check_limits(buyer, teams)
    check_limits(seller, teams)

    trade.entry.update_score()
    accepting_entry.update_score()


def get_team_from_identifier(team_id):
    try:
        num_id = int(team_id)
        team_query = Q(id=num_id)
    except ValueError:
        team_query = Q(abbrev_name__iexact=team_id)

    try:
        return Team.objects.get(team_query)
    except Team.DoesNotExist:
        return None
