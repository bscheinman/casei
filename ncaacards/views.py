from casei.ncaacards.models import *
from casei.views import render_with_request_context
from django.contrib.auth import logout
from django.db.models import Q
from django.http import HttpResponseRedirect

def home(request):
    return render_with_request_context(request, 'ncaa_home.html', { })


def do_logout(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect('/ncaa/')


def entry_view(request, game_id, entry_id):
    try:
        game = NcaaGame.objects.get(id=game_id)
    except NcaaGame.DoesNotExist:
        return HttpResponseRedirect('/ncaa/')
    
    try:
        entry = UserEntry.objects.get(id=entry_id, game__id=game_id)
    except UserEntry.DoesNotExist:
        return HttpResponseRedirect('/ncaa/game/%s/' % game_id)

    teams = []
    total_score = 0
    
    user_teams = UserTeam.objects.filter(entry=entry)
    for user_team in user_teams:
        team_score = user_team.team.score * user_team.count
        total_score += team_score
        teams.append((user_team.team, user_team.count, team_score))
    
    # sort by team name
    teams = sorted(teams, key=lambda x: x[0].team.abbrev_name)
    return render_with_request_context(request, 'entry.html', { 'entry':entry, 'teams':teams, 'total_score':total_score })


def marketplace(request, game_id):
    try:
        game = NcaaGame.objects.get(id=game_id)
    except NcaaGame.DoesNotExist:
        return HttpResponseRedirect('/ncaa/')
    
    offers_query = Q(entry__game=game, accepting_user=None)

    ask_filter = request.GET.get('ask_filter', '')
    bid_filter = request.GET.get('bid_filter', '')

    if ask_filter:
        offers_query = offers_query & Q(ask_side__components__team__abbrev_name__iexact=ask_filter)
    if bid_filter:
        offers_query = offers_query & Q(bid_side__components__team__abbrev_name__iexact=bid_filter)

    offers = TradeOffer.objects.filter(offers_query)

    return HttpResponseRedirect('/ncaa/')
    #return render_with_request_context(request, 'marketplace.html', { 'game'=game, 'offers'=offers })


def leaderboard(request, game_id):
    try:
        game = NcaaGame.objects.get(id=game_id)
    except NcaaGame.DoesNotExist:
        return HttpResponseRedirect('/ncaa/')
    
    leaders = UserEntry.objects.filter(game=game).order_by('score')

    return render_with_request_context(request, 'leaderboard.html', { 'game':game, 'leaders':leaders })


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
        context['game'] = game
        context['game_team'] = GameTeam.objects.get(game=game, team=team)
    return context


def team_view(request, team_id):
    team = get_team_from_identifier(team_id)
    if not team:
        return HttpResponseRedirect('/ncaa/')

    return render_with_request_context(request, 'team_view.html', create_team_context(team=team))


def game_team_view(request, game_id, team_id):
    try:
        game = NcaaGame.objects.get(id=game_id)
    except NcaaGame.DoesNotExist:
        return HttpResponseRedirect('/ncaa/')

    team = get_team_from_identifier(team_id)
    if not team:
        return HttpResponseRedirect('/ncaa/')

    game_team = GameTeam.objects.get(game=game, team=team)

    return render_with_request_context(request, 'team_view.html', create_team_context(team=team, game=game))
