import pytz

from datetime import timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from dashboard.models import Token

TIME_ZONE_OBJ = pytz.timezone(settings.TIME_ZONE)


class TokenTests(TestCase):
    fixtures = ["simple_tokens.yaml"]

    def test_some_dumb_test(self):
        self.assertEqual(Token.objects.all().count(), 4)

    def test_valid_code(self):
        token = Token.objects.create(code="BLAH", reward_text="A Reward!")

        self.assertEqual(token.code, "BLAH")

    def test_valid_code_but_changed(self):
        token = Token.objects.create(code="blah-bl-arg", reward_text="A Reward!")

        self.assertEqual(token.code, "BLAH_BL_ARG")

    def test_invalid_code(self):
        with self.assertRaises(ValidationError):
            token = Token(code="bl%ah", reward_text="A Reward!")
            token.full_clean()

    def test_code_date_before(self):
        token = Token.objects.get(code="GM_REWARD_DATE")
        token.valid_from = timezone.now() + timedelta(hours=2)
        token.save()

        self.assertEqual(token.user_reward.find("This reward unlocks at "), 0)

    def test_code_date_after(self):
        token = Token.objects.get(code="GM_REWARD_DATE")

        self.assertEqual(token.user_reward, "rawr")
