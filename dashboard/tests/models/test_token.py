from django.test import TestCase

from dashboard.models import Token

class TokenTests(TestCase):

  fixtures = ["simple_tokens.yaml"]

  def test_some_dumb_test(self):
    print(Token.objects.all().count())
