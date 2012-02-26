from array import array
from django import template
register = template.Library()
import random

@register.filter
def get_range(i):
    return range(i)


@register.inclusion_tag('offer_table.html')
def render_offer_table(offer, entry):
    rows = []
    bids, asks = list(offer.bid_side.components.all()), list(offer.ask_side.components.all())
    bid_points, ask_points = offer.bid_side.points, offer.ask_side.points

    if bid_points:
        bids.append(bid_points)
    if ask_points:
        asks.append(ask_points)

    bid_count, ask_count = len(bids), len(asks)
    bid_total, ask_total = 0,0
    # maybe later change this to actually use iterators since lists don't have constant-time random access
    # for now it doesn't really matter
    for i in range(max(bid_count, ask_count)):
        bid, ask = None, None
        if i < bid_count:
            bid = bids[i]
            if hasattr(bid, 'get_score'): # this is a hacky way of checking for the special case points row
                bid_total += bid.get_score()
            else:
                bid_total += bid
        if i < ask_count:
            ask = asks[i]
            if hasattr(ask, 'get_score'):
                ask_total += ask.get_score()
            else:
                ask_total += ask
        rows.append((bid, ask))

    can_claim, can_cancel = False, False
    if not offer.is_accepted():
        if offer.entry.id != entry.id:
            can_claim = True
        elif offer.is_active:
            can_cancel = True

    return { 'offer':offer, 'rows':rows, 'bid_points':bid_points, 'ask_points':ask_points, 'bid_total':bid_total, 'ask_total':ask_total, 'can_claim':can_claim, 'can_cancel':can_cancel }


@register.inclusion_tag('team_link.html')
def team_link(team, game=None):
    return { 'team':team, 'game':game }


@register.inclusion_tag('entry_link.html')
def entry_link(entry):
    return { 'entry':entry }


@register.inclusion_tag('game_link.html')
def game_link(game):
    return { 'game':game }


@register.inclusion_tag('leaderboard.html')
def leaderboard(leaders):
    return { 'leaders':leaders }


@register.inclusion_tag('auth_block.html')
def auth_block(user):
    return { 'user':user }


CI_LOWER = 'case insensitive'
@register.inclusion_tag('ci_text.html')
def ci_text():
    ci_array = array('c', CI_LOWER)
    for i in range(len(CI_LOWER)):
        if random.randint(0,1):
            ci_array[i] = ci_array[i].upper()
    return { 'ci_text':ci_array.tostring() }
