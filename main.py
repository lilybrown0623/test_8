import discord
import json
from discord.ext import commands
client = commands.Bot(command_prefix = '@', activity=discord.Game("This is from Github!"), intents = discord.Intents.all())
client.remove_command('help')
client.run('ODI4NjYzMzAyOTA5MzI5NDA5.YGs21w.JKpIXFBQBlaDBOeDbrLf5Rq3WKA') 
