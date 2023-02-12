# pyowapi
`pyowapi` is an asynchronous wrapper around an unofficial Overwatch api (https://ow-api.com) using aiohttp.

Things have changed considerably from v2 to v3, make sure to update your code before upgrading.

# Example usage

```python
import pyowapi

# Both of these create an event loop for you for convenience. This will not work where an event loop already exists (like discord.py)

# For a single player
player = pyowapi.get_player("Jayne#1447")
print(player.success)
print(player.private)
print(player.competitive_tank)

# For multiple players
player_list = ["Jayne#1447", "Krusher#9999"]
players = pyowapi.get_player(player_list)
for single_player in players:
    print(player.competitive_tank.group)
    print(player.competitive_tank.tier)

# For different platforms
player = pyowapi.get_player("Krusher99", platform="psn") # platform can be pc, xbox, ps4 and nintendo-switch
print(player.competitive_tank)

# If the player name is from user input sometimes it can be capitalized wrong or use the wrong discriminator
# You can pass correct_player = True and if the player name is incorrect pyowapi will attempt to find the correct one
# The player object will then have original_player_name which is the previous battletag
player = pyowapi.get_player("jayne#1447", correct_player=True)
print(player.original_player_name) # jayne#1447
print(player.player_name) # Jayne#1447
print(player.success) # True


# If an event loop already exists you need to call get_player_async instead
player = await pyowapi.get_player_async("Jayne#1447")
print(player.private)
print(player.competitive_tank)

# A player has the following properties
print(player.player_name)  # The name of the Player (battletag or other)
print(player.original_player_name) # If a player name was corrected this is the misspelled version
print(player.success)  # If the request was successful
print(player.private)  # If the player profile is private
print(player.endorsement)  # The player endorsement level
print(player.competitive_tank.tier)  # Player Tank Tier (5-1)
print(player.competitive_tank.group)  # Player Tank Group (Bronze, Silver, Gold, Platinum, Diamond, Master, Grandmaster)
print(player.competitive_damage)  # Player Damage Rating (similar to Tank)
print(player.competitive_support)  # Player Support Rating (similar to Tank)
print(player.quickplay_stats)  # Dictionary containing all quickplay stats
print(player.quickplay_games_won)
print(player.competitive_stats)  # Dictionary containing all competitive stats
print(player.competitive_games_played)
print(player.competitive_games_won)
```
