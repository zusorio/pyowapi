# pyowapi
`pyowapi` is an asynchronous wrapper around an unofficial Overwatch api (https://ow-api.com) using aiohttp.

Things have changed considerably from v1 to v2, make sure to update your code before upgrading.

# Example usage

```python
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
players = pyowapi.get_player(player_list)
for single_player in players:
    print(player.actual_level)

# For different platforms
player = pyowapi.get_player("Krusher99", platform="psn") # platform can be pc, xbox, ps4 and nintendo-switch
print(player.actual_level)

# If the player name is from user input sometimes it can be capitalized wrong or use the wrong discriminator
# You can pass correct_player = True and if the player name is incorrect pyowapi will attempt to find the correct one
# The player object will then have original_player_name which is the previous battletag
player = pyowapi.get_player("jayne#1447", correct_player=True)
print(player.original_player_name) # jayne#1447
print(player.player_name) # Jayne#1447
print(player.success) # True


# If an event loop already exists you need to call get_player_async instead
player = await pyowapi.get_player_async("Jayne#1447")
print(player.actual_level)
print(player.private)
print(player.competitive_tank)

# A player has the following properties
print(player.player_name)  # The name of the Player (battletag or other)
print(player.original_player_name) # If a player name was corrected this is the misspelled version
print(player.success)  # If the request was successful
print(player.level)  # The number in Overwatch without stars calculated in
print(player.prestige)  # The number of stars in Overwatch
print(player.actual_level)  # The full level with stars calculated in
print(player.private)  # If the player profile is private
print(player.endorsement)  # The player endorsement level
print(player.competitive_tank)  # Player Tank SR. False if unplaced
print(player.competitive_damage)  # Player Damage SR. False if unplaced
print(player.competitive_support)  # Player Support SR. False if unplaced
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
```
