from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class NcaaGame(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # Storing these in plain text for now
    password = models.CharField(blank=True, null=True, max_length=100)
    starting_shares = models.IntegerField(default=100)
    starting_points = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class ScoreType(models.Model):
    name = models.CharField(max_length=30)
    default_score = models.IntegerField()
    ordering = models.IntegerField(unique=True) # this is for creating a manual ordering

    def __str__(self):
        return self.name


class ScoringSetting(models.Model):
    game = models.ForeignKey(NcaaGame)
    scoreType = models.ForeignKey(ScoreType)
    points = models.IntegerField()


class UserEntry(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(NcaaGame)
    entry_name = models.CharField(max_length=30)
    extra_points = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('game', 'entry_name')
    
    def __str__(self):
        return self.entry_name

    def update_score(self):
        points = 0
        for team in self.teams.all():
            points += team.team.score * team.count
        self.score = points
        self.save()


class Team(models.Model):
    full_name = models.CharField(max_length=50, unique=True)
    abbrev_name = models.CharField(max_length=6, unique=True)

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
        import pdb; pdb.set_trace()
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
    entry = models.OneToOneField(UserEntry)
    teams_desired = models.ManyToManyField(Team, related_name='desired_blocks')
    teams_available = models.ManyToManyField(Team, related_name='available_blocks')

    def __str__(self):
        return '%s\'s Trading Block' % self.entry.user.username


class TradeSide(models.Model):
    points = models.IntegerField(blank=True, null=True)


class TradeOffer(models.Model):
    entry = models.ForeignKey(UserEntry, related_name='proposed_trades')
    bid_side = models.OneToOneField(TradeSide, related_name='bid_offer')
    ask_side = models.OneToOneField(TradeSide, related_name='ask_offer')
    accepting_user = models.ForeignKey(UserEntry, blank=True, null=True, related_name='accepted_trades')

    def is_accepted(self):
        return bool(self.accepting_user)


class TradeComponent(models.Model):
    team = models.ForeignKey(Team, related_name='components')
    count = models.IntegerField()
    offer = models.ForeignKey(TradeSide)

admin.site.register(NcaaGame)
admin.site.register(Team)
admin.site.register(UserTeam)
admin.site.register(ScoreType)
admin.site.register(TradingBlock)
admin.site.register(UserEntry)
admin.site.register(TeamScoreCount)
admin.site.register(GameTeam)
admin.site.register(ScoringSetting)

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
        for team in Team.objects.all():
            GameTeam.objects.create(game=instance, team=team)


@receiver(post_save, sender=Team, weak=False)
def create_team_counts(sender, instance, created, **kwargs):
    if created:
        for scoreType in ScoreType.objects.all():
            TeamScoreCount.objects.create(team=instance, scoreType=scoreType)


# Once we're actually processing trades, we should remove this and specifically
# call update_score after each trade
@receiver(post_save, sender=UserTeam, weak=False)
def reflect_trade(sender, instance, created, **kwargs):
    instance.entry.update_score()
