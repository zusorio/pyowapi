import asyncio
import aiohttp
from typing import List


class Player:
    def __init__(self, bnet, response):
        self.bnet = bnet
        self.success = "error" not in response
        if self.success:
            self.level = response["level"]
            self.prestige = response["prestige"]
            self.actual_level = self.prestige * 100 + self.level
            self.private = response["private"]
            self.endorsement = response["endorsement"]

            if not self.private:
                self.quickplay_stats = response["competitiveStats"]
                self.quickplay_cards = self.quickplay_stats["awards"]["cards"]
                self.quickplay_medals = self.quickplay_stats["awards"]["medals"]
                self.quickplay_medals_bronze = self.quickplay_stats["awards"]["medalsBronze"]
                self.quickplay_medals_silver = self.quickplay_stats["awards"]["medalsSilver"]
                self.quickplay_medals_gold = self.quickplay_stats["awards"]["medalsGold"]
                self.quickplay_games_won = self.quickplay_stats["games"]["won"]

                self.competitive_stats = response["competitiveStats"]
                self.competitive_cards = self.competitive_stats["awards"]["cards"]
                self.competitive_medals = self.competitive_stats["awards"]["medals"]
                self.competitive_medals_bronze = self.competitive_stats["awards"]["medalsBronze"]
                self.competitive_medals_silver = self.competitive_stats["awards"]["medalsSilver"]
                self.competitive_medals_gold = self.competitive_stats["awards"]["medalsGold"]
                self.competitive_games_played = self.competitive_stats["games"]["played"]
                self.competitive_games_won = self.competitive_stats["games"]["won"]

                self.competitive_tank = False
                self.competitive_damage = False
                self.competitive_support = False

                if response["ratings"]:
                    for rating in response["ratings"]:
                        if rating["role"] == "tank":
                            self.competitive_tank = rating["level"]
                        if rating["role"] == "damage":
                            self.competitive_damage = rating["level"]
                        if rating["role"] == "support":
                            self.competitive_support = rating["level"]

    def __repr__(self):
        return f"<Player {self.bnet} success: {self.success}>"


async def _get_player_internal(player: str, session):
    try:
        async with session.get(f"https://ow-api.com/v1/stats/pc/eu/{player.replace('#', '-')}/profile") as resp:
            data = await resp.json()
            return Player(player, data)
    except TimeoutError:
        return Player(player, {"error": "timeout"})


async def _get_player(player: str) -> Player:
    async with aiohttp.ClientSession() as session:
        result = await _get_player_internal(player, session)
        return result


def get_player(player: str):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(_get_player(player))
    return result


async def _get_bulk_players(players: list) -> List[Player]:
    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(*[_get_player_internal(player, session) for player in players])
        return result


def get_bulk_players(players: list) -> List[Player]:
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(_get_bulk_players(players))
    return result
