# pyowapi
`pyowapi` is an asynchronous wrapper around an official Overwatch api (https://ow-api.com) using aiohttp.

# Example usage

```
# Import asyncio and pyowapi
import pyowapi


# For a single player
player = pyowapi.get_player("Jayne#1447")
print(player.actual_level)
print(player.private)
print(player.competitive_tank)

# For multiple players
player_list = ["Jayne#1447", "Krusher#9999"]
players = pyowapi.get_bulk_players(player_list)
for single_player in players:
    print(player.actual_level)

```