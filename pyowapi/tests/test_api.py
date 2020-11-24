from unittest import TestCase
import pyowapi


class TestAPI(TestCase):
    def test_single_player(self):
        player = pyowapi.get_player("Jayne#1447")
        self.assertTrue(player.success)

    def test_single_player_playstation(self):
        player = pyowapi.get_player("R3flexTube", platform="psn")
        self.assertTrue(player.success)

    def test_single_player_xbox(self):
        player = pyowapi.get_player("VeX I Ninja", platform="xbl")
        self.assertTrue(player.success)

    def test_multiple_players(self):
        players = pyowapi.get_player(["Jayne#1447", "Zusor#2553"])
        for player in players:
            self.assertTrue(player.success)

    def test_multiple_players_playstation(self):
        players = pyowapi.get_player(["R3flexTube", "Savage_DadD"], platform="psn")
        for player in players:
            self.assertTrue(player.success)

    def test_multiple_players_xbox(self):
        players = pyowapi.get_player(["VeX I Ninja", "MunchingCarrot"], platform="xbl")
        for player in players:
            self.assertTrue(player.success)

    def test_incorrect_player(self):
        player = pyowapi.get_player("jayne#1447")
        self.assertFalse(player.success)
        player2 = pyowapi.get_player("r3flextube", platform="psn")
        self.assertFalse(player2.success)

    def test_correcting_player(self):
        player = pyowapi.get_player("jayne#1447", correct_player=True)
        self.assertTrue(player.success)
        self.assertTrue(player.player_name == "Jayne#1447")
        player2 = pyowapi.get_player("zusor#1234", correct_player=True)
        self.assertTrue(player2.success)
        self.assertFalse(player2.player_name == player2.original_player_name)
        self.assertTrue(player2.player_name == "Zusor#2553")
