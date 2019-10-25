# pyowapi
`pyowapi` is an asynchronous wrapper around an official Overwatch api (https://ow-api.com) using aiohttp.

# Example usage

```
# Import asyncio and pyowapi
import asyncio
import pyowapi

# Get asyncio loop
loop = asyncio.get_event_loop()

# For a single player
player = loop.run_until_complete(pyowapi.get_player("Jayne#1447"))
print(player.actual_level)
print(player.private)
print(player.competitive_tank)

# For multiple players
player_list = ["Jayne#1447", "Krusher#9999"]
players = loop.run_until_complete(pyowapi.get_bulk_players(player_list))
for single_player in players:
    print(player.actual_level)

```