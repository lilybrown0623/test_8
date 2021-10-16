import discord
import json
from discord.ext import commands
client = commands.Bot(command_prefix = '@', activity=discord.Game("This is from Github!"), intents = discord.Intents.all())
client.remove_command('help')

@client.command()
async def work(ctx):
    with open("data.json", "r") as f:
        users = json.load(f)
    if str(ctx.author.id) not in users:
        users[str(ctx.author.id)] = 0
        users[str(ctx.author.id)] += 1
        await ctx.send("Your got one coin!")
    else:
        users[str(ctx.author.id)] += 1
        await ctx.send("Your got one coin!")
    with open("data.json", "w") as f:
        json.dump(users, f)
        
@client.command()
async def bal(ctx):
    with open("data.json", "r") as f:
        users = json.load(f)
    if str(ctx.author.id) not in users:
        await ctx.send("You don't have any money!")
    else:
        balance = users[str(ctx.author.id)]
        await ctx.send(f"You got {balance} in your wallet")
    
        
id1 = "ODI4NTE0MDEyMDEzNzg5MjE2.YGqrzQ."
id2 = "Q2X1KVt8F1OvNrAqBsubDaQo5do"
client.run(id1 + id2) 
