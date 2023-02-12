import asyncio
import aiohttp
from typing import List, Union, Optional, Literal
from dataclasses import dataclass


@dataclass
class Rank:
    group: Literal["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster"]
    tier: Literal[1, 2, 3, 4, 5]

    _group_order = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster"]

    def __gt__(self, other):
        if isinstance(other, Rank):
            if self.group == other.group:
                return self.tier < other.tier
            else:
                return self._group_order.index(self.group) > self._group_order.index(other.group)
        else:
            raise TypeError("Cannot compare Rank to non-Rank object")

    def __lt__(self, other):
        if isinstance(other, Rank):
            if self.group == other.group:
                return self.tier > other.tier
            else:
                return self._group_order.index(self.group) < self._group_order.index(other.group)
        else:
            raise TypeError("Cannot compare Rank to non-Rank object")

    def __eq__(self, other):
        if isinstance(other, Rank):
            return self.group == other.group and self.tier == other.tier
        else:
            raise TypeError("Cannot compare Rank to non-Rank object")


class Player:
    def __init__(self, player_name: str, response: dict, original_player_name: Optional[str] = None, ):
        self.player_name: str = player_name
        self.original_player_name: Optional[str] = original_player_name
        self.success: bool = "error" not in response
        if self.success:
            self.private: Optional[bool] = response["private"]
            self.endorsement: Optional[int] = response["endorsement"]

            if not self.private:
                self.quickplay_stats: Optional[dict] = response["competitiveStats"]
                self.quickplay_games_won: Optional[int] = self.quickplay_stats["games"]["won"]

                self.competitive_stats: Optional[dict] = response["competitiveStats"]
                self.competitive_games_played: Optional[int] = self.competitive_stats["games"]["played"]
                self.competitive_games_won: Optional[int] = self.competitive_stats["games"]["won"]

            self.competitive_tank: Optional[Rank] = None
            self.competitive_damage: Optional[Rank] = None
            self.competitive_support: Optional[Rank] = None

            if response.get("ratings"):
                for rating in response["ratings"]:
                    if rating["role"] == "tank":
                        self.competitive_tank = Rank(rating["group"], rating["tier"])
                    if rating["role"] == "damage":
                        self.competitive_damage = Rank(rating["group"], rating["tier"])
                    if rating["role"] == "support":
                        self.competitive_support = Rank(rating["group"], rating["tier"])

    def __repr__(self):
        return f"<Player {self.player_name} success: {self.success}>"


async def _correct_player_internal(session: aiohttp.ClientSession, incorrect_player_name: str) -> Optional[Player]:
    """
    Attempts to find the corrected player name and returns a Player object if it does
    :param session: An aiohttp ClientSession
    :param incorrect_player_name: The incorrect player name to correct
    :return: A player object if a corrected battletag is found
    """

    # Use full name to correct wrong capitalization
    player_name_with_discriminator = incorrect_player_name.replace('#', '%23')
    # Try short version to account for a wrong discriminator
    player_name_short = incorrect_player_name.split('#')[0]

    search_terms = [player_name_with_discriminator, player_name_short]

    for search_term in search_terms:
        async with session.get(f"https://playoverwatch.com/en-us/search/account-by-name/{search_term}") as r:
            if r.status == 200:
                profiles = await r.json()
                # If we have one match that must be it
                if len(profiles) == 1:
                    new_player = await _get_player_internal(session, profiles[0]["battleTag"])
                    if new_player.success:
                        new_player.original_player_name = incorrect_player_name
                        return new_player


async def _get_player_internal(session: aiohttp.ClientSession, player_name: str,
                               correct_player: bool = False) -> Player:
    """
    Uses an aiohttp session to get a player. This is a coroutine and must be awaited.
    :param session: An aiohttp ClientSession
    :param player_name: String that is the players name (battletag or other)
    :param correct_player: If True and the lookup fails a correction will be attempted.
    :return: A Player object
    """
    try:
        async with session.get(
                f"https://ow-api.com/v2/stats/pc/{player_name.replace('#', '-')}/profile") as resp:
            data = await resp.json()
            player = Player(player_name, data)
            if not correct_player:
                return player
            elif player.success:
                return player
            else:
                new_player = await _correct_player_internal(session, player_name)
                if new_player:
                    return new_player
                else:
                    return player

    except TimeoutError:
        return Player(player_name, {"error": "timeout"})


async def get_player_async(player_names: Union[str, List[str]], correct_player: bool = False) -> Union[
    Player, List[Player]]:
    """
    This is a coroutine and must be awaited.
    :param player_names: String that is the players name (battletag or other)
    :param correct_player: If True and the lookup fails a correction will be attempted.
    :return: A Player object
    """
    async with aiohttp.ClientSession() as session:
        if isinstance(player_names, list):
            result = await asyncio.gather(*[_get_player_internal(session, player) for player in player_names])
            return result
        else:
            result = await _get_player_internal(session, player_names, correct_player)
            return result


def get_player(player_names: Union[str, List[str]], correct_player: bool = False) -> Union[Player, List[Player]]:
    """
    Automatically creates event loop. Does not work with programs that already have an event loop, await _get_player instead
    :param player_names: String that is the players name (battletag or other)
    :param correct_player: If True and the lookup fails a correction will be attempted.
    :return: A Player object
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    result = loop.run_until_complete(get_player_async(player_names, correct_player))

    # Wait 250 ms for the underlying SSL connections to close
    # See https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
    loop.run_until_complete(asyncio.sleep(0.250))
    loop.close()

    return result
