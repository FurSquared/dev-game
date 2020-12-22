import csv

from django.test import TestCase

from dashboard.domain import process_csv_codes
from dashboard.models import Token

from dashboard.tests.util import get_file_lines

class UploadCsvCodesTests(TestCase):

    def test_upload_once(self):
        decoded_file = get_file_lines(__file__, 'codes.csv')
        reader = csv.DictReader(decoded_file)

        keys, new_codes, updated_codes = process_csv_codes(reader)
        self.assertEqual(len(new_codes), 1)
        self.assertEqual(len(updated_codes), 0)

        token = Token.objects.all()[0]
        self.assertEqual(token.reward_text, 'reward message')

    def test_upload_twice(self):
        decoded_file_1 = get_file_lines(__file__, 'codes.csv')
        decoded_file_2 = get_file_lines(__file__, 'codes_update.csv')

        reader_1 = csv.DictReader(decoded_file_1)
        reader_2 = csv.DictReader(decoded_file_2)

        process_csv_codes(reader_1)
        keys, new_codes, updated_codes = process_csv_codes(reader_2)
        self.assertEqual(len(new_codes), 0)
        self.assertEqual(len(updated_codes), 1)

        token = Token.objects.all()[0]
        self.assertEqual(token.reward_text, 'revised message')
