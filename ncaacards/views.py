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


def entry_view(request, entry_id):
    try:
        entry = UserEntry.objects.get(id=entry_id)
    except UserEntry.DoesNotExist:
        return HttpResponseRedirect('/ncaa/')

    teams = []
    total_score = 0
    
    user_teams = UserTeam.objects.filter(entry=entry)
    for user_team in user_teams:
        team_score = user_team.team.score * user_team.count
        total_score += team_score
        teams.append((user_team.team, user_team.count, team_score))
    
    teams = sorted(teams, key=lambda x: x[0].team.abbrev_name)
    return render_with_request_context(request, 'entry.html', { 'entry':entry, 'teams':teams, 'total_score':total_score })


def marketplace(request, game_id):
    try:
        game = NcaaGame.objects.get(id=game_id)
    except NcaaGame.DoesNotExist:
        return HttpResponseRedirect('/ncaa/')
    
    offers_query = Q(entry__game=game)

    ask_filter = request.GET.get('ask_filter', '')
    bid_filter = request.GET.get('bid_filter', '')

    if ask_filter:
        offers_query = offers_query & Q(ask_side__components__team__abbrev_name__iexact=ask_filter)
    if bid_filter:
        offers_query = offers_query & Q(bid_side__components__team__abbrev_name__iexact=bid_filter)

    offers = TradeOffer.objects.filter(offers_query)

    return HttpResponseRedirect('/ncaa/')
    #return render_with_request_context(request, 'marketplace.html', { 'game'=game, 'offers'=offers })
