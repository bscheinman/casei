from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class NcaaGame(models.Model):
    name = models.CharField(max_length=50)
    # Storing these in plain text for now
    password = models.CharField(blank=True, null=True, max_length=100)
    starting_shares = models.IntegerField(default=100)
    starting_money = models.IntegerField(default=0)


class ScoreType(models.Model):
    name = models.CharField(max_length=30)
    default_score = models.IntegerField()


class ScoringSetting(models.Model):
    game = models.ForeignKey(NcaaGame)
    scoreType = models.ForeignKey(ScoreType)
    points = models.IntegerField()


class UserEntry(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(NcaaGame)
    entry_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.entry_name

    def get_score(self):
        points = 0
        for team in self.user_teams:
            points += team.team.get_score() * team.count
        return points


class Team(models.Model):
    full_name = models.CharField(max_length=50)
    abbrev_name = models.CharField(max_length=6)

    def __str__(self):
        return self.abbrev_name


class GameTeam(models.Model):
    game = models.ForeignKey(NcaaGame)
    team = models.ForeignKey(Team)
    score = models.IntegerField(default=0)

    # We could pass in the multipliers for the team to the method so we don't need to make that db call for each game
    def update_score(self):
        score = 0
        counts = self.counts
        multipliers = ScoringSetting.objects.filter(game=self.game)
        for scoreType in ScoreType.objects.all():
            count = counts.get(scoreType=scoreType)
            multiplier = multipliers.get(scoreType=scoreType)
            score += count * multiplier
        return score
        


class TeamScoreCount(models.Model):
    team = models.ForeignKey(Team, related_name='counts')
    scoreType = models.ForeignKey(ScoreType)
    count = models.IntegerField(default=0)


class UserTeam(models.Model):
    entry = models.ForeignKey(UserEntry)
    team = models.ForeignKey(Team)
    count = models.IntegerField()


class TradingBlock(models.Model):
    entry = models.OneToOneField(UserEntry)
    teams_desired = models.ManyToManyField(Team, related_name='desired_blocks')
    teams_available = models.ManyToManyField(Team, related_name='available_blocks')


class TradeSide(models.Model):
    dollar_amount = models.IntegerField(blank=True, null=True)


class TradeOffer(models.Model):
    user = models.ForeignKey(User)
    bid_side = models.OneToOneField(TradeSide, related_name='bid_offer')
    ask_side = models.OneToOneField(TradeSide, related_name='ask_offer')


class TradeComponent(models.Model):
    team = models.ForeignKey(Team)
    count = models.IntegerField()
    offer = models.ForeignKey(TradeSide)

admin.site.register(Team)
admin.site.register(UserTeam)
admin.site.register(ScoreType)

@receiver(post_save, sender=UserEntry, weak=False)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        TradingBlock.objects.create(entry=instance)
        for team in Team.objects.all():
            UserTeam.objects.create(entry=instance, team=team, count=instance.game.starting_shares)


# Whenever a team's wins are updated, update the score for that team
@receiver(post_save, sender=TeamScoreCount, weak=False)
def update_team_scores(sender, instance, create, **kwargs):
    for team in GameTeam.objects.filter(team=instance.team):
        team.update_score()
