import pytz

from datetime import timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from dashboard.models import Token, Reward, CollectedToken, CollectedReward

TIME_ZONE_OBJ = pytz.timezone(settings.TIME_ZONE)


class RewardTests(TestCase):
    fixtures = ["simple_tokens.yaml", "simple_rewards"]

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testy", email="testy@nowhere.bees")

    def test_some_dumb_test(self):
        self.assertEqual(Reward.objects.all().count(), 2)

    def test_reward_date_before(self):
        token = Token.objects.get(code="GM_ONLY")
        token.valid_from = timezone.now() + timedelta(hours=2)
        token.save()

        CollectedToken.objects.create(
            user=self.user,
            token=token,
        )
        CollectedToken.objects.create(
            user=self.user,
            token=Token.objects.get(code='GM_REWARD'),
        )
        collected_token = CollectedToken(
            user=self.user,
            token=Token.objects.get(code='REWARD_ONLY'),
        )
        collected_token.save()

        collected_reward = CollectedReward.objects.get(reward__name='Required Token Reward')

        self.assertEqual(collected_reward.reward.user_reward.find('This reward unlocks at '), 0)

    def test_reward_date_after(self):
        token = Token.objects.get(code="GM_ONLY")

        CollectedToken.objects.create(
            user=self.user,
            token=token,
        )
        CollectedToken.objects.create(
            user=self.user,
            token=Token.objects.get(code='GM_REWARD'),
        )
        collected_token = CollectedToken(
            user=self.user,
            token=Token.objects.get(code='REWARD_ONLY'),
        )
        collected_token.save()

        collected_reward = CollectedReward.objects.get(reward__name='Required Token Reward')

        self.assertEqual(collected_reward.reward.user_reward, 'honk honk')
