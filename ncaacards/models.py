from casei.trading.models import Execution, Market, Security
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

class GameType(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class NcaaGame(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # Storing these in plain text for now
    password = models.CharField(blank=True, null=True, max_length=100)
    starting_shares = models.IntegerField(default=100)
    starting_points = models.IntegerField(default=0)
    game_type = models.ForeignKey(GameType, related_name='games')

    def __str__(self):
        return self.name


class ScoreType(models.Model):
    name = models.CharField(max_length=30)
    default_score = models.IntegerField()
    ordering = models.IntegerField(unique=True) # this is for creating a manual ordering
    game_type = models.ForeignKey(GameType, related_name='score_types')

    def __str__(self):
        return self.name


class ScoringSetting(models.Model):
    game = models.ForeignKey(NcaaGame)
    scoreType = models.ForeignKey(ScoreType)
    points = models.IntegerField()


class UserEntry(models.Model):
    user = models.ForeignKey(User, related_name='entries')
    game = models.ForeignKey(NcaaGame, related_name='entries')
    entry_name = models.CharField(max_length=30)
    extra_points = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('game', 'entry_name')
    
    def __str__(self):
        return self.entry_name

    def update_score(self):
        points = self.extra_points
        for team in self.teams.all():
            points += team.team.score * team.count
        self.score = points
        self.save()


class Team(models.Model):
    full_name = models.CharField(max_length=50, unique=True)
    abbrev_name = models.CharField(max_length=6, unique=True)
    game_type = models.ForeignKey(GameType, related_name='teams')

    def __str__(self):
        return self.full_name


class GameTeam(models.Model):
    game = models.ForeignKey(NcaaGame)
    team = models.ForeignKey(Team)
    score = models.IntegerField(default=0)

    def __str__(self):
        return '%s (%s)' % (self.team.full_name, self.game.name)

    # We could pass in the multipliers for the team to the method so we don't need to make that db call for each game
    def update_score(self):
        points = 0
        counts = self.team.counts
        multipliers = ScoringSetting.objects.filter(game=self.game)
        for scoreType in ScoreType.objects.all():
            count = counts.get(scoreType=scoreType).count
            multiplier = multipliers.get(scoreType=scoreType).points
            points += count * multiplier
        self.score = points 
        self.save()
        


class TeamScoreCount(models.Model):
    team = models.ForeignKey(Team, related_name='counts')
    scoreType = models.ForeignKey(ScoreType)
    count = models.IntegerField(default=0)

    def __str__(self):
        return '%s-- %s' % (self.team.full_name, self.scoreType.name)


class UserTeam(models.Model):
    entry = models.ForeignKey(UserEntry, related_name='teams')
    team = models.ForeignKey(GameTeam)
    count = models.IntegerField()

    def __str__(self):
        return '%s: %s' % (self.entry.entry_name, self.team.team.abbrev_name)


class TradingBlock(models.Model):
    entry = models.OneToOneField(UserEntry, related_name='trading_block')
    game_teams_desired = models.ManyToManyField(GameTeam, related_name='desired_blocks')
    game_teams_available = models.ManyToManyField(GameTeam, related_name='available_blocks')

    def __str__(self):
        return '%s\'s Trading Block' % self.entry.user.username


class TradeSide(models.Model):
    points = models.IntegerField(blank=True, null=True)


class TradeOffer(models.Model):
    entry = models.ForeignKey(UserEntry, related_name='proposed_trades')
    bid_side = models.OneToOneField(TradeSide, related_name='bid_offer')
    ask_side = models.OneToOneField(TradeSide, related_name='ask_offer')
    accepting_user = models.ForeignKey(UserEntry, blank=True, null=True, related_name='accepted_trades')
    offer_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    accept_time = models.DateTimeField(blank=True, null=True)

    def is_accepted(self):
        return bool(self.accepting_user)


class TradeComponent(models.Model):
    team = models.ForeignKey(GameTeam)
    count = models.IntegerField()
    offer = models.ForeignKey(TradeSide, related_name='components')

    def get_score(self):
        return self.count * self.team.score

admin.site.register(NcaaGame)
admin.site.register(Team)
admin.site.register(UserTeam)
admin.site.register(ScoreType)
admin.site.register(TradingBlock)
admin.site.register(UserEntry)
admin.site.register(TeamScoreCount)
admin.site.register(GameTeam)
admin.site.register(ScoringSetting)
admin.site.register(TradeOffer)
admin.site.register(TradeSide)
admin.site.register(TradeComponent)
admin.site.register(GameType)

@receiver(post_save, sender=UserEntry, weak=False)
def complete_user_entry(sender, instance, created, **kwargs):
    if created:
        TradingBlock.objects.create(entry=instance)
        for team in GameTeam.objects.filter(game=instance.game):
            UserTeam.objects.create(entry=instance, team=team, count=instance.game.starting_shares)
        instance.extra_points = instance.game.starting_points
        instance.save()


# Whenever a team's wins are updated, update the score for that team
@receiver(post_save, sender=TeamScoreCount, weak=False)
def update_team_scores(sender, instance, created, **kwargs):
    for team in GameTeam.objects.filter(team=instance.team):
        team.update_score()
    for entry in UserEntry.objects.all():
        entry.update_score()


@receiver(post_save, sender=NcaaGame, weak=False)
def populate_game(sender, instance, created, **kwargs):
    if created:
        market = Market.objects.create(name=instance.name)
        for team in Team.objects.filter(game_type=instance.game_type):
            GameTeam.objects.create(game=instance, team=team)
            Security.objects.create(market=market, name=team.abbrev_name)
        for scoreType in ScoreType.objects.filter(game_type=instance.game_type):
            ScoringSetting.objects.create(game=instance, scoreType=scoreType, points=scoreType.default_score)


@receiver(post_save, sender=Team, weak=False)
def create_team_counts(sender, instance, created, **kwargs):
    if created:
        for scoreType in ScoreType.objects.filter(game_type=instance.game_type):
            TeamScoreCount.objects.create(team=instance, scoreType=scoreType)


@receiver(post_save, sender=Execution, weak=False)
def record_execution(sender, instance, created, **kwargs):
    if created:
        try:
            game = NcaaGame.get(name=instance.name)
            buyer = UserEntry.get(game=game, entry_name=instance.placer)
            seller = UserEntry.get(game=game, entry_name=instance.placer)
            team = Team.get(name=instance.security.name)
            game_team = GameTeam.get(game=game, team=team)

            buyer_count = UserTeam.get(team=game_team, entry=buyer)
            buyer_count.count += instance.quantity
            buyer_count.save()

            seller_count = UserTeam.get(team=game_team, entry=buyer)
            seller_count.count -= instance.quantity
            seller_count.save()
        except Exception as e:
            logger.error('Error processing execution %s: %s' % (instance.execution_id, str(e)))
