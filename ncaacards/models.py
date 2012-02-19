from django.contrib.auth.models import User
from django.db import models

class Team(models.Model):
    full_name = models.CharField(max_length=50)
    abbrev_name = models.CharField(max_length=6)
    score = models.IntegerField(default=0)


class UserTeam(models.Model):
    user = models.ForeignKey(User)
    team = models.ForeignKey(Team)
    count = models.IntegerField(default=0)


class TradingBlock(models.Model):
    user = models.ForeignKey(User)
    teams_desired = models.ManyToManyField(Team, related_name='desired_blocks')
    teams_available = models.ManyToManyField(Team, related_name='available_blocks')


class TradeSide(models.Model):
    pass


class TradeOffer(models.Model):
    user = models.ForeignKey(User)
    bid_side = models.OneToOneField(TradeSide, related_name='bid_offer')
    ask_side = models.OneToOneField(TradeSide, related_name='ask_offer')


class TradeComponent(models.Model):
    team = models.ForeignKey(Team)
    count = models.IntegerField()
    offer = models.ForeignKey(TradeSide)
