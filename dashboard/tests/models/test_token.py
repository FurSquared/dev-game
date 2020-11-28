from django.core.exceptions import ValidationError
from django.test import TestCase

from dashboard.models import Token

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
