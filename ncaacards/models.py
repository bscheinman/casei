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
