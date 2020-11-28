from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from dashboard.models import Token, CollectedToken

class SubmitTokenTests(TestCase):

  fixtures = ["simple_tokens.yaml"]

  def setUp(self):
    self.user = get_user_model().objects.create_user(username="testy", email="testy@nowhere.bees")
    self.user.set_password("testy_pass")
    self.user.save()
    self.client = Client()

  def test_login_required(self):
    response = self.client.get('/dashboard/enter_code')

    self.assertEqual(response.status_code, 302)

  def test_successful_code(self):
    self.client.login(username="testy", password="testy_pass")

    response = self.client.post('/dashboard/enter_code', {'code': "REWARD_ONLY"})

    collected_tokens = CollectedToken.objects.filter(user=self.user)

    self.assertEqual(collected_tokens.count(), 1)

  def test_invalid_code(self):
    self.client.login(username="testy", password="testy_pass")

    response = self.client.post('/dashboard/enter_code', {'code': "NOT_A_REAL_CODE"})

    collected_tokens = CollectedToken.objects.filter(user=self.user)

    self.assertEqual(collected_tokens.count(), 0)
