from django import template
register = template.Library()

@register.filter
def get_range(i):
    return range(i)


@register.inclusion_tag('offer_table.html')
def render_offer_table(offer):
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

    return { 'rows':rows, 'bid_points':bid_points, 'ask_points':ask_points, 'bid_total':bid_total, 'ask_total':ask_total }


@register.inclusion_tag('team_link.html')
def team_link(team, game=None):
    return { 'team':team, 'game':game }


@register.inclusion_tag('entry_link.html')
def entry_link(entry):
    return { 'entry':entry }


@register.inclusion_tag('leaderboard.html')
def leaderboard(leaders):
    return { 'leaders':leaders }
