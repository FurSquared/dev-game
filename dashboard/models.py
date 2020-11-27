from django.db import models
from django.utils import timezone


class Tokens(models.Model):
    token = models.CharField(max_length=25, primary_key=True)


class TokensCollected(models.Model):
    userid = models.IntegerField()
    token = models.ForeignKey(Tokens, on_delete=models.DO_NOTHING)
    collected_at = models.DateTimeField(default=timezone.now)
