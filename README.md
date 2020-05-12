# pyowapi
`pyowapi` is an asynchronous wrapper around an official Overwatch api (https://ow-api.com) using aiohttp.

# Example usage

```
import pyowapi

# Both of these create an event loop for you for convenience. This will not work where an event loop already exists (like discord.py)

# For a single player
player = pyowapi.get_player("Jayne#1447")
print(player.success)
print(player.actual_level)
print(player.private)
print(player.competitive_tank)

# For multiple players
player_list = ["Jayne#1447", "Krusher#9999"]
players = pyowapi.get_bulk_players(player_list)
for single_player in players:
    print(player.actual_level)


# If an event loop already exists you need to await the methods with an _ at the start


player = await pyowapi._get_player("Jayne#1447")
print(player.actual_level)
print(player.private)
print(player.competitive_tank)

player_list = ["Jayne#1447", "Krusher#9999"]
players = await pyowapi._get_bulk_players(player_list)
for single_player in players:
    print(player.actual_level)

A player has the following properties
print(player.bnet)  # The battletag of the Player
print(player.success)  # If the request was successful
print(player.level)  # The number in Overwatch without stars calculated in
print(player.prestige)  # The number of stars in Overwatch
print(player.actual_level)  # The full level with stars calculated in
print(player.private)  # If the players profile is private
print(player.endorsement)  # The player endorsement level
print(player.quickplay_stats)  # Dictionary containing all quickplay stats
print(player.quickplay_cards)
print(player.quickplay_medals)
print(player.quickplay_medals_bronze)
print(player.quickplay_medals_silver)
print(player.quickplay_medals_gold)
print(player.quickplay_games_won)
print(player.competitive_stats)  # Dictionary containing all competitive stats
print(player.competitive_cards)
print(player.competitive_medals)
print(player.competitive_medals_bronze)
print(player.competitive_medals_silver)
print(player.competitive_medals_gold)
print(player.competitive_games_played)
print(player.competitive_games_won)
print(player.competitive_tank)  # Player Tank SR. False if unplaced
print(player.competitive_damage)  # Player Damage SR. False if unplaced
print(player.competitive_support)  # Player Support SR. False if unplaced
```
