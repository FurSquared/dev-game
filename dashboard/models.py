from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils import timezone

alphanumeric_validator = RegexValidator(r'^[0-9a-zA-Z_-]*$', 'Only alphanumeric, underscore, and dash are allowed.')


class Token(models.Model):
  def __str__(self):
    return self.code

  code = models.CharField(max_length=25, primary_key=True, validators=[alphanumeric_validator])
  gm_note = models.TextField(blank=True)
  reward_text = models.TextField(blank=True)
  valid_from = models.DateTimeField(blank=True, null=True)

  def save(self, *args, **kwargs):
    self.code = self.code.upper().replace("-", "_")

    super().save(*args, **kwargs)


class CollectedToken(models.Model):
  def __str__(self):
    return f"{self.user} | {self.token}"

  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
  token = models.ForeignKey(Token, on_delete=models.DO_NOTHING)
  read = models.BooleanField(default=False)
  collected_at = models.DateTimeField(default=timezone.now)

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    user_token_count = CollectedToken.objects.filter(user=self.user).count()
    user_rewards = [cr.reward.id for cr in CollectedReward.objects.filter(user=self.user)]

    for reward in Reward.objects.exclude(id__in=user_rewards).filter(count__gt=0, count__lte=user_token_count):
      CollectedReward.objects.create(user=self.user, reward=reward)

    for reward in Reward.objects.exclude(id__in=user_rewards).filter(required_tokens__isnull=False).distinct():
      collected_tokens = CollectedToken.objects.filter(user=self.user, token__in=reward.required_tokens.all())
      count = CollectedToken.objects.filter(user=self.user, token__in=reward.required_tokens.all()).count()
      if count == reward.required_tokens.count():
        CollectedReward.objects.create(user=self.user, reward=reward)

  class Meta:
    indexes = [
      models.Index(fields=['user', 'token']),
      models.Index(fields=['user']),
      models.Index(fields=['token']),
    ]
    unique_together = [['user', 'token']]


class Reward(models.Model):
  def __str__(self):
    return self.name

  name = models.CharField(max_length=255)
  #save time
  count = models.PositiveIntegerField(default=0)
  required_tokens = models.ManyToManyField(Token, blank=True)

  #page load time
  valid_from = models.DateTimeField(blank=True, null=True)
  gm_note = models.TextField(blank=True)
  reward_text = models.TextField(blank=True)

  class Meta:
    indexes = [
      models.Index(fields=['count']),
    ]


class CollectedReward(models.Model):
  def __str__(self):
    return f"{self.user} | {self.reward}"

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
    unique_together = [['user', 'reward']]
