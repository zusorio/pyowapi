from unittest import TestCase
import asyncio
import pyowapi


class TestAPI(TestCase):
    def test_api_working(self):
        loop = asyncio.get_event_loop()
        player = loop.run_until_complete(pyowapi.get_player("Jayne#1447"))
        self.assertTrue(player.success)
        self.assertTrue(isinstance(player.actual_level, int))
