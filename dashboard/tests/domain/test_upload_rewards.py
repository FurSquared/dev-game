import csv

from django.test import TestCase

from dashboard.domain import process_csv_codes, process_csv_rewards
from dashboard.models import Token, Reward

from dashboard.tests.util import get_file_lines

class UploadCsvRewardsTests(TestCase):

    fixtures = ["simple_tokens.yaml"]

    def test_upload_once(self):
        decoded_file = get_file_lines(__file__, 'rewards.csv')
        reader = csv.DictReader(decoded_file)

        keys, new_codes, updated_codes = process_csv_rewards(reader)
        self.assertEqual(len(new_codes), 2)
        self.assertEqual(len(updated_codes), 0)

        reward = Reward.objects.all()[0]
        self.assertEqual(reward.reward_text, 'twosies')

    def test_upload_twice(self):
        decoded_file_1 = get_file_lines(__file__, 'rewards.csv')
        decoded_file_2 = get_file_lines(__file__, 'rewards_update.csv')

        reader_1 = csv.DictReader(decoded_file_1)
        reader_2 = csv.DictReader(decoded_file_2)

        process_csv_rewards(reader_1)
        keys, new_rewards, updated_rewards = process_csv_rewards(reader_2)
        self.assertEqual(len(new_rewards), 0)
        self.assertEqual(len(updated_rewards), 2)

        reward = Reward.objects.all()[1]
        self.assertEqual(reward.reward_text, 'rawrteries')
