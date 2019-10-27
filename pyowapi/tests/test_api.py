from unittest import TestCase
import pyowapi


class TestAPI(TestCase):
    def test_api_working(self):
        player = pyowapi.get_player("Jayne#1447")
        print(player)
        self.assertTrue(player.success)
        self.assertTrue(isinstance(player.actual_level, int))
