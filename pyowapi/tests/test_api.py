from unittest import TestCase
import pyowapi


class TestAPI(TestCase):
    def test_single_player(self):
        player = pyowapi.get_player("Jayne#1447")
        self.assertTrue(player.success)
        self.assertTrue(isinstance(player.actual_level, int))

    def test_single_player_playstation(self):
        player = pyowapi.get_player("R3flexTube", platform="psn")
        self.assertTrue(player.success)
        self.assertTrue(isinstance(player.actual_level, int))

    def test_single_player_xbox(self):
        player = pyowapi.get_player("VeX I Ninja", platform="xbl")
        self.assertTrue(player.success)
        self.assertTrue(isinstance(player.actual_level, int))

    def test_multiple_players(self):
        players = pyowapi.get_player(["Jayne#1447", "Zusor#2553"])
        for player in players:
            self.assertTrue(player.success)
            self.assertTrue(isinstance(player.actual_level, int))

    def test_multiple_players_playstation(self):
        players = pyowapi.get_player(["R3flexTube", "Savage_DadD"], platform="psn")
        for player in players:
            self.assertTrue(player.success)
            self.assertTrue(isinstance(player.actual_level, int))

    def test_multiple_players_xbox(self):
        players = pyowapi.get_player(["VeX I Ninja", "MunchingCarrot"], platform="xbl")
        for player in players:
            self.assertTrue(player.success)
            self.assertTrue(isinstance(player.actual_level, int))

    def test_correct_player(self):
        players = pyowapi.get_player(["VeX I Ninja", "MunchingCarrot"], platform="xbl")
        for player in players:
            self.assertTrue(player.success)
            self.assertTrue(isinstance(player.actual_level, int))

