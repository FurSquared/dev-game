from django.test import Client, TestCase
from django.contrib.staticfiles import finders


class BasicPageTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_favicon(self):
        response = self.client.get('/favicon.ico')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/static/favicon.ico')

        # There is no "definitive" way to check statics in test mode
        absolute_path = finders.find('favicon.ico')
        assert absolute_path is not None
        assert absolute_path.endswith('/static/favicon.ico')
