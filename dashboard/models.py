from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils import timezone

alphanumeric_validator = RegexValidator(r'^[0-9a-zA-Z_-]*$', 'Only alphanumeric, underscore, and dash are allowed.')


class Token(models.Model):
  code = models.CharField(max_length=25, primary_key=True, validators=[alphanumeric_validator])
  gm_note = models.TextField(blank=True)
  reward_text = models.TextField(blank=True)
  valid_from = models.DateTimeField(blank=True, null=True)

  def save(self, *args, **kwargs):
    self.code = self.code.upper().replace("-", "_")

    super().save(*args, **kwargs)


class CollectedToken(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
  token = models.ForeignKey(Token, on_delete=models.DO_NOTHING)
  read = models.BooleanField(default=False)
  collected_at = models.DateTimeField(default=timezone.now)

  class Meta:
    indexes = [
      models.Index(fields=['user', 'token']),
      models.Index(fields=['user']),
      models.Index(fields=['token']),
    ]


class Reward(models.Model):
  #save time
  count = models.PositiveIntegerField(default=0)
  required_tokens = models.ManyToManyField(Token)

  #page load time
  valid_from = models.DateTimeField(blank=True)
  gm_note = models.TextField(blank=True)
  reward_text = models.TextField(blank=True)

  class Meta:
    indexes = [
      models.Index(fields=['count']),
    ]


class CollectedReward(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
  reward = models.ForeignKey(Reward, on_delete=models.DO_NOTHING)
  read = models.BooleanField(default=False)
  collected_at = models.DateTimeField(default=timezone.now)

  class Meta:
    indexes = [
      models.Index(fields=['user']),
      models.Index(fields=['user', 'reward']),
      models.Index(fields=['reward']),
    ]
