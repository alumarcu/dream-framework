from django.test import TestCase
from dream.core.models import *

class CoreModelsTestCase(TestCase):
    def setUp(self):
        Sport.objects.create(name='Association Football', common_key='soccer')

    def test_soccer_is_association_football(self):
        """A dummy test. Checks that 'soccer' common key resolves to Association Football"""
        s = Sport.objects.get(common_key='soccer')
        self.assertNotEqual(s.name, "American Football")
        self.assertEqual(s.name, "Association Football")
