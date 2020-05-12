from unittest import TestCase
import pyowapi


class TestAPI(TestCase):
    def test_single_player(self):
        player = pyowapi.get_player("Jayne#1447")
        print(player)
        self.assertTrue(player.success)
        self.assertTrue(isinstance(player.actual_level, int))

    def test_multiple_players(self):
        players = pyowapi.get_bulk_players(["Jayne#1447"])
        for player in players:
            self.assertTrue(player.success)
            self.assertTrue(isinstance(player.actual_level, int))