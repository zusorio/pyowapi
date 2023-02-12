from unittest import TestCase
import pyowapi


class TestAPI(TestCase):
    def test_single_player(self):
        player = pyowapi.get_player("Zusor#2553")
        self.assertTrue(player.success)

    def test_multiple_players(self):
        players = pyowapi.get_player(["Solomon#2456", "Zusor#2553"])
        for player in players:
            self.assertTrue(player.success)

    def test_incorrect_player(self):
        player = pyowapi.get_player("zusor#2553")
        self.assertFalse(player.success)

    def test_correcting_player(self):
        player = pyowapi.get_player("zusor#2553", correct_player=True)
        self.assertTrue(player.success)
        self.assertTrue(player.player_name == "Zusor#2553")
        player2 = pyowapi.get_player("knockonwood0#1234", correct_player=True)
        self.assertTrue(player2.success)
        self.assertFalse(player2.player_name == player2.original_player_name)
        self.assertTrue(player2.player_name == "Knockonwood0#1345")
