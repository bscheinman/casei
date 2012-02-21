from casei.ncaacards.logic import get_leaders, get_game, get_entry
from casei.ncaacards.models import *
from casei.views import render_with_request_context
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect

def home(request):
    return render_with_request_context(request, 'ncaa_home.html', { })

@login_required
def game_home(request, game_id):
    game = get_game(game_id)
    if not game:
        return HttpResponseRedirect('/ncaa/')

    try:
        entry = UserEntry.objects.get(user=request.user, game=game)
    except UserEntry.DoesNotExist:
        return HttpResponseRedirect('/ncaa/')

    leaders = get_leaders(game)

    return render_with_request_context(request, 'game_home.html', { 'game':game, 'self_entry':entry, 'leaders':leaders })


def do_logout(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect('/ncaa/')


@login_required
def entry_view(request, game_id, entry_id):
    game = get_game(game_id)
    self_entry = get_entry(game, request.user)
    if not self_entry:
        return HttpResponseRedirect('/ncaa/')
    
    try:
        entry = UserEntry.objects.get(id=entry_id, game__id=game_id)
    except UserEntry.DoesNotExist:
        return HttpResponseRedirect('/ncaa/game/%s/' % game_id)

    teams = []
    
    user_teams = UserTeam.objects.filter(entry=entry)
    for user_team in user_teams:
        team_score = user_team.team.score * user_team.count
        teams.append((user_team.team, user_team.count, team_score))
    
    # sort by team name
    teams = sorted(teams, key=lambda x: x[0].team.abbrev_name)
    return render_with_request_context(request, 'entry.html', { 'game':game, 'self_entry':self_entry, 'entry':entry, 'teams':teams })


@login_required
def marketplace(request, game_id):
    game = get_game(game_id)
    entry = get_entry(game, request.user)
    if not entry:
        return HttpResponseRedirect('/ncaa/')
        

    offers_query = Q(entry__game=game, accepting_user=None)

    ask_filter = request.GET.get('ask_filter', '')
    bid_filter = request.GET.get('bid_filter', '')

    if ask_filter:
        offers_query = offers_query & Q(ask_side__components__team__abbrev_name__iexact=ask_filter)
    if bid_filter:
        offers_query = offers_query & Q(bid_side__components__team__abbrev_name__iexact=bid_filter)

    offers = TradeOffer.objects.filter(offers_query)
    
    return render_with_request_context(request, 'marketplace.html', { 'game':game, 'self_entry':entry, 'offers':offers })


@login_required
def leaderboard(request, game_id):
    game = get_game(game_id)
    entry = get_entry(game, request.user)
    if not entry:
        return HttpResponseRedirect('/ncaa/')

    leaders = get_leaders(game)

    return render_with_request_context(request, 'leaderboard.html', { 'game':game, 'self_entry':entry, 'leaders':leaders })


def get_team_from_identifier(team_id):
    try:
        num_id = int(team_id)
        team_query = Q(id=num_id)
    except ValueError:
        team_query = Q(abbrev_name__iexact=team_id)

    try:
        team = Team.objects.get(team_query)
    except Team.DoesNotExist:
        return None
    
    return team


def create_team_context(**kwargs):
    team = kwargs['team']
    game = kwargs.get('game', None)

    score_counts_list = []
    score_counts = TeamScoreCount.objects.filter(team=team).order_by('scoreType__ordering')
    if game:
        score_multipliers = ScoringSetting.objects.filter(game=game)

    for score_count in score_counts:
        if game:
            multiplier = score_multipliers.get(scoreType=score_count.scoreType).points
            score_counts_list.append((score_count.scoreType.name, score_count.count, score_count.count * multiplier))
        else:
            score_counts_list.append((score_count.scoreType.name, score_count.count))

    context = { 'team':team, 'score_counts':score_counts_list }
    if game:
        game_team = GameTeam.objects.get(game=game, team=team)

        context['game'] = game
        context['game_team'] = game_team

        top_owners_list = []
        top_owners = UserTeam.objects.filter(team=game_team).order_by('-count')
        
        for owner in top_owners:
            top_owners_list.append((owner.entry, owner.count))
        context['top_owners'] = top_owners_list

        offering_trades = TradeOffer.objects.filter(entry__game=game, bid_side__components__team=game_team)
        asking_trades = TradeOffer.objects.filter(entry__game=game, ask_side__components__team=game_team)

        context['offering_trades'] = offering_trades
        context['asking_trades'] = asking_trades

    return context


def team_view(request, team_id):
    team = get_team_from_identifier(team_id)
    if not team:
        return HttpResponseRedirect('/ncaa/')

    return render_with_request_context(request, 'team_view.html', create_team_context(team=team))


@login_required
def game_team_view(request, game_id, team_id):
    game = get_game(game_id)
    entry = get_entry(game, request.user)
    if not entry:
        return HttpResponseRedirect('/ncaa/')

    team = get_team_from_identifier(team_id)
    if not team:
        return HttpResponseRedirect('/ncaa/')

    context = create_team_context(team=team, game=game)
    context['self_entry'] = entry

    return render_with_request_context(request, 'team_view.html', context)


MAX_OFFER_SIZE = 5

@login_required
def create_offer(request, game_id, **kwargs):
    game = get_game(game_id)
    entry = get_entry(game, request.user)
    if not entry:
        return HttpResponseRedirect('/ncaa/')

    all_teams = GameTeam.objects.filter(game=game)

    error = kwargs.get('error', '')

    return render_with_request_context(request, 'create_offer.html', { 'game':game, 'self_entry':entry,\
        'all_teams':all_teams, 'max_offer_size':MAX_OFFER_SIZE, 'error':error })


def create_offer_component(team_name, count_str, teams_in_offer):
    if bool(team_name) != bool(count_str):
        raise Exception('All offer components must have both a team and a share count')
    if team_name:
        if team_name in teams_in_offer:
            raise Exception('Team %s occurs more than once in the offer' % team_name)
        teams_in_offer.add(team_name)
        try:
            team = GameTeam.objects.get(game=game, team__abbrev_name=team_name)
        except GameTeam.DoesNotExist:
            raise Exception('Team %s does not exist in this game' % team_name)

        try:
            count = int(count_str)
        except ValueError:
            raise Exception('You must enter a valid integer value for each offer component')
        if count <= 0:
            raise Exception('All component counts must be positive')

        return (team, count)
    


@login_required
def make_offer(request, game_id):
    if request.method != 'POST':
        return HttpResponseRedirect('/ncaa/game/%s/' % game_id)

    game = get_game(game_id)
    self_entry = get_entry(game, request.user)
    if not self_entry:
        return HttpResponseRedirect('/ncaa/')

    bids, asks = [], []
    teams_in_offer = set()

    try:
        for i in range(MAX_OFFER_SIZE):
            bid_team_name, bid_count_str = request.POST.get('bid_%s_team' % i, ''), request.POST.get('bid_%s_count' % i, '')
            bid = create_offer_component(bid_team_name, bid_count_str, teams_in_offer)
            if bid:
                bids.append(bid)
            ask_team_name, ask_count_str = request.POST.get('ask_%s_team' % i, ''), request.POST.get('ask_%s_count' % i, '')
            ask = create_offer_component(ask_team_name, ask_count_str, teams_in_offer)
            if ask:
                asks.append(ask)

        bid_point_str, ask_point_str = request.POST.get('bid_points', ''), request.POST.get('ask_points', '')
        try:
            if bid_point_str:
                bid_points = int(bid_point_str)
            if ask_point_str:
                ask_points = int(ask_point_str)
        except ValueError:
            raise Exception('You must enter integer values for points')

        if bid_points and ask_points:
            raise Exception('You can\'t include points on both sides of an offer')

    except Exception as e:
        return create_offer(request, game_id, error=str(e))

    bid_side, ask_side = TradeSide(), TradeSide()
    if bid_points:
        bid_side.points = bid_points
    if ask_points:
        ask_side.points = ask_points
    bid_side.save()
    ask_side.save()

    offer = TradeOffer.objects.create(entry=self_entry, ask_side=ask_side, bid_side=bid_side)

    for bid_team, bid_count in bids:
        bid_component = TradeComponent.create(team=bid_team, count=bid_count, offer=bid_side)
    for ask_team, ask_count in asks:
        ask_component = TradeComponent.create(team=ask_team, count=ask_count, offer=ask_side)

    return HttpResponseRedirect('/ncaa/game/%s/offer/%s/' % game_id, offer.id)
