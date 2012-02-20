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
    return render_with_request_context(request, 'entry.html', { 'self_entry':self_entry, 'entry':entry, 'teams':teams })


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
