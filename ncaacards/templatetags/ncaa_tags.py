from django import template
register = template.Library()

@register.inclusion_tag('offer_table.html')
def render_offer_table(offer):
    rows = []
    bids = offer.bid_side.components
    asks = offer.ask_side.components
    bid_count = bids.count()
    ask_count = asks.count()
    # maybe later change this to actually use iterators since lists don't have constant-time random access
    # for now it doesn't really matter
    for i in range(max(bid_count, ask_count)):
        bid = None
        ask = None
        if i < bid_count:
            bid = bids[i]
        if i < ask_count:
            ask = asks[i]
        rows.append((bid, ask))
    return { 'rows':rows }


@register.inclusion_tag('team_link.html')
def team_link(team, game=None):
    return { 'team':team, 'game':game }


@register.inclusion_tag('entry_link.html')
def entry_link(entry):
    return { 'entry':entry }
