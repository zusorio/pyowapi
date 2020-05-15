import asyncio
import aiohttp
from typing import List, Union


class Player:
    def __init__(self, bnet: str, response: dict):
        self.bnet: str = bnet
        self.success: bool = "error" not in response
        if self.success:
            self.level: int = response["level"]
            self.prestige: int = response["prestige"]
            self.actual_level: int = self.prestige * 100 + self.level
            self.private: bool = response["private"]
            self.endorsement: int = response["endorsement"]

            if not self.private:
                self.quickplay_stats: dict = response["competitiveStats"]
                self.quickplay_cards: int = self.quickplay_stats["awards"]["cards"]
                self.quickplay_medals: int = self.quickplay_stats["awards"]["medals"]
                self.quickplay_medals_bronze: int = self.quickplay_stats["awards"]["medalsBronze"]
                self.quickplay_medals_silver: int = self.quickplay_stats["awards"]["medalsSilver"]
                self.quickplay_medals_gold: int = self.quickplay_stats["awards"]["medalsGold"]
                self.quickplay_games_won: int = self.quickplay_stats["games"]["won"]

                self.competitive_stats: dict = response["competitiveStats"]
                self.competitive_cards: int = self.competitive_stats["awards"]["cards"]
                self.competitive_medals: int = self.competitive_stats["awards"]["medals"]
                self.competitive_medals_bronze: int = self.competitive_stats["awards"]["medalsBronze"]
                self.competitive_medals_silver: int = self.competitive_stats["awards"]["medalsSilver"]
                self.competitive_medals_gold: int = self.competitive_stats["awards"]["medalsGold"]
                self.competitive_games_played: int = self.competitive_stats["games"]["played"]
                self.competitive_games_won: int = self.competitive_stats["games"]["won"]

                self.competitive_tank: Union[bool, int] = False
                self.competitive_damage: Union[bool, int] = False
                self.competitive_support: Union[bool, int] = False

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


async def _get_player_internal(player: str, session: aiohttp.ClientSession) -> Player:
    """
    Uses an aiohttp session to get a player. This is a coroutine and must be awaited.
    :param player: String that is the players battletag
    :param session: An aiohttp ClientSession
    :return: A Player object
    """
    try:
        async with session.get(f"https://ow-api.com/v2/stats/pc/{player.replace('#', '-')}/profile") as resp:
            data = await resp.json()
            return Player(player, data)
    except TimeoutError:
        return Player(player, {"error": "timeout"})


async def _get_player(player: str) -> Player:
    """
    This is a coroutine and must be awaited.
    :param player: String that is the players battletag
    :return: A Player object
    """
    async with aiohttp.ClientSession() as session:
        result = await _get_player_internal(player, session)
        return result


def get_player(player: str) -> Player:
    """
    Automatically creates event loop. Does not work with programs that already have an event loop, await _get_player instead
    :param player: String that is the players battletag
    :return: A Player object
    """
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(_get_player(player))
    return result


async def _get_bulk_players(players: List[str]) -> List[Player]:
    """
    This is a coroutine and must be awaited.
    :param players: List of strings of the players battletags
    :return: A list of Player objects
    """
    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(*[_get_player_internal(player, session) for player in players])
        return result


def get_bulk_players(players: List[str]) -> List[Player]:
    """
    Automatically creates event loop. Does not work with programs that already have an event loop, await _get_bulk_players instead
    :param players: List of strings of the players battletags
    :return: A list of Player objects
    """
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(_get_bulk_players(players))
    return result
