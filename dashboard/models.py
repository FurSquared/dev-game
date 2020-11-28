from django.db import models
from django.conf import settings
from django.utils import timezone


class Token(models.Model):
    code = models.CharField(max_length=25, primary_key=True)
    gm_note = models.TextField(blank=True)
    reward_text = models.TextField(blank=True)
    valid_from = models.DateTimeField(blank=True, null=True)

class CollectedToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    token = models.ForeignKey(Token, on_delete=models.DO_NOTHING)
    read = models.BooleanField(default=False)
    collected_at = models.DateTimeField(default=timezone.now)

class Reward(models.Model):
    #save time
    count = models.PositiveIntegerField(default=0)
    required_tokens = models.ManyToManyField(Token)

    #page load time
    valid_from = models.DateTimeField(blank=True)
    gm_note = models.TextField(blank=True)
    reward_text = models.TextField(blank=True)

class CollectedReward(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    reward = models.ForeignKey(Reward, on_delete=models.DO_NOTHING)
    read = models.BooleanField(default=False)
    collected_at = models.DateTimeField(default=timezone.now)

