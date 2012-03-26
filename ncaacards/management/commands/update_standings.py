from casei.ncaacards.models import GameType, ScoreType, Team, TeamScoreCount
from django.core.management.base import NoArgsCommand
import datetime
import json
import re
import urllib2


class Command(NoArgsCommand):
    
    team_names = {
        'kan' : 'KC',
        'sdg' : 'SD',
        'sfo' : 'SF',
        'tam' : 'TB',
    }
    game_type = GameType.objects.get(name='MLB')
    url = 'http://sports.yahoo.com/mlb/standings'
    regex = re.compile('<a href="/mlb/teams/(?P<name>[a-z]+)" ?>[A-Za-z ]+</a>\s+</td>\s+<td>\s+(?P<wins>[0-9]+)\s+</td>\s+<td>\s+(?P<losses>[0-9]+)\s+</td>')
    wins_type, losses_type = ScoreType.objects.get(name='Wins'), ScoreType.objects.get(name='Losses')


    def get_team(self, team_name):
        return Team.objects.get(game_type=self.game_type, abbrev_name=self.team_names.get(team_name, team_name.upper()))

    def handle_noargs(self, **options):
        html = urllib2.urlopen(self.url).read()
        matches = self.regex.finditer(html)
        for match in matches:
            try:
                team = self.get_team(match.group('name'))
                wins, losses = TeamScoreCount.objects.get(team=team, scoreType=self.wins_type), TeamScoreCount.objects.get(team=team, scoreType=self.losses_type)
                wins.count = int(match.group('wins'))
                wins.save()
                losses.count = int(match.group('losses'))
                losses.save()
            except Exception as err:
                print 'Error processing team %s: %s' % (match.group('name'), str(err))
