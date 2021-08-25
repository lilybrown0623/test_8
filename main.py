import discord
import json
from discord.ext import commands
client = commands.Bot(command_prefix = '@', activity=discord.Game("This is from Github!"), intents = discord.Intents.all())
client.remove_command('help')
id1 = "ODI4NjYzMzAyOTA5MzI5NDA5.YGs21w."
id2 = "3avVqGIv-dDXgDtG7bspk3ZvjYs"
client.run(id1 + id2) 
