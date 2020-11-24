import asyncio
import aiohttp
from typing import List, Union, Optional


class Player:
    def __init__(self, player_name: str, response: dict, platform: str = "pc",  original_player_name: Optional[str] = None,):
        self.player_name: str = player_name
        self.original_player_name: Optional[str] = original_player_name
        self.platform: str = platform
        self.success: bool = "error" not in response
        if self.success:
            self.level: Optional[int] = response["level"]
            self.prestige: Optional[int] = response["prestige"]
            self.actual_level: Optional[int] = self.prestige * 100 + self.level
            self.private: Optional[bool] = response["private"]
            self.endorsement: Optional[int] = response["endorsement"]

            if not self.private:
                self.quickplay_stats: Optional[dict] = response["competitiveStats"]
                self.quickplay_cards: Optional[int] = self.quickplay_stats["awards"]["cards"]
                self.quickplay_medals: Optional[int] = self.quickplay_stats["awards"]["medals"]
                self.quickplay_medals_bronze: Optional[int] = self.quickplay_stats["awards"]["medalsBronze"]
                self.quickplay_medals_silver: Optional[int] = self.quickplay_stats["awards"]["medalsSilver"]
                self.quickplay_medals_gold: Optional[int] = self.quickplay_stats["awards"]["medalsGold"]
                self.quickplay_games_won: Optional[int] = self.quickplay_stats["games"]["won"]

                self.competitive_stats: Optional[dict] = response["competitiveStats"]
                self.competitive_cards: Optional[int] = self.competitive_stats["awards"]["cards"]
                self.competitive_medals: Optional[int] = self.competitive_stats["awards"]["medals"]
                self.competitive_medals_bronze: Optional[int] = self.competitive_stats["awards"]["medalsBronze"]
                self.competitive_medals_silver: Optional[int] = self.competitive_stats["awards"]["medalsSilver"]
                self.competitive_medals_gold: Optional[int] = self.competitive_stats["awards"]["medalsGold"]
                self.competitive_games_played: Optional[int] = self.competitive_stats["games"]["played"]
                self.competitive_games_won: Optional[int] = self.competitive_stats["games"]["won"]

            self.competitive_tank: Union[bool, int] = False
            self.competitive_damage: Union[bool, int] = False
            self.competitive_support: Union[bool, int] = False

            if response.get("ratings"):
                for rating in response["ratings"]:
                    if rating["role"] == "tank":
                        self.competitive_tank = rating["level"]
                    if rating["role"] == "damage":
                        self.competitive_damage = rating["level"]
                    if rating["role"] == "support":
                        self.competitive_support = rating["level"]

    def __repr__(self):
        return f"<Player {self.player_name} success: {self.success}>"


async def _correct_player_internal(session: aiohttp.ClientSession, incorrect_player_name: str, platform: str = "pc") -> Optional[Player]:
    """
    Attempts to find the corrected player name and returns a Player object if it does
    :param session: An aiohttp ClientSession
    :param incorrect_player_name: The incorrect player name to correct
    :param platform: Platform, can be pc, xbox, ps4 and nintendo-switch
    :return: A player object if a corrected battletag is found
    """
    search_terms = []
    if platform == "pc":
        # Use full name to correct wrong capitalization
        player_name_with_discriminator = incorrect_player_name.replace('#', '%23')
        # Try short version to account for a wrong discriminator
        player_name_short = incorrect_player_name.split('#')[0]
        search_terms.append(player_name_with_discriminator)
        search_terms.append(player_name_short)
    else:
        # Use full player name to correct wrong capitalization, there are no discriminators on console
        search_terms.append(incorrect_player_name)

    for search_term in search_terms:
        async with session.get(f"https://playoverwatch.com/en-us/search/account-by-name/{search_term}") as r:
            if r.status == 200:
                profiles = await r.json()
                # Filter the data to only include names from the platform
                profiles = [profile for profile in profiles if profile["platform"] == platform]
                # If we have one match that must be it
                if len(profiles) == 1:
                    new_player = await _get_player_internal(session, profiles[0]["name"], platform)
                    if new_player.success:
                        new_player.original_player_name = incorrect_player_name
                        return new_player


async def _get_player_internal(session: aiohttp.ClientSession, player_name: str, platform: str = "pc", correct_player: bool = False) -> Player:
    """
    Uses an aiohttp session to get a player. This is a coroutine and must be awaited.
    :param session: An aiohttp ClientSession
    :param player_name: String that is the players name (battletag or other)
    :param platform: Platform, can be pc, xbox, ps4 and nintendo-switch
    :param correct_player: If True and the lookup fails a correction will be attempted.
    :return: A Player object
    """
    try:
        async with session.get(
                f"https://ow-api.com/v2/stats/{platform}/{player_name.replace('#', '-')}/profile") as resp:
            data = await resp.json()
            player = Player(player_name, data)
            if not correct_player:
                return player
            elif player.success:
                return player
            else:
                new_player = await _correct_player_internal(session, player_name, platform)
                if new_player:
                    return new_player
                else:
                    return player

    except TimeoutError:
        return Player(player_name, {"error": "timeout"})


async def get_player_async(player_names: Union[str, List[str]], platform: str = "pc", correct_player: bool = False) -> Union[Player, List[Player]]:
    """
    This is a coroutine and must be awaited.
    :param player_names: String that is the players name (battletag or other)
    :param platform: Platform, can be pc, xbox, ps4 and nintendo-switch
    :param correct_player: If True and the lookup fails a correction will be attempted.
    :return: A Player object
    """
    async with aiohttp.ClientSession() as session:
        if isinstance(player_names, list):
            result = await asyncio.gather(*[_get_player_internal(session, player, platform) for player in player_names])
            return result
        else:
            result = await _get_player_internal(session, player_names, platform, correct_player)
            return result


def get_player(player_names: Union[str, List[str]], platform: str = "pc", correct_player: bool = False) -> Union[Player, List[Player]]:
    """
    Automatically creates event loop. Does not work with programs that already have an event loop, await _get_player instead
    :param player_names: String that is the players name (battletag or other)
    :param platform: Platform, can be pc, xbox, ps4 and nintendo-switch
    :param correct_player: If True and the lookup fails a correction will be attempted.
    :return: A Player object
    """
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_player_async(player_names, platform, correct_player))
    return result
