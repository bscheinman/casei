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


class UserEntry(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(NcaaGame)
    entry_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.entry_name

    def get_score(self):
        points = 0
        for team in self.user_teams:
            points += team.team.score * team.count
        return points


class Team(models.Model):
    full_name = models.CharField(max_length=50)
    abbrev_name = models.CharField(max_length=6)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.abbrev_name


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

@receiver(post_save, sender=UserEntry, weak=False)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        TradingBlock.objects.create(entry=instance)
        for team in Team.objects.all():
            UserTeam.objects.create(entry=instance, team=team, count=instance.game.starting_shares)
