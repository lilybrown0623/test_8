import discord
import random
import asyncio
import os
import datetime
import json
import math
import pymongo
from discord.ext import commands
from asyncio import sleep as s

client_user = pymongo.MongoClient("mongodb+srv://warzone0623:Jak89980123@cluster0.hmeol.mongodb.net/test1?retryWrites=true&w=majority")
db = client_user['discord']
col = db['owmbank']
collection_afk = db['afk']
collection_patreon = db['patreon']
collection_counting = db['counting']
collection_status = db['status']
  
def get_prefix(client, message):
  if message.channel == message.author.dm_channel:
    return "!"
  else:
    server = col.find_one({"guild": str(message.guild.id)})
    prefix = server["prefix"]
    return prefix, "owm"
  
client = commands.Bot(command_prefix = get_prefix, activity=discord.Game("owmhelp"), intents = discord.Intents.all())
client.remove_command('help')
#bot = commands.Bot(command_prefix="!", activity=..., status=...)
#ideas: tanint medehuin or any kind of question adend its leaderboard

"""@client.command()
async def deploy(ctx, id, prefix):
    if col.find({'name': id}).count() == 0:
        id = str(id)
        status = {"guild": str(id), "prefix": str(prefix)}
        col.insert_one(status)
        await ctx.send(f"Successfully deployed the server id and the prefix `{prefix}`")
    else:
        await ctx.send("Exists already")
        return"""
@client.command()
async def prefix(ctx, prefix = None):
  id = str(ctx.guild.id)
  server = col.find_one({"guild": id})
  pre = server["prefix"]
  if prefix == None:
    id = str(ctx.guild.id)
    await ctx.send(f"Одоогийн prefix: `{pre}`\nPrefix солих заавар:\n`{pre}prefix [new prefix]`")
  else:
    new = {"$set": {"prefix": str(prefix)}}
    col.update_one(server, new)
    await ctx.send(f"The prefix for this server was changed to `{prefix}`")

dataFilename = "data.pickle"
time_window_milliseconds = 10000
max_msg_per_window = 3
author_msg_times = {}
global ADMINS
ADMINS = [766509844425342996, 759756236996083713, 759793731644686357, 720358254991114330]
#sniker, anahita, jelly, hiruko


eagle = "<a:eagle1:835487397054906398>"
fox = "<a:fox:864980350123114507>"
snake = "🐍"
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

#TIERS
tiers = {
  "common": '<:common:852455114043555850>',
  "uncommon": '<:uncommon:852455146562912256>', 
  "rare": '<:rare:852455146033119294>', 
  "epic": '<:epic:852455114764582923>', 
  "mythical": '<:mythical:852455147069243413>',
  "legendary": '<a:legendary:852455141993873438>', 
  "fabled": '<a:fabled:852455147955290142>'
}


#SIMPLE ANNOUNCEMENT
@client.command()
async def event(ctx, *, desc = None):
  if ctx.channel == ctx.author.dm_channel:
    if desc == None:
      await ctx.send("No message was found, missing argument!")
    else:
      await ctx.send("Хүсэлтийг хүлээн авлаа!\nТаны нийтлэл 30 минутын дотор site дээр орох болно :grin:")

@client.command()
@commands.has_permissions(administrator = True)
async def announce(ctx, *, message):
  channel = client.get_channel(825112489325887558)
  await channel.send(f'**{message}**')
 
@client.command()
@commands.has_permissions(manage_messages = True)
async def post(ctx, id = None, *, message = None):
  if id == None:
    await ctx.send(message)
  else:
    channel = client.get_channel(int(id))
    await channel.send(f'{message}')
    name = channel.name
    await ctx.message.delete()
    await ctx.send(f"Made a post in the channel __{name}__!")

@client.command(aliases = ['postembedded', 'embedpost'])
@commands.has_permissions(manage_messages = True)
async def postembed(ctx, channel = None, *, desc = None):
  now = datetime.datetime.now().strftime("%x")
  if channel == None and desc == None:
    await ctx.send("**Error!**\n`!postembed {channel id} {description}`")
  else:
    channel = client.get_channel(int(channel))
    embed = discord.Embed(description=desc, color=3447003)
    embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
    embed.set_footer(text = now)
    await channel.send(embed =embed)
    name = channel.name
    await ctx.message.delete()
    await ctx.send(f"Made a post in the channel __{name}__!")


@client.command()
async def dm(ctx, id : int, *, message):
  if ctx.channel == ctx.author.dm_channel:
      user = client.get_user(id)
      await user.send(message)

@client.command()
async def poke(ctx, idr : discord.Member = None, *, msg = None):
  server = col.find_one({"guild": str(ctx.guild.id)})
  prefix = server["prefix"]
  jelly = ctx.guild.get_member(759756236996083713)

  if idr == None and msg == None:
    membe = "{member/id}"
    message = "{message}"
    await ctx.send(f"**Poke command тайлбар:**\nСерверийн хэн нэгэнд мэдэгдэлгүйгээр DM бичих\n`{prefix}poke {membe} {message}`\nЖишээ нь: `{prefix}poke 98432024823043 Hi! Stalker chin bain!`\n`{prefix}poke @OwO Hi! Stalker chin bain!`")
  else:
    await idr.send(f"**Your stalker**: {msg}")
    await jelly.send(f"{ctx.author.mention} pokes {idr.mention}\n> {msg}")
  await ctx.message.delete()


#PURGE COMMAND

@client.command(aliases=['purge'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount=100):
  amount = amount + 1
  await ctx.channel.purge(limit=amount)

@client.command()
async def clear_dm(ctx):
    messages_to_remove = 1000

    async for message in client.get_user(759756236996083713).history(limit=messages_to_remove):
        if message.author.id == client.user.id:
            await message.delete()
            await asyncio.sleep(0.5)




#CHECKING PING
@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! In {round(client.latency * 1000)}ms :ping_pong:')

@client.command()
async def servers(ctx):
    await ctx.send(f"{client.guilds}")

@client.command()
async def suggest(ctx, *, messag = None):
  if messag == None:
    await ctx.send("No suggestion found!\ne.g.: ```!suggest I need legendary spirit staff!```")
  else:
    await ctx.send("Are you sure to submit your suggestion? `yes` to confirm")

    def check(m):
      return m.content.lower() in ["yes", 'no'] and m.channel == ctx.channel
    
    embed = discord.Embed(description=f"{messag}", color=3447003)
    embed.set_author(name=f"{ctx.author.name}'s suggestion:", icon_url=f"{ctx.author.avatar_url}")
    pchannel = client.get_channel(843140086756933632)
    try:
      message = await client.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
      await ctx.send('Request timeout!')
    else:
      if message.content.lower() == 'yes':
        await ctx.send("Your suggestion has been submitted!")
        msg = await pchannel.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
      else:
        await ctx.send("Request closed!")
      

    

#-- Command for reroll
def check_tier(quality):
    if int(quality) < 20:
      tier = tiers["common"]
      return tier
    elif int(quality) >= 20 and int(quality) < 40:
      tier = tiers["uncommon"]
      return tier
    elif int(quality) <= 40 and int(quality) <= 60:
      tier = tiers["rare"]
      return tier
    elif int(quality) > 60 and int(quality) <= 80:
      tier = tiers["epic"]
      return tier
    elif int(quality) > 80 and int(quality) < 95:
      tier = tiers["mythical"]
      return tier
    elif int(quality) >= 95 and int(quality) < 100:
      tier = tiers["legendary"]
      return tier
    elif int(quality) == 100:
      tier = tiers["fabled"]
      return tier

def weapon_desc(weapon):
  if weapon == "sstaff":
    desc = "{weapon_img} **OLD WEAPON**\n**Quality:** {ql}\n**WP COST:** {cost} <:mana:835822890536402955>\n**Description:** Heal all allies for **{s1}**% of your <:magatt:835822890149740554> MAG and applies **Defense Up** for 2 turns\n\n<:defup:852539340529598494> **Defense Up** - Reduces incoming damage by **{s2}%**% Cannot stack with other Defense Up buffs\n\n{passive_message}\n‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗\n\n{weapon_img} **NEW WEAPON**\n**Quality:** {ql_new}\n**WP COST:** {cost}\n**Description:** Heal all allies for **{s1}**% of your <:magatt:835822890149740554> MAG and applies **Defense Up** for 2 turns\n\n<:defup:852539340529598494> **Defense Up** - Reduces incoming damage by **{s2}**% Cannot stack with other Defense Up buffs"
    return desc

  elif weapon == "vstaff":
    desc = "{weapon_img} **OLD WEAPON**\n**Quality:** {ql}\n**WP COST:** {cost} <:mana:835822890536402955>\n**Description:** Deal **{s1}**% of your <:magatt:835822890149740554> MAG to ALL enemies and heal ALL allies by the damage dealt\n\n{passive_message}\n‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗\n\n{weapon_img} **NEW WEAPON**\n**Quality:** {ql_new}\n**WP COST:** {cost}\n**Description:** Deal **{s1}**% of your <:magatt:835822890149740554> MAG to ALL enemies and heal ALL allies by the damage dealt"
    return desc

  elif weapon == "bow":
    desc = "{weapon_img} **OLD WEAPON**\n**Quality:** {ql}\n**WP COST:** {cost} <:mana:835822890536402955>\n**Description:** Deals **{s1}**% of your {str}STR to a random opponent\n\n{passive_message}\n‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗\n\n{weapon_img} **NEW WEAPON**\n**Quality:** {ql_new}\n**WP COST:** {cost}\n**Description:** Deals **{s1}**% of your <:att:835822889462267905> STR to a random opponent"
    return desc

  elif weapon == "dagger":
    desc = "{weapon_img} **OLD WEAPON**\n**Quality:** {ql}\n**WP COST:** {cost} <:mana:835822890536402955>\n**Description:** Deals **{s1}**% of your <:att:835822889462267905> STR to a random enemy and applies **poison** for 3 turns\n<:poison:866601422924414977> **Poison** - Deals **{s2}**% of your <:magatt:835822890149740554> MAG as true damage at the end of the turn\n\n{passive_message}\n‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗\n\n{weapon_img} **NEW WEAPON**\n**Quality:** {ql_new}\n**WP COST:** {cost}\n**Description:** Deals **{s1}**% of your <:att:835822889462267905> STR to a random enemy and applies **poison** for 3 turns\n<:poison:866601422924414977> **Poison** - Deals **{s2}**% of your <:magatt:835822890149740554> MAG as true damage at the end of the turn"
    return desc

  elif weapon == "shield":
    desc = "{weapon_img} **OLD WEAPON**\n**Quality:** {ql}\n**WP COST:** {cost} <:mana:835822890536402955>\n**Description:** Adds a **taunt** buff to your animal for 2 turns\n<:taunt:866601377119862805> **Taunt** - Taunts the enemy team and forces all opponents to attack this animal. Reduces incoming damage by **{s1}**%\n\n{passive_message}\n‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗\n\n{weapon_img} **NEW WEAPON**\n**Quality:** {ql_new}\n**WP COST:** {cost}\n**Description:** Adds a **taunt** buff to your animal for 2 turns\n<:taunt:866601377119862805> **Taunt** - Taunts the enemy team and forces all opponents to attack this animal. Reduces incoming damage by **{s1}**%"
    return desc

  elif weapon == "sword":
    desc = "{weapon_img} **OLD WEAPON**\n**Quality:** {ql}\n**WP COST:** {cost} <:mana:835822890536402955>\n**Description:** Deals **{s1}**% of your <:att:835822889462267905> STR to all opponents\n\n{passive_message}\n‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗\n\n{weapon_img} **NEW WEAPON**\n**Quality:** {ql_new}\n**WP COST:** {cost}\n**Description:** Deals **{s1}**% of your <:att:835822889462267905> STR to all opponents"
    return desc

  elif weapon == "axe":
    desc = "{weapon_img} **OLD WEAPON**\n**Quality:** {ql}\n**WP COST:** {cost}\n**Description:** Deals **{s1}**% of your <:att:835822889462267905> STR to a random opponent and apply **Freeze**\n<:freeze:866601255937376267> **Freeze** - Freeze an enemy. They can not attack next turn.\n\n{passive_message}\n‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗\n\n{weapon_img}**NEW WEAPON**\n**Quality:** {ql_new}\n**WP COST:** {cost}\n**Description:** Deals **{s1}**% of your <:att:835822889462267905> STR to a random opponent and apply **Freeze**\n<:freeze:866601255937376267> **Freeze** - Freeze an enemy. They can not attack next turn."
    return desc

  elif weapon == "banner":
    desc = "**Quality:** {ql}\n**WP COST:** {cost} <:mana:835822890536402955>\n**Description: desc orulhas zalhu hursen \n‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗\n**Quality:** {ql_new}\n**WP COST:** {cost}\n**Description: zalhu hursen"
    return desc

  elif weapon == "fstaff":
    desc = "{weapon_img} **OLD WEAPON**\n**Quality:** {ql}\n**WP COST:** {cost} <:mana:835822890536402955>\n**Description:** Deals **{s1}**% of your <:magatt:835822890149740554> MAG to a random enemy and applies **flame** for 3 turns\n**Flame** - Deals **{s2}**% of your <:magatt:835822890149740554> MAG at the end of the turn. Applying flame on a target that already has flame will explode and deal **{s3}**% damage to the target\n\n{passive_message}\n‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗\n\n{weapon_img} **NEW WEAPON**\n**Quality:** {ql_new}\n**WP COST:** {cost}\n**Description:** Deals **{s1}**% of your <:magatt:835822890149740554> MAG to a random enemy and applies **flame** for 3 turns\n**Flame** - Deals **{s2}**% of your <:magatt:835822890149740554> MAG at the end of the turn. Applying flame on a target that already has flame will explode and deal **{s3}**% damage to the target"
    return desc

  elif weapon == "hstaff":
    desc = "{weapon_img} **OLD WEAPON**\n**Quality:** {ql}\n**WP COST:** {cost} <:mana:835822890536402955>\n**Description:** Heals **{s1}**% of your <:magatt:835822890149740554> MAG to the lowest health ally\n\n{passive_message}\n‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗\n\n{weapon_img} **NEW WEAPON**\n**Quality:** {ql_new}\n**WP COST:** {cost}\n**Description:** Heals **{s1}**% of your <:magatt:835822890149740554> MAG to the lowest health ally"
    return desc

  elif weapon == "wand":
    desc = "{weapon_img} **OLD WEAPON**\n**Quality:** {ql}\n**WP COST:** {cost} <:mana:835822890536402955>\n**Description:** Deal **{s1}**% of your <:magatt:835822890149740554> MAG to a random enemy and transfer their <:mana:835822890536402955> WP to an ally equal to **{s2}**% of the damage done\n\n{passive_message}\n‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗\n\n{weapon_img} **NEW WEAPON**\n**Quality:** {ql_new}\n**WP COST:** {cost}\n**Description:** Deal **{s1}**% of your <:magatt:835822890149740554> MAG to a random enemy and transfer their <:mana:835822890536402955> WP to an ally equal to **{s2}**% of the damage done"
    return desc

  elif weapon == "estaff":
    desc = "{weapon_img} **OLD WEAPON**\n**Quality:** {ql}\n**WP COST:** {cost} <:mana:835822890536402955>\n**Description:** Sends a wave of energy and deals **{s1}**% of your <:magatt:835822890149740554> MAG to all opponents\n\n{passive_message}\n‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗\n\n{weapon_img} **NEW WEAPON**\n**Quality:** {ql_new}\n**WP COST:** {cost}\n**Description:** Sends a wave of energy and deals **{s1}**% of your <:magatt:835822890149740554> MAG to all opponents"
    return desc

  elif weapon == "scepter":
    desc = "{weapon_img} **OLD WEAPON**\n**Quality:** {ql}\n**WP COST:** {cost} <:mana:835822890536402955>\n**Description:** Replenish **{s1}**% of your <:magatt:835822890149740554> MAG as <:mana:835822890536402955> WP to an ally with the lowest <:mana:835822890536402955> WP\n\n{passive_message}\n‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗\n\n{weapon_img} **NEW WEAPON**\n**Quality:** {ql_new}\n**WP COST:** {cost}\n**Description:** Replenish **{s1}**% of your <:magatt:835822890149740554> MAG as <:mana:835822890536402955> WP to an ally with the lowest <:mana:835822890536402955> WP"
    return desc

  elif weapon == "scythe":
    desc = "{weapon_img} **OLD WEAPON**\n**Quality:** {ql}\n**WP COST:** {cost} <:mana:835822890536402955> \n**Description:** Deals **{s1}**% of your <:att:835822889462267905> STR to a random enemy and applies **Mortality** for 2 turns\n<:mortality:866601294889091103> **Mortality** - Decreases all healing for this animal by **{s2}**\n\n{passive_message}\n‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗\n\n{weapon_img} **NEW WEAPON**\n**Quality:** {ql_new}\n**WP COST:** {cost}\n**Description:** Deals **{s1}**% of your <:att:835822889462267905> STR to a random enemy and applies **Mortality** for 2 turns\n<:mortality:866601294889091103> **Mortality** - Decreases all healing for this animal by **{s2}**"
    return desc

def passive_identity(passive):
  if "hgen" in passive:
    rang = [5, 10]
    desc = "Heal **{}%** of your max HP after every turn"
    return ["Regeneration", rang, desc]
  elif "egen" in passive:
    rang = [20, 40]
    desc = "Replenish **{}** WP after every turn"
    return ["Energize", rang, desc]
  elif "mag" in passive:
    rang = [5, 20]
    desc = "Increases your MAG by **{}%**"
    return ["MAG", rang, desc]
  elif "str" in passive:
    rang = [5, 20]
    desc = "Increases your STR by **{}%**"
    return ["STR", rang, desc]
  elif "hp" in passive:
    rang = [5, 20]
    desc = "Increases your HP by **{}%**"
    return ["HP", rang, desc]
  elif "wp" in passive:
    rang = [10, 30]
    desc = "Increases your WP by **{}%**"
    return ["WP", rang, desc]
  elif "pr" in passive:
    rang = [15, 35]
    desc = "Increases your PR by **{}%**"
    return ["PR", rang, desc]
  elif "mr" in passive:
    rang = [15, 35]
    desc = "Increases your MR by **{}%**"
    return ["MR", rang, desc]
  elif "ls" in passive:
    rang = [15, 35]
    desc = "All damage you deal heals you for **{}%** of the damage dealt!"
    return ["Lifesteal", rang, desc]
  elif "thorns" in passive:
    rang = [15, 35]
    desc = "Reflect **{}%** of the damage dealt to you as true damage"
    return ["Thorns", rang, desc]
  elif "mtap" in passive:
    rang = [15, 30]
    desc = "All damage you deal replenishes your WP for **{}%** of the damage dealt!"
    return ["Mana Tap", rang, desc]
  elif "absolve" in passive:
    rang = [60, 80]
    desc = "When healed, deal **{}%** of the healed amount to a random enemy as MAG damage"
    return ["Absolve", rang, desc]
  elif "safeguard" in passive:
    rang = [20, 40]
    desc = "Negate **{}%** of the damage dealt to you with WP"
    return ["Safeguard", rang, desc]
  elif "crit" in passive:
    rang = [10, 30]
    desc = "Every attack has a **{}%** chance to deal **50%** more damage. This can apply to heals."
    return ["Critical", rang, desc]
  elif "discharge" in passive:
    rang = [100, 140]
    desc = "When WP is replenished, deal **{}%** of the replenished amount to a random enemy as MAG damage"
    return ["Discharge", rang, desc]
  elif "kami" in passive:
    rang = [50, 75]
    desc = "When the animal dies, deal **{}%** of its Max HP as MAG dmg to the attacker"
    return ["Kamikaze", rang, desc]
  elif "sprout" in passive:
    rang = [20, 40]
    desc = "Increase all incoming healing by **{}%**"
    return ["Sprout", rang, desc]
  elif "enrage" in passive:
    rang = [1, 4]
    desc = "Every 10% of missing health gives **{}%** damage"
    return ["Enrage", rang, desc]
#passive

def passive_tier(identity):
  word = []
  for letter in identity:
    word += letter
  if word[2] == "c":
    return "common"
  elif word[2] == "u":
    return "uncommon"
  elif word[2] == "r":
    return "rare"
  elif word[2] == "e":
    return "epic"
  elif word[2] == "m":
    return "mythical"
  elif word[2] == "l":
    return "legendary"
  elif word[2] == "f":
    return "fabled"
#passuve tier

def passive_quality(tier, rang):
  if tier == "common":
    crange = float(((rang[1] - rang[0]) * 0.2) + rang[0])
    amount1 = random.uniform(rang[0], crange)
    amount = round(amount1, 1)
    percent = (amount1 - rang[0])/(rang[1] - rang[0])
    return [amount, percent]
  elif tier == "uncommon":
    crange0 = float(((rang[1] - rang[0]) * 0.2) + rang[0])
    crange = float(((rang[1] - rang[0]) * 0.4) + rang[0])
    amount1 = random.uniform(crange0, crange)
    amount = round(amount1, 1)
    percent = (amount1 - rang[0])/(rang[1] - rang[0])
    return [amount, percent]
  elif tier == "rare":
    crange0 = float(((rang[1] - rang[0]) * 0.4) + rang[0])
    crange = float(((rang[1] - rang[0]) * 0.6) + rang[0])
    amount1 = random.uniform(crange0, crange)
    amount = round(amount1, 1)
    percent = (amount1 - rang[0])/(rang[1] - rang[0])
    return [amount, percent]
  elif tier == "epic":
    crange0 = float(((rang[1] - rang[0]) * 0.6) + rang[0])
    crange = float(((rang[1] - rang[0]) * 0.8) + rang[0])
    amount1 = random.uniform(crange0, crange)
    amount = round(amount1, 1)
    percent = (amount1 - rang[0])/(rang[1] - rang[0])
    return [amount, percent]
  elif tier == "mythical":
    crange0 = float(((rang[1] - rang[0]) * 0.8) + rang[0])
    crange = float(((rang[1] - rang[0]) * 0.95) + rang[0])
    amount1 = random.uniform(crange0, crange)
    amount = round(amount1, 1)
    percent = (amount1 - rang[0])/(rang[1] - rang[0])
    return [amount, percent]
  elif tier == "legendary":
    crange0 = float(((rang[1] - rang[0]) * 0.95) + rang[0])
    crange = float(((rang[1] - rang[0]) * 0.99) + rang[0])
    amount1 = random.uniform(crange0, crange)
    amount = round(amount1, 1)
    percent = (amount1 - rang[0])/(rang[1] - rang[0])
    return [amount, percent]
  elif tier == "fabled":
    amount = rang[1]
    percent = 1
    return [amount, percent]
 #passive quality

def weapon_quality(weapon, cost = None, stat1 = None, stat2 = None, stat3 = None):
  if weapon == "bow":
    stats = 100 * (((220 - int(cost)) / 100) + ((float(stat1) - 110) / 50) + 1)/3
    multi = 3
    return [stats, multi]
  elif weapon == "dagger":
    stats = 100 * (((200 - int(cost))/100) + ((float(stat1) - 70) / 30) + ((float(stat2) - 40) / 25) + 1)/4
    multi = 4
    return [stats, multi]
  elif weapon == "shield":
    stats = 100 * (((250 - int(cost)) / 100) + ((float(stat1) - 30) / 20) + 1)/3
    multi = 3
    return [stats, multi]
  elif weapon == "sword":
    stats = 100 * (((250 - int(cost)) / 100) + ((float(stat1) - 35) / 20) + 1)/3
    multi = 3
    return [stats, multi]
  elif weapon == "axe":
    stats = 100 * (((220 - int(cost)) / 100) + ((float(stat1) - 50) / 30) + 1)/3
    multi = 3
    return [stats, multi]
  elif weapon == "scythe":
    stats = 100 * (((200 - int(cost)) / 100) + ((float(stat1) - 70) / 30) + ((float(stat2) - 30)/30) + 1)/4
    multi = 4
    return [stats, multi]
  elif weapon == "fstaff":
    stats = 100 * (((200 - int(cost)) / 100) + ((float(stat1) - 60) / 20) + ((float(stat2) - 20) / 20) + ((float(stat3) - 40) / 20) + 1)/5
    multi = 5
    return [stats, multi]
  elif weapon == "hstaff":
    stats = 100 * (((200 - int(cost)) / 75) + ((float(stat2) - 100) / 50) + 1) / 3
    multi = 3
    return [stats, multi]
  elif weapon == "wand":
    stats = 100 * (((250 - int(cost)) / 100) + ((float(stat1) - 80) / 20) + ((float(stat2) - 20) / 20) + 1)/4
    multi = 4
    return [stats, multi]
  elif weapon == "estaff":
    stats = 100 * (((200 - int(cost)) / 100) + ((float(stat1) - 35) / 30) + 1) / 3
    multi = 3
    return [stats, multi]
  elif weapon == "sstaff":
    stats = 100 * (((225 - int(cost))/100) + ((float(stat1) - 30) / 20) + ((float(stat2) - 20) / 10) + 1)/4
    multi = 4
    return [stats, multi]
  elif weapon == "vstaff":
    stats = 100 * (((200 - int(cost)) / 100) + ((float(stat1) - 25) / 20) + 1) / 3
    multi = 3
    return [stats, multi]
  elif weapon == "scepter":
    stats = 100 * (((200 - int(cost))/ 75) + ((float(stat1) - 40)/ 30) + 1)/3
    multi = 3
    return [stats, multi]

def wp_id(weapon):
  if weapon == "shield":
    id = "105"
    return id
  elif weapon == "sword":
    id = "101"
    return id
  elif weapon == "hstaff":
    id = "102"
    return id
  elif weapon == "bow":
    id = "103"
    return id
  elif weapon == "vstaff":
    id = "107"
    return id
  elif weapon == "dagger":
    id = "108"
    return id
  elif weapon == "wand":
    id = "109"
    return id
  elif weapon == "fstaff":
    id = "110"
    return id
  elif weapon == "estaff":
    id = "111"
    return id
  elif weapon == "sstaff":
    id = "112"
    return id
  elif weapon == "scepter":
    id = "113"
    return id
  elif weapon == "rstaff":
    id = "114"
    return id
  elif weapon == "axe":
    id = "115"
    return id
  elif weapon == "scythe":
    id = "116"
    return id

def check_userwpn(user_id, weapon_id):
  with open("userwpn.json", "r") as f:
    users = json.load(f)
  box = str(list(users.keys()))
  crate = str(list(users.values()))
  if str(user_id) in box and str(weapon_id) in crate:
    op1 = users[str(user_id)][str(weapon_id)]["pm"]
    op2 = float(users[str(user_id)][str(weapon_id)]["pq"])
    return [op1, op2]
  else:
    op1 = " "
    op2 = float(1)
    return [op1, op2]

#-- Commands forreroll
@client.command()
async def rpassive(ctx):
  with open("passives.json", "r") as f:
    passives = json.load(f)
  r_passive = random.choice(list(passives.values()))
  r_tier = random.choice(list(r_passive.values()))
  passive = passive_identity(r_tier)
  tier = passive_tier(r_tier)
  rang = passive[1]
  amount = passive_quality(tier, rang)
  desc = passive[2]
  descr = desc.format(amount[0])
  await ctx.send(f"{r_tier} **{passive[0]}** - {descr}")

@client.command()
async def reroll(ctx, weapon_name, stat1 = None, stat2 = None, stat3 = None, stat4 = None):
  with open("passives.json", "r") as f:
    passives = json.load(f)
  with open("weapons.json", "r") as f:
    weapons = json.load(f)
  with open("userwpn.json", "r") as f:
    saved = json.load(f)
    #WEAPONS

  wping = weapons[str(weapon_name)]

  r_passive = random.choice(list(passives.values()))
  r_tier = random.choice(list(r_passive.values()))
  passive = passive_identity(r_tier)
  tier = passive_tier(r_tier)
  rang = passive[1]
  amount = passive_quality(tier, rang)
  desc = passive[2]
  descr = desc.format(amount[0])
  passive_msg = f"{r_tier} **{passive[0]}** - {descr}"

#-- First reroll appearance, appears when the command is first called
  wpid = str(wp_id(weapon_name))
  user_id = str(ctx.author.id)
  pm_main = check_userwpn(user_id, wpid)
  pm = pm_main[0]
  psql = float(pm_main[1])
  #psql 0.ab
  pre_wep_raw = weapon_quality(weapon_name, stat1, stat2, stat3, stat4)
  #Pre_wep_raw: returns [highest stats, multiplier]
  wep_raw = float(pre_wep_raw[0])
  wep_raw_upper = float(pre_wep_raw[0] / 100)
  muli = float(pre_wep_raw[1])
  wepql = float(100 * ((((wep_raw_upper * muli) - 1) + psql) / muli))
  wepql = int(wepql)
  #wep raw: weapon quality that will be shown on the top!
  weapon = weapon_desc(weapon_name)
  #weapon: "desc here" description for the weapon in str format
  tier_logo = check_tier(wepql)
  qlsct = f"{tier_logo} {wepql}%"
  #qlsct message that will be shown after the att Quality
  multiplier1 = float(pre_wep_raw[1])
  wep_ql = int(100 * (((((wep_raw / 100) * multiplier1) - 1) + amount[1]) / multiplier1))
  tier_logo_1 = check_tier(wep_ql)
  qlsct_new = f"{tier_logo_1} {wep_ql}%"
  description = weapon.format(ql = qlsct, ql_new = qlsct_new, cost = stat1, s1 = stat2, s2 = stat3, s3 = stat4, weapon_img = wping, passive_message = pm)
#--

  r_passive_1 = random.choice(list(passives.values()))
  r_tier_1 = random.choice(list(r_passive_1.values()))
  passive_1 = passive_identity(r_tier_1)
  tier_1 = passive_tier(r_tier_1)
  rang_1 = passive_1[1]
  amount_1 = passive_quality(tier_1, rang_1)
  desc_1 = passive_1[2]
  descr_1 = desc_1.format(amount_1[0])
  passive_msg_1 = f"{r_tier_1} **{passive_1[0]}** - {descr_1}"

  wep_lower1 = int(100 * (((((wep_raw / 100) * multiplier1) - 1) + amount_1[1]) / multiplier1))
  tier_logo1 = check_tier(wep_lower1)
  qlsct1 = f"{tier_logo1} {wep_lower1}%"
  description1 = weapon.format(ql = qlsct, ql_new = qlsct1, cost = stat1, s1 = stat2, s2 = stat3, s3 = stat4, weapon_img = wping, passive_message = pm)

  
  #-- Second reroll passive appearance, appears when counterclock emoji is chosen

  color = 3447003
  embed_main = discord.Embed(description=f'{description}\n\n{passive_msg}', color = discord.Colour.blue())
  embed_main.set_author(name=f"{ctx.author.name} spent 10 owo to reroll!", icon_url=ctx.author.avatar_url)
  #Main embed, and got edited in first command awaits 3 emojis
  await ctx.message.delete()

  msg1 = await ctx.send(embed = embed_main)
  await msg1.add_reaction('✅')
  await msg1.add_reaction('❎')
  await msg1.add_reaction('🔄')


  def check(reaction, user):
    return str(reaction.emoji) in ['✅', '❎', '🔄'] and user.id == ctx.author.id

  try:
    reaction, user = await client.wait_for('reaction_add', check=check, timeout=60)

  except asyncio.TimeoutError:
    embed_main = discord.Embed(title=f'{weapons[str(weapon_name)]} OLD WEAPON', description=f'{description}\n\n{passive_msg}', color = discord.Colour.grey())
    embed_main.set_author(name=f"{ctx.author.name} spent 10 owo to reroll!", icon_url=ctx.author.avatar_url)
    await msg1.edit(embed = embed_main)
    return

  else:
    if str(reaction.emoji) == '✅':
      color = discord.Colour.green()
      embed_main = discord.Embed(description=f'{description}\n\n{passive_msg}', color = discord.Colour.green())
      embed_main.set_author(name=f"{ctx.author.name} spent 10 owo to reroll!", icon_url=ctx.author.avatar_url)
      wpid = wp_id(weapon_name)
      if str(ctx.author.id) in saved:
        saved[str(ctx.author.id)][str(wpid)] = {}
        saved[str(ctx.author.id)][str(wpid)]["pm"] = passive_msg
        saved[str(ctx.author.id)][str(wpid)]["pq"] = amount[1]
      else:
        saved[str(ctx.author.id)] = {}
        saved[str(ctx.author.id)][str(wpid)] = {}
        saved[str(ctx.author.id)][str(wpid)]["pm"] = passive_msg
        saved[str(ctx.author.id)][str(wpid)]["pq"] = amount[1]
      with open("userwpn.json", "w") as f:
        json.dump(saved, f)
      await msg1.edit(embed=embed_main)
      return
    elif str(reaction.emoji) == '❎':
      color = discord.Colour.red()
      embed_main = discord.Embed(description=f'{description}\n\n{passive_msg}', color = discord.Colour.red())
      embed_main.set_author(name=f"{ctx.author.name} spent 10 owo to reroll!", icon_url=ctx.author.avatar_url)
      await msg1.edit(embed = embed_main)
      return
    elif str(reaction.emoji) == '🔄':
      new_embed = discord.Embed(description=f'{description1}\n\n{passive_msg_1}', color = discord.Colour.blue())
      new_embed.set_author(name=f"{ctx.author.name} spent 10 owo to reroll!", icon_url=ctx.author.avatar_url)
      #Among the other emojis waiting, if counter_clock is clicked it appears
      tempo = passive_msg_1
      pass_temp = description1
      ql_temp = amount_1[1]
      await msg1.edit(embed=new_embed)
      for x in range(1000):
        r_passive_2 = random.choice(list(passives.values()))
        r_tier_2 = random.choice(list(r_passive_2.values()))
        passive_2 = passive_identity(r_tier_2)
        tier_2 = passive_tier(r_tier_2)
        rang_2 = passive_2[1]
        amount_2 = passive_quality(tier_2, rang_2)
        desc_2 = passive_2[2]
        descr_2 = desc_2.format(amount_2[0])
        passive_msg_2 = f"{r_tier_2} **{passive_2[0]}** - {descr_2}"
        
        wep_lower2 = int(100 * (((((wep_raw / 100) * multiplier1) - 1) + amount_2[1]) / multiplier1))
        tier_logo2 = check_tier(wep_lower2)
        qlsct2 = f"{tier_logo2} {wep_lower2}%"
        
        description2 = weapon.format(ql = qlsct, ql_new = qlsct2, cost = stat1, s1 = stat2, s2 = stat3, s3 = stat4, weapon_img = wping, passive_message = pm)
        

        color = discord.Colour.blue()
        embed = discord.Embed(description=f'{description}\n\n{passive_msg_2}', color = color)
        embed.set_author(name=f"{ctx.author.name} spent 10 owo to reroll!", icon_url=ctx.author.avatar_url)

        try:
          reaction, user = await client.wait_for('reaction_add', check=check, timeout=60)

        except asyncio.TimeoutError:
          color = discord.Colour.grey()
          embed = discord.Embed(description=f'{description}\n\n{passive_msg_2}', color = color)
          await msg1.edit(embed = embed)
          await ctx.send("Cooldown is up!")
          return

        else:
          if str(reaction.emoji) == '✅':
            color = discord.Colour.green()
            embed = discord.Embed(description=f'{pass_temp}\n\n{tempo}', color = color)
            embed.set_author(name=f"{ctx.author.name} spent 10 owo to reroll!", icon_url=ctx.author.avatar_url)
            wpid = wp_id(weapon_name)
            if str(ctx.author.id) in saved:
              saved[str(ctx.author.id)][str(wpid)] = {}
              saved[str(ctx.author.id)][str(wpid)]["pm"] = tempo
              saved[str(ctx.author.id)][str(wpid)]["pq"] = ql_temp
            else:
              saved[str(ctx.author.id)] = {}
              saved[str(ctx.author.id)][str(wpid)] = {}
              saved[str(ctx.author.id)][str(wpid)]["pm"] = tempo
              saved[str(ctx.author.id)][str(wpid)]["pq"] = ql_temp
            with open("userwpn.json", "w") as f:
              json.dump(saved, f)
            await msg1.edit(embed = embed)
            return
          
          if str(reaction.emoji) == '❎':
            color = discord.Colour.red()
            embed = discord.Embed(description=f'{pass_temp}\n\n{tempo}', color = color)
            embed.set_author(name=f"{ctx.author.name} spent 10 owo to reroll!", icon_url=ctx.author.avatar_url)
            await msg1.edit(embed = embed)
            return 
            
          if str(reaction.emoji) == '🔄':
            color = discord.Colour.blue()
            new_embed_1 = discord.Embed(description=f'{description2}\n\n{passive_msg_2}', color = color)
            new_embed_1.set_author(name=f"{ctx.author.name} spent 10 owo to reroll!", icon_url=ctx.author.avatar_url)
            tempo = passive_msg_2
            pass_temp = description2
            ql_temp = amount_2[1]
            await msg1.edit(embed=new_embed_1)    
    

#COMMAND LIST FOR MODS
@client.command(aliases=["mod"])
@commands.has_permissions(manage_messages = True)
async def modcommands(ctx):
  embed = discord.Embed(title='Moderating commands', description='`kick`, `ban`, `purge`, `announce`, `post`', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  await ctx.send(embed=embed)

"""
@client.command(aliases=["giveaway"])
async def ga(ctx, time=None, *, prize=None):
  if time == None:
    return await ctx.send("Time not found!")
  if prize == None:
    return await ctx.send("Prize not found!")
  embed = discord.Embed(description=f"**{prize}**\n\n**React with 🎉 to enter!**\n**Time remaining**: {time}\n**Hosted by**: {ctx.author.mention}", color=3447003)
  time_convert = {"s":1, "m":60, "h":3600, "d":86400}
  gawtime = int(time[0]) * time_convert[time[-1]]
  gawmsg = await ctx.send(embed=embed)
  
  await gawmsg.add_reaction("🎉")
  await asyncio.sleep(gawtime)

  new_gawmsg = await ctx.channel.fetch_message(gawmsg.id)
  users = await gawmsg.reactions[0].users().flatten()
  users.pop(users.index(client.user))
  
  winner = random.choice(users)
  await ctx.send(f"{winner.mention} has won the **{prize}**!")
"""

@client.command()
async def avatar(ctx, *, id : int):
  if ctx.channel == ctx.author.dm_channel:
      user = client.get_user(id)
      em = discord.Embed(color=3447004)
      em.set_image(url=user.avatar_url)
      await ctx.send(embed=em)

@client.command()
async def help(ctx):
  server = col.find_one({"guild": str(ctx.guild.id)})
  p = server["prefix"]
  if ctx.guild.id == 824701307779678229:
    myEmbed = discord.Embed(
    color=3447003)
    myEmbed = discord.Embed(description=f'**СЕРВЕРИЙН PREFIX:** **{p}**\n**Prefix солих: {p}prefix**', color=3447003)
    myEmbed.add_field(name='**:crossed_swords:Weapon:**', value=f'Weapon Information\n`{p}weapons`', inline=True)
    myEmbed.add_field(name='**:robot:Huntbot:**', value=f'Huntbot Guide\n`{p}huntbot`', inline=True)
    myEmbed.add_field(name='**:snail:Team:**', value=f'Team Information\n`{p}team`\n`{p}counterinfo`', inline=True)

    myEmbed.add_field(name='**🕹️Utilities**', value=f'`{p}poke`\n`{p}8ball`\n`{p}afk`', inline=True)
    myEmbed.add_field(name=':performing_arts:**Action Commands:**', value=f'Actions and Emotes\n`{p}aclist`', inline=True)
    myEmbed.add_field(name=':game_die:**Gambling:**', value=f'Active commands:\n`{p}roll`\n`{p}coinflip`', inline=True)
    

    myEmbed.add_field(name=':tickets:**Patreon:**', value=f'Patreon худалдан авах:\n`{p}patreon`\n`{p}addpatreon`', inline=True)
    myEmbed.add_field(name='💻**Bot:**', value=f'OwO Mongolia website:\n[Link](https://bit.ly/3wdpTzp)\nBot серверт нэмэх:\n`{p}invite`', inline=True)

    myEmbed.add_field(name=':mag_right:**Help:**', value=f'Сервертэй холбоотой тусламж:\n`{p}helper`', inline=True)

    myEmbed.set_footer(text='ӨӨР АСУУХ ЗҮЙЛСИЙГ BOT-РУУ DM БИЧИЖ АСУУГААРАЙ', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')


    myEmbed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
    await ctx.send(embed=myEmbed)
  else:
    prx = server["prefix"]
    myEmbed = discord.Embed(color=3447003)
    myEmbed = discord.Embed(description=f'**СЕРВЕРИЙН PREFIX:** **{p}**\n**Prefix солих: {p}prefix**', color=3447003)
    myEmbed.add_field(name='**:crossed_swords:Weapon:**', value=f'Weapon Information\n`{prx}weapons`', inline=True)
    myEmbed.add_field(name='**:robot:Huntbot:**', value=f'Huntbot Guide\n`{prx}huntbot`', inline=True)
    myEmbed.add_field(name='**:snail:Team:**', value=f'Team Information\n`{prx}team`\n`{prx}counterinfo`', inline=True)

    myEmbed.add_field(name='**🕹️Utilities**', value=f'`{p}poke`\n`{p}8ball`\n`{p}afk`', inline=True)
    myEmbed.add_field(name=':performing_arts:**Action Commands:**', value=f'Actions and Emotes\n`{prx}aclist`', inline=True)
    myEmbed.add_field(name=':game_die:**Gambling:**', value=f'Active commands:\n`{prx}roll`\n`{prx}coinflip`', inline=True)
    
    myEmbed.add_field(name=':tickets:**Patreon:**', value=f'Patreon худалдан авах:\n`{prx}patreon`\n`{p}addpatreon`', inline=True)
    myEmbed.add_field(name=':gear:**Bot**', value=f'Bot серверт нэмэх:\n`{prx}invite`', inline=True)
    myEmbed.add_field(name='💻**Website:**', value=f'OwO Mongolia website\n[**{prx}website**](https://bit.ly/3wdpTzp)', inline=True)

    myEmbed.set_footer(text='ӨӨР АСУУХ ЗҮЙЛСИЙГ BOT-РУУ DM БИЧИЖ АСУУГААРАЙ', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')

    myEmbed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
    await ctx.send(embed=myEmbed)


  

#COMMAND HAPPY
@client.command(aliases=['smile'])
async def happy(ctx):
  links = [
'https://media.giphy.com/media/B0vFTrb0ZGDf2/giphy.gif', 
'https://media.giphy.com/media/9o59Pga7BWlDrzWhhh/giphy.gif',
'https://media.giphy.com/media/7C7pNe8NIpbFe/giphy.gif',
'https://media.giphy.com/media/LML5ldpTKLPelFtBfY/giphy.gif',
'https://media.giphy.com/media/3Cm8cxtSHqu6Q/giphy.gif',
'https://media.giphy.com/media/rFfmUWVMOyKVG/giphy.gif',
'https://media.giphy.com/media/w7dn7xRSHGZUs/giphy.gif',
'https://media.giphy.com/media/vkb4aEjq5TqqQ/giphy.gif',
'https://media.giphy.com/media/ivibkKm68n3a/giphy.gif',
'https://media.giphy.com/media/L5f4Z5JoOKARG/giphy.gif',
'https://media.giphy.com/media/JG4iKdJamPHNK/giphy.gif',
'https://media.giphy.com/media/EAOTD2L0qyvhm/giphy.gif',
'https://media.giphy.com/media/10uPYiVtMvJ5rq/giphy.gif',
'https://media.giphy.com/media/CNUb51EbTxuRG/giphy.gif',
'https://cdn.discordapp.com/attachments/713916004954275851/713941649566204006/jiKEIBTnjD8.gif']
  links2 = random.choice(links)
  myembed = discord.Embed(description= f'**| {ctx.author.name}** is happy!', color=3447003)
  myembed.set_image(url= links2)
  myembed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  await ctx.channel.send(embed=myembed)



#COMMAND SAD/CRY
@client.command(aliases=['cry'])
async def sad(ctx):
  linksforsad = ['https://media.giphy.com/media/ROF8OQvDmxytW/giphy.gif',
'https://media.giphy.com/media/shVJpcnY5MZVK/giphy.gif',
'https://media.giphy.com/media/on9LDLF5JskaQ/giphy.gif',
'https://media.giphy.com/media/1hMJTkDXPTBiU/giphy.gif',
'https://media.giphy.com/media/dT7LBdAZP1Rh6/giphy.gif',
'https://media.giphy.com/media/c1FqhfGG9YaPe/giphy.gif',
'https://media.giphy.com/media/ArLxZ4PebH2Ug/giphy.gif',
'https://media.giphy.com/media/4NW8N9mGY8sKI/giphy.gif',
'https://media.giphy.com/media/8YutMatqkTfSE/giphy.gif',
'https://media.giphy.com/media/mvRwcoCJ9kGTS/giphy.gif',
'https://media.giphy.com/media/h6C6f4phY7MU8/giphy.gif',
'https://media.giphy.com/media/4smXTnnqlS2ys/giphy.gif',
'https://media.giphy.com/media/ukfn7kMzzLqLeyi5Tt/giphy.gif']
  linkforsad2 = random.choice(linksforsad)
  temp = ['crying', 'sad']
  mood = random.choice(temp)
  myembed = discord.Embed(description= f'**|** There, there **{ctx.author.name}** is {mood}!', color=3447003)
  myembed.set_image(url = linkforsad2)
  myembed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  await ctx.channel.send(embed=myembed)



#COMMAND HUG CUDDLE
@client.command(aliases=['cuddle'])
async def hug(ctx, member : discord.Member):
  linksforhug = ['https://media.giphy.com/media/PHZ7v9tfQu0o0/giphy.gif',
'https://media.giphy.com/media/qscdhWs5o3yb6/giphy.gif',
'https://media.giphy.com/media/GMFUrC8E8aWoo/giphy.gif',
'https://media.giphy.com/media/ZQN9jsRWp1M76/giphy.gif',
'https://media.giphy.com/media/3bqtLDeiDtwhq/giphy.gif',
'https://media.giphy.com/media/gTLfgIRwAiWOc/giphy.gif,'
'https://media.giphy.com/media/lrr9rHuoJOE0w/giphy.gif',
'https://media.giphy.com/media/DjczAlIcyK1Co/giphy.gif',
'https://media.giphy.com/media/wnsgren9NtITS/giphy.gif', 
'https://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif']
  linkforhug2 = random.choice(linksforhug)
  temp = ['hugs', 'gives']
  end = [', Don\'t squeeze too hard!', ' a big hug!']
  end2 = random.choice(end)
  mood = random.choice(temp)
  if end2 ==' a big hug!':
    myembed = discord.Embed(description= f'**|** **{ctx.author.name}** gives **{member}**{end2} ', color=3447003)
    myembed.set_image(url = linkforhug2)
    myembed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
    await ctx.channel.send(embed=myembed)
  elif end2 ==', Don\'t squeeze too hard!':
    myembed = discord.Embed(description= f'**|** **{ctx.author.name}** hugs **{member}**{end2} ', color=3447003)
    myembed.set_image(url = linkforhug2)
    myembed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
    await ctx.channel.send(embed=myembed)



#COMMAND SLAP BONK PUNCH 

@client.command(aliases=['slap'])
async def punch(ctx, member : discord.Member):
  linksforslap = ['https://media.giphy.com/media/xUO4t2gkWBxDi/giphy.gif',
'https://media.giphy.com/media/m6etefcEsTANa/giphy.gif',
'https://media.giphy.com/media/Gf3AUz3eBNbTW/giphy.gif',
'https://media.giphy.com/media/xUNd9HZq1itMkiK652/giphy.gif',
'https://media.giphy.com/media/tX29X2Dx3sAXS/giphy.gif',
'https://media.giphy.com/media/xUO4t2gkWBxDi/giphy.gif',
'https://cdn.weeb.sh/images/SkSCyl5yz.gif',
'https://media.giphy.com/media/6Fad0loHc6Cbe/giphy.gif',
'https://media.giphy.com/media/u8maN0dMhVWPS/giphy.gif']
  linkforslap2 = random.choice(linksforslap)
  doing = ['slaps', 'punches',]
  action = random.choice(doing)
  myembed = discord.Embed(description= f'**|** **{ctx.author.name}** {action} **{member}** Awww It hurts!', color=3447003)
  myembed.set_image(url = linkforslap2)
  myembed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  await ctx.channel.send(embed=myembed)


#COMMAND ANGRY

@client.command(aliases=['furious'])
async def angry(ctx):
  linksforangry = ['https://media.giphy.com/media/dTWMCXuvFHJhOMS4OJ/giphy.gif',
'https://media.giphy.com/media/U77FFxuyoIPvHEIgkq/giphy.gif',
'https://media.giphy.com/media/9w9Z2ZOxcbs1a/giphy.gif',
'https://media.giphy.com/media/11WojR0GhjExlm/giphy.gif',
'https://media.giphy.com/media/X3VrxPijowGC4/giphy.gif',
'https://media.giphy.com/media/gHw3C5n5IfRWU/giphy.gif',
'https://media.giphy.com/media/RYOsjgBkb40E/giphy.gif',
'https://media.giphy.com/media/k63gNYkfIxbwY/giphy.gif',
'https://media.giphy.com/media/hCm6h7PinjD2g/giphy.gif',
'https://media.giphy.com/media/uXsPodwDXnitq/giphy.gif']
  linkforangry2 = random.choice(linksforangry)
  myembed = discord.Embed(description= f'**|** **{ctx.author.name}** is angry! You better run!', color=3447003)
  myembed.set_image(url = linkforangry2)
  myembed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  await ctx.channel.send(embed=myembed)


#COMMAND SMUG

@client.command(aliases=['scoff'])
async def smug(ctx):
  linksforsmug = ['https://media.giphy.com/media/wkW0maGDN1eSc/giphy.gif'
'https://media.giphy.com/media/bqSkJ4IwNcoZG/giphy.gif'
'https://media.giphy.com/media/Z7erjbU8fYxAQ/giphy.gif'
'https://cdn.weeb.sh/images/HkaQI1YvZ.gif'
'https://cdn.weeb.sh/images/BJJ-Lytvb.gif'
'https://cdn.weeb.sh/images/BkpeUJYw-.gif'
'https://cdn.weeb.sh/images/Hk0b8JFPZ.gif'
'https://cdn.weeb.sh/images/S1gk-U1KDW.gif'
'https://cdn.weeb.sh/images/S1slUkFvZ.gif'
'https://cdn.weeb.sh/images/H1xgWUktPW.gif']
  linkforsmug2 = random.choice(linksforsmug)
  myembed = discord.Embed(description= f'**|** **{ctx.author.name}** scoffs',color=3447003)
  myembed.set_image(url = linkforsmug2)
  myembed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  await ctx.channel.send(embed=myembed)


#COMMAND FOR KISS
@client.command(aliases=['smooch'])
async def kiss(ctx, member : discord.Member):
  linksforkiss = ['https://media.giphy.com/media/hnNyVPIXgLdle/giphy.gif',
'https://media.giphy.com/media/bGm9FuBCGg4SY/giphy.gif',
'https://media.giphy.com/media/zkppEMFvRX5FC/giphy.gif',
'https://media.giphy.com/media/bm2O3nXTcKJeU/giphy.gif',
'https://media.giphy.com/media/FqBTvSNjNzeZG/giphy.gif',
'https://media.giphy.com/media/QweWddrIQxlfi/giphy.gif',
'https://media.giphy.com/media/11k3oaUjSlFR4I/giphy.gif',
'https://media.giphy.com/media/jR22gdcPiOLaE/giphy.gif',
'https://media.giphy.com/media/QGc8RgRvMonFm/giphy.gif',
'https://media.giphy.com/media/PlybJM2j39G4qL2C1y/giphy.gif',
'https://media.giphy.com/media/US68iy39IvqWA/giphy.gif',
'https://media.giphy.com/media/xTiIzBx7xbFimGAhB6/giphy.gif',
'https://media.giphy.com/media/eHLHwWxstaDMQWQkDc/giphy.gif']
  linkforkiss2 = random.choice(linksforkiss)
  myembed = discord.Embed(description= f'**|** **{ctx.author.name}** kisses **{member}**!',color=3447003)
  myembed.set_image(url = linkforkiss2)
  myembed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  await ctx.channel.send(embed=myembed)

#COMMAND BITE

@client.command()
async def bite(ctx, member : discord.Member):
  linksforbite = ['https://cdn.weeb.sh/images/S1FOllQj-.gif',
'https://cdn.weeb.sh/images/rkNgZlXi-.gif',
'https://cdn.weeb.sh/images/rJjd1nDLz.gif',
'https://cdn.weeb.sh/images/rkakblmiZ.gif',
'https://cdn.weeb.sh/images/r1Vk-x7sZ.gif',
'https://cdn.weeb.sh/images/H1gYelQjZ.gif',
'https://cdn.weeb.sh/images/HJmbWxmiZ.gif',
'https://cdn.weeb.sh/images/BJXRmfr6-.gif']
  linkforbite2 = random.choice(linksforbite)
  myembed = discord.Embed(description= f'**|** **{ctx.author.name}** bites **{member}**!',color=3447003)
  myembed.set_image(url = linkforbite2)
  myembed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  await ctx.channel.send(embed=myembed)

@client.command()
async def pat(ctx, member: discord.Member):
  linksforpat = ["https://media.giphy.com/media/L2z7dnOduqEow/giphy.gif",
"https://media.giphy.com/media/109ltuoSQT212w/giphy.gif",
"https://media.giphy.com/media/5tmRHwTlHAA9WkVxTU/giphy.gif",
"https://media.giphy.com/media/109ltuoSQT212w/giphy.gif",
"https://media.giphy.com/media/osYdfUptPqV0s/giphy.gif",
"https://media.giphy.com/media/ye7OTQgwmVuVy/giphy.gif",
"https://media.tenor.com/images/40f454db8d7ee7ccad8998479fbabe69/tenor.gif",
"https://media.tenor.com/images/bb4471bdc56bb2cf355338059d9fe4a0/tenor.gif",
"https://media.tenor.com/images/a5bc0631e178956d3f0c5419ddd7e9c7/tenor.gi",
"https://media.tenor.com/images/1d37a873edfeb81a1f5403f4a3bfa185/tenor.gif",
"https://media.tenor.com/images/50b500c0fc0ad01a974af8b58b5e0c9b/tenor.gif",
"https://media.tenor.com/images/18d7933b549eb5a5f2bd51f53fd8697a/tenor.gif",
"https://media.tenor.com/images/472582c4625ac190447c8867fac9c4d7/tenor.gif"]
  linksforpat2 = random.choice(linksforpat)
  myembed = discord.Embed(description= f'**|** **{ctx.author.name}** pets **{member}**!',color=3447003)
  myembed.set_image(url = linksforpat2)
  myembed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  await ctx.channel.send(embed=myembed)



#CUSTOM COMMAND PIZU 
@client.command()
async def eggslap(ctx, member : discord.Member):
    linkforpizuslap = ['https://media.giphy.com/media/xUO4t2gkWBxDi/giphy.gif',
'https://media.giphy.com/media/m6etefcEsTANa/giphy.gif',
'https://media.giphy.com/media/Gf3AUz3eBNbTW/giphy.gif',
'https://media.giphy.com/media/xUNd9HZq1itMkiK652/giphy.gif',
'https://media.giphy.com/media/tX29X2Dx3sAXS/giphy.gif',
'https://media.giphy.com/media/xUO4t2gkWBxDi/giphy.gif',
'https://cdn.weeb.sh/images/SkSCyl5yz.gif',
'https://media.giphy.com/media/6Fad0loHc6Cbe/giphy.gif',
'https://media.giphy.com/media/u8maN0dMhVWPS/giphy.gif']
    pizuslap = random.choice(linkforpizuslap)
    myembed = discord.Embed(description= f'**|** **{ctx.author.name}** egged **{member}**! with the GIF!🥚',color=3447003)
    myembed.set_image(url = pizuslap)
    myembed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
    await ctx.channel.send(embed=myembed)

@client.command()
async def egghappy(ctx):
    pizuhappy = ['https://media.giphy.com/media/B0vFTrb0ZGDf2/giphy.gif', 
'https://media.giphy.com/media/9o59Pga7BWlDrzWhhh/giphy.gif',
'https://media.giphy.com/media/7C7pNe8NIpbFe/giphy.gif',
'https://media.giphy.com/media/LML5ldpTKLPelFtBfY/giphy.gif',
'https://media.giphy.com/media/3Cm8cxtSHqu6Q/giphy.gif',
'https://media.giphy.com/media/rFfmUWVMOyKVG/giphy.gif',
'https://media.giphy.com/media/w7dn7xRSHGZUs/giphy.gif',
'https://media.giphy.com/media/vkb4aEjq5TqqQ/giphy.gif',
'https://media.giphy.com/media/ivibkKm68n3a/giphy.gif',
'https://media.giphy.com/media/L5f4Z5JoOKARG/giphy.gif',
'https://media.giphy.com/media/JG4iKdJamPHNK/giphy.gif',
'https://media.giphy.com/media/EAOTD2L0qyvhm/giphy.gif',
'https://media.giphy.com/media/10uPYiVtMvJ5rq/giphy.gif',
'https://media.giphy.com/media/CNUb51EbTxuRG/giphy.gif',
'https://cdn.discordapp.com/attachments/713916004954275851/713941649566204006/jiKEIBTnjD8.gif']
    pizuhappy2 = random.choice(pizuhappy)
    myembed = discord.Embed(description= f'**|** **{ctx.author.name}** has a grin!🥚',color=3447003)
    myembed.set_image(url = pizuhappy2)
    myembed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
    await ctx.channel.send(embed=myembed)


@client.command()
async def eggbite(ctx, member : discord.Member):
    pizubite = ['https://cdn.weeb.sh/images/S1FOllQj-.gif',
'https://cdn.weeb.sh/images/rkNgZlXi-.gif',
'https://cdn.weeb.sh/images/rJjd1nDLz.gif',
'https://cdn.weeb.sh/images/rkakblmiZ.gif',
'https://cdn.weeb.sh/images/r1Vk-x7sZ.gif',
'https://cdn.weeb.sh/images/H1gYelQjZ.gif',
'https://cdn.weeb.sh/images/HJmbWxmiZ.gif',
'https://cdn.weeb.sh/images/BJXRmfr6-.gif']
    pizubite2 = random.choice(pizubite)
    myembed = discord.Embed(description= f'**|** **{ctx.author.name}** egged **{member}**! with the GIF!🥚',color=3447003)
    myembed.set_image(url = pizubite2)
    myembed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
    await ctx.channel.send(embed=myembed)


@client.command()
async def eggpat(ctx, member : discord.Member):
    pizupat = ["https://media.giphy.com/media/L2z7dnOduqEow/giphy.gif",
"https://media.giphy.com/media/109ltuoSQT212w/giphy.gif",
"https://media.giphy.com/media/5tmRHwTlHAA9WkVxTU/giphy.gif",
"https://media.giphy.com/media/109ltuoSQT212w/giphy.gif",
"https://media.giphy.com/media/osYdfUptPqV0s/giphy.gif",
"https://media.giphy.com/media/ye7OTQgwmVuVy/giphy.gif",
"https://media.tenor.com/images/40f454db8d7ee7ccad8998479fbabe69/tenor.gif",
"https://media.tenor.com/images/bb4471bdc56bb2cf355338059d9fe4a0/tenor.gif",
"https://media.tenor.com/images/a5bc0631e178956d3f0c5419ddd7e9c7/tenor.gi",
"https://media.tenor.com/images/1d37a873edfeb81a1f5403f4a3bfa185/tenor.gif",
"https://media.tenor.com/images/50b500c0fc0ad01a974af8b58b5e0c9b/tenor.gif",
"https://media.tenor.com/images/18d7933b549eb5a5f2bd51f53fd8697a/tenor.gif",
"https://media.tenor.com/images/472582c4625ac190447c8867fac9c4d7/tenor.gif"]
    pizupat2 = random.choice(pizupat)
    myembed = discord.Embed(description= f'**|** **{ctx.author.name}** egged **{member}**! with the GIF!🥚',color=3447003)
    myembed.set_image(url = pizupat2)
    myembed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
    await ctx.channel.send(embed=myembed)

@client.command()
async def egghug(ctx, member : discord.Member):
    linkforpizuhug = ['https://media.giphy.com/media/PHZ7v9tfQu0o0/giphy.gif',
'https://media.giphy.com/media/qscdhWs5o3yb6/giphy.gif',
'https://media.giphy.com/media/GMFUrC8E8aWoo/giphy.gif',
'https://media.giphy.com/media/ZQN9jsRWp1M76/giphy.gif',
'https://media.giphy.com/media/3bqtLDeiDtwhq/giphy.gif',
'https://media.giphy.com/media/gTLfgIRwAiWOc/giphy.gif,'
'https://media.giphy.com/media/lrr9rHuoJOE0w/giphy.gif',
'https://media.giphy.com/media/DjczAlIcyK1Co/giphy.gif',
'https://media.giphy.com/media/wnsgren9NtITS/giphy.gif', 
'https://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif']
    linkforpizu2 = random.choice(linkforpizuhug)
    myembed = discord.Embed(description= f'**|** **{ctx.author.name}** egged **{member}**! with the GIF!🥚',color=3447003)
    myembed.set_image(url = linkforpizu2)
    myembed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
    await ctx.channel.send(embed=myembed)

@client.command()
async def pizu(ctx):
  pizu = ctx.guild.get_member(482224954348273698)
  embed = discord.Embed(description=f"**Custom commands list for {pizu.name}**:\n`egghappy`\n`eggpat`\n`egghug`\n`eggbite`\n`eggslap`\n`egg`", color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url=pizu.avatar_url)
  await ctx.channel.send(embed=embed)

  

#ROLL
@client.command(aliases=['Roll'])
async def roll(ctx, *, number):
  cos = ctx.guild.get_member(760041402779828245)
  inumber = float(number)
  too = random.randint(1, inumber)
  inumber2 = round(inumber)
  if ctx.message.author == cos:
    if inumber >=3 and inumber <= 500:
      x = int(number)
      y = 2
      inumber3 = random.randint(y, x)
      inumber4 = round(inumber3)
      emojis = ["<:funny:851427740145156096>", "<:stock:851427775267995648>"]
      emoji = random.choice(emojis)
      words = ["Lucky", "Yes!", "Ohh", "Dang", "Bingo", "Brr"]
      word = random.choice(words)
      embed = discord.Embed(description=f':game_die:** | {ctx.author.name}** rolls a **{inumber2}** sided die\n:game_die: **|** {word}! It\'s **{int(inumber4)}** {emoji}', color=3447003)
      embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
      embed.set_thumbnail(url=f'{ctx.author.avatar_url}')
      await ctx.send(embed=embed)
    elif int(number) == 2:
      emojis = ["<:funny:851427740145156096>", "<:stock:851427775267995648>"]
      emoji = random.choice(emojis)
      words = ["Lucky", "Yes!", "Ohh", "Dang", "Bingo", "Brr"]
      word = random.choice(words)
      embed = discord.Embed(description=f':game_die:** | {ctx.author.name}** rolls a **{number}** sided die\n:game_die: **|** {word}! It\'s **{number}** {emoji}', color=3447003)
      embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
      embed.set_thumbnail(url=f'{ctx.author.avatar_url}')
      await ctx.send(embed=embed)

    else:
      words = ["Lucky", "Yes!", "Ohh", "Dang", "Bingo", "Brr..."]
      word = random.choice(words)
      embed = discord.Embed(description=f':game_die:** | {ctx.author.name}** rolls a **{inumber2}** sided die\n:game_die: **|** {word}! It\'s **{too}**!', color=3447003)
      embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
      embed.set_thumbnail(url=f'{ctx.author.avatar_url}')
      await ctx.send(embed=embed)
  else:
    if too == 1:
      emojis = ["<:sad:851427657925263360>", "<:uhnebi:851427803270086667>", "<:cry:851427718943080460>"]
      emoji = random.choice(emojis)
      words = ["Yikes!", "Geez", "Not a good day", "Aw...", "What a bad day", "Eww"]
      word = random.choice(words)
      embed = discord.Embed(description=f':game_die:** | {ctx.author.name}** rolls a **{inumber2}** sided die\n:game_die: **|** {word}! It\'s **{too}** {emoji}', color=3447003)
      embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
      embed.set_thumbnail(url=f'{ctx.author.avatar_url}')
      await ctx.send(embed=embed)
    elif too >= 2 and too <= 50:
      emojis = ["<:funny:851427740145156096>", "<:stock:851427775267995648>"]
      emoji = random.choice(emojis)
      words = ["Lucky", "Yes!", "Ohh", "Dang", "Bingo", "Brr"]
      word = random.choice(words)
      embed = discord.Embed(description=f':game_die:** | {ctx.author.name}** rolls a **{inumber2}** sided die\n:game_die: **|** {word}! It\'s **{too}** {emoji}', color=3447003)
      embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
      embed.set_thumbnail(url=f'{ctx.author.avatar_url}')
      await ctx.send(embed=embed)
    else:
      words = ["Lucky", "Yes!", "Ohh", "Dang", "Bingo", "Brr..."]
      word = random.choice(words)
      embed = discord.Embed(description=f':game_die:** | {ctx.author.name}** rolls a **{inumber2}** sided die\n:game_die: **|** {word}! It\'s **{too}**!', color=3447003)
      embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
      embed.set_thumbnail(url=f'{ctx.author.avatar_url}')
      await ctx.send(embed=embed)


#FUNGAME(8BALL)
@client.command(aliases=['8ball', '8b'])
async def eightball(ctx, *, question = None):
  server = col.find_one({"guild": str(ctx.guild.id)})
  prefix = server["prefix"]
  if question == None:
    myEmbed = discord.Embed(title='8ball ашиглах заавар:', description=f'{prefix}8ball + `question`\nЖишээ нь:\n**This is jelly**: {prefix}8ball Does Lisa have a crush on me!\n**OwO Mongolia**: Yes! ',
    color=3447003)
    myEmbed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
    myEmbed.set_thumbnail(url='https://img.favpng.com/13/8/4/8-ball-pool-magic-8-ball-eight-ball-billiards-emoji-png-favpng-vhiJ7dgTFxSwy0REFHuWAEuDK.jpg')
    await ctx.send(embed=myEmbed)
  else:
    responses = ['Тийм', 'Үгүй', 'Магадгүй тийм', 'Магадгүй үгүй', 'Бараг л тийм', ' Бараг л үгүй', 'Одоо хэлж болохгүй', 'Дараа асуу', 'Хариултыг нь хэлээд дэмий байх', 'Тхх', 'Юу гэж тийм байхав Үгүй', 'Чиний худлаа', 'Go for it!', 'Umm No!']
    emojis1 = [':face_with_raised_eyebrow:', ':thumbsup:', ':mage:', ':see_no_evil:', ':face_with_monocle:', ':disguised_face:', ':man_detective:', ':eyes:', ':thinking:', ':lying_face:', ':shushing_face:']

    await ctx.send(f':8ball: Question: {question}\n:8ball: Answer: {random.choice(responses)} {random.choice(emojis1)} {ctx.author.mention}')

@client.command(aliases=['hb'])
async def huntbot(ctx):
    myEmbed3 = discord.Embed(title= ':robot: HuntBot ашиглах заавар:',
    color=3447003)
    myEmbed3.add_field(name=':stopwatch: Efficiency:', value='Нэг цаг тутамд авах Pet-ний тоог нэмнэ', inline=True)
    myEmbed3.add_field(name=':hourglass_flowing_sand: Duration:', value='Хэр удаан хугацаанд HuntBot хийхийг тааруулна', inline=True)
    myEmbed3.add_field(name=':money_with_wings: Cost:', value='HuntBot хийхэд ашиглагдах хэмжээг багасгана', inline=True)

    myEmbed3.add_field(name=':wrench: Gain:', value='HuntBot-оос ирэх Essence-ний хэмжээг ихэсгэнэ', inline=True)
    myEmbed3.add_field(name=':crossed_swords: Experience:', value='HuntBot-оос ирэх XP-г ихэсгэнэ', inline=True)
    myEmbed3.add_field(name=':satellite: Radar:', value='Bot tieriin pet унах магадлалыг өсгөнө', inline=True)
    myEmbed3.set_thumbnail(url='https://cdn.discordapp.com/emojis/621848056714756097.gif?v=1')
    myEmbed3.add_field(name=':man_tipping_hand: TIP:', value='Шинээр ашиглаж байгаа тохиолдолд Duration, Gain-ийг хөгжүүлж, Duration 12H хүрсэн тохиолдолд Efficiency, Gain-ийг хөгжүүлснээр хурдан сайжрана. Өөрт байх Cowoncy-ний хэмжээнээс хамааран хүссэн үедээ Cowoncy-g MAX хүртэл хөгжүүлж болно. Efficiency, Gain хоёрыг хөгжүүлж дууссаны дараа XP-г тулгаж болно. Radar-ийг хамгийн сүүлд хөгжүүлэх нь ашигтай.', inline=False)
    
    await ctx.send(embed=myEmbed3)

@client.command(aliases=['weapon'])
async def weapons(ctx):
    myEmbed = discord.Embed(description='**Weapons List**: `dagger` `estaff` `vstaff` `bow` `sword` `scythe` `axe` `fstaff` `wand` `rune` `sstaff` `hstaff` `scepter` `shield` `banner` `rstaff` `orb`',
    color=3447003)
    myEmbed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')

    await ctx.send(embed=myEmbed)


#PATREON
@client.command()
async def patreon(ctx):
  cowoncy = "<:cowoncy:835154714793738281>"
  embed = discord.Embed(title=':tickets:Patreon tickets:', description=f'Patreon ticket нь 1 сарын Patreon Perks эрх өгөх юм. Хэрвээ та авахыг хүсч байвал доорх хүмүүстэй холбогдож авч болно', color=3447003)
  index = 1
  profiles = collection_patreon.find().sort('user_id')
  for item in profiles:
    price = item['price']
    user_id = int(item['user_id'])
    name = client.get_user(user_id)
    embed.add_field(name=f"{index}. {name}", value=f"Үнэ: {price} {cowoncy}", inline=False)
    index += 1

  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/483053960337293321.gif?v=1')

  await ctx.send(embed=embed)


@client.command()
async def addpatreon(ctx, *, price=None):
    user = ctx.author
    if price == None:
      await ctx.send("Command order\n`addpatreon {member} {description}`")
    else:
      status = {'user_id': user.id, 'price': str(price)}
      collection_patreon.insert_one(status)
      await ctx.send(f"{ctx.author.mention}-ыг амжилттай нэмлээ!")

@client.command()
async def removepatreon(ctx):
  user = ctx.author
  profile = collection_patreon.find_one({"user_id": user.id})
  collection_patreon.delete_one(profile)
  await ctx.send("Removed from the list")

  
#HELPERS
@client.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def helper(ctx):
  channel = client.get_channel(824707620287152129)
  if ctx.message.channel == channel:
    helper = ctx.guild.get_role(835189734006718524)
    await ctx.send(f'{helper.mention} {ctx.author.name} needs help!')
  else:
    await ctx.send(f"You can only use the command in {channel.mention}")

  
  

#AFK
@client.command()
async def afk(ctx, *, reason = None):
  server = col.find_one({"guild": str(ctx.guild.id)})
  prefix = server["prefix"]
  if reason == None:
    message = "{message}"
    await ctx.send(f"AFK command ашиглах заавар\n`{prefix}afk {message}`\nЖишээ нь: `{prefix}afk Ywj uulaa :(`")
  else:
    user = ctx.author
    then = int(datetime.datetime.now().strftime("%s"))
    status = {"user_id": user.id, "reason": str(reason), "time": then}
    collection_afk.insert_one(status)
    await ctx.send("Таны status-ийг **AFK** болголоо! :grin:")

#ACTION COMMANDS INFO
@client.command()
async def aclist(ctx):
  embed = discord.Embed(title='Action Commands', description='Emotes: `smile` `happy` `sad` `cry` `angry` `smug`\nActions: `cuddle` `slap` `punch` `kiss` `bite` `hug`', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  await ctx.send(embed=embed)




#TAGS
@client.command(aliases=['tag'])
async def tags(ctx):
  embed = discord.Embed(title='Tags:', description='whatisrune, weaponchart, wcs, wand, vstaff, votingfaq, tierlist, tierchart, tags, sword, sstaff, specialpetchart, shield, shards, serversetup, serverrules, scythe, sceptre, scepter, rules, rstaff, ratelimit, radar, quest, psupport, pgem, petchart, patreonlink, patreonfaq, orbguide, open, new, money, maxhblvl, maxhb, lvlxp, luck, linkpatreon, lbs, hstaff, howtoverify, howtorr, howtohb, howtoequip, hbrank, hbmaxlvl, hbguide, hbcost, getid, gemhelp, gemchart, fstaff, explainhb, estaff, essencecost, equip, emoji, editprofile, dt, distorted, deletedsuggestion, dagger, cprules, collectibles, cl, bow, botrules, botchart, banner, axe, agree\nUse "?tag name" to show a tag', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  await ctx.send(embed=embed)



#INVITE LINK
@client.command()
async def invite(ctx):
  embed = discord.Embed(title='Bot invitation link:', description='[Invite Bot](https://discord.com/api/oauth2/authorize?client_id=828514012013789216&permissions=3490184310&scope=bot)', color=3447003)
  embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024")

  await ctx.channel.send(embed=embed)

@client.command(aliases=['site'])
async def website(ctx):
  embed = discord.Embed(title="OwO Mongolia Website:", description=f"[(click)Link](https://bit.ly/3wdpTzp)", color=3447003)
  await ctx.send(embed=embed)
  




#TEAMS_____________________________________________________________#TEAMS
#TEAMS_______________________________________________________________#TEAMS
#TEAMS_________________________________________________________________#TEAMS




#COUNTERTEAM INFO

@client.command()
async def counterinfo(ctx):
  embed = discord.Embed(description="**Counter team, weapon informantion**\n\n**<:dagger:835822889860726795> / <:fstaff:835838720384958517>  >  <:vstaff:835822891286134814>  >  <:estaff:835822891169611776>  >  <:dagger:835822889860726795> / <:fstaff:835838720384958517>**🔁\n\n<:shield:835822891114299452>  **>**  <:dagger:835822889860726795> / <:fstaff:835838720384958517>\n\n**<:sstaff:835822892557140048>  >  <:vstaff:835822891286134814> / <:estaff:835822891169611776>**\n\n**<:shield:835822891114299452>  >   <:scythe:835822891219943434>/<:axe:835836259095281685>**\n\n**<:scythe:835822891219943434> / <:axe:835836259095281685>  +  <:dagger:835822889860726795> / <:fstaff:835838720384958517> > <:shield:835822891114299452> + <:vstaff:835822891286134814> / <:estaff:835822891169611776>**\n\n**<:dagger:835822889860726795>  +  <:shield:835822891114299452> > <:scythe:835822891219943434>  +  <:dagger:835822889860726795>**", color=3447004)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  await ctx.send(embed=embed)
#TEAMS
@client.command(aliases=['teams'])
async def team(ctx): 
  myEmbed = discord.Embed(description='**Teams List:** `mmeta`, `dbaoe`, `blitz`, `stall`', color=3447003)
  myEmbed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  msg = await ctx.send(embed=myEmbed)
  await msg.add_reaction('🐌')
  await msg.add_reaction('🐟')
  await msg.add_reaction('⛏️')
  await msg.add_reaction('🐍')



#Main meta
@client.command(aliases=['meta'])
async def mmeta(ctx):
  embed1 = discord.Embed(title='Main Meta team:', description='Main Meta баг нь Attacker, Healer, Tank-аас бүрдэх баг.\nStreak хийхэд тохиромжтой мөн ихэнх player-уудын main баг\n\n**Position 1**: `Attacker`   **|** <a:gfish:829972695583948801>  **|**  <a:lfox:829972695281172530>  **|**  <a:ldeer:829972739259105310>  **|**  <a:feagle:828506744018960394>  **|**  🦎 **+** <:dagger:835822889860726795> **|** <:vstaff:835822891286134814> **|** <:estaff:835822891169611776> **|** <:sword:835822891521409065> **|** <:bow:835822890573234247>\nХамгийн өндөр damage учруулах учих эхэнд хийх нь илүү их overall damage учруулна\n\n**Position 2**: `Healer` **|** 🦄 **|** <a:lsquid:829972695025844236>  **|** <a:ffrog:831405857622196264> **|** 🦦 **|** <:new_owo:824913223043907594> **+** <:sstaff:835822892557140048>\n**Def up**-ийг эрт идэхвжүүлнэ. Xэрвээ эсрэг багын Pos1 хэт өндөр damage-тэй бол Pos1-тэй байрыг нь сольж болно.\n\n**Position 3**: `Tank` **|** 🐌  **|** <a:fboar:828506994138284082> **|** 🦖 **|** 🦥 **+** <:shield:835822891114299452>\nХамгаалaхаас өөр ид шидгүй учир хамгийн сүүлд', color=3447003)
  embed1.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  await ctx.send(embed=embed1)

@client.command(aliases=['aoe'])
async def dbaoe(ctx):
  embed2 = discord.Embed(title='Double Aoe team:', description='Дайсний талийн бүх нэгэн зэрэг учруулж богино хугацаанд дайснаа буулган авдаг баг\n\n**Position 1**: `Attacker:` **|** <a:gfish:829972695583948801> **|** <a:ldeer:829972739259105310> **|** 🦎 **+** <:estaff:835822891169611776> \nХамгийн өндөр damage-тэй pet-ийг эхэнд хийснээр түрүүлж өндөр damage-ээр дайрна.\n\n**Position 2**: `Attacker:` **|** <a:gspider:831481110373728306> **|** <a:lfox:829972695281172530> **|** <a:feagle:828506744018960394> **|** 🐍 **+** <:sword:835822891521409065>\n2дох өндөр damage-тэй pet\n\n**Position 3**:\n`Hybrid Tank:` <a:fboar:828506994138284082> **|** <a:fgorilla:831406097133862912> **+** <:shield:835822891114299452><:thorns:835822759087046687>\n`Durable Tank:` 🦖  **|** <:lobbot:850584532419739649> **+** <:shield:835822891114299452><:reg:835822759174078474> \n`Healer:` <:new_owo:835156130022948875> **+** <:sstaff:835822892557140048>\nBattle-ийн эхний turns-д damage учруулдаггүй мөн хамгийн бага damage-тэй учир хамгийн сүүлд', color=3447003)
  embed2.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  await ctx.send(embed=embed2)

@client.command()
async def blitz(ctx):
  fstaff = "<:fstaff:835838720384958517>"
  embed3 = discord.Embed(title='Blitz team:', description=f'Blitz баг нь эсрэг багын Heal-ыг сааруулж, burst damage учруулж дайснаа ялах зорилготой баг\n\n**Position 1**: `Attacker:` **|** <a:lfox:829972695281172530> **|** <a:feagle:828506744018960394> **|** 🐍 **+** <:scythe:835822891219943434> **|** <:axe:835836259095281685>\nBattle эхлэхэд хамгийн түрүүлж эсрэг багын heal-ийг саармагжуулснаар эсрэг баг тоглолтын эхнээс бага цус нөхөлт авна\n\n**Position 2**: `Healer:` <:new_owo:824913223043907594> **+** <:sstaff:835822892557140048>\nHealer-ийг энэ байрлалд хийснээр эрт **Def Up**-ийг идэвхжүүлж ирэх damage-ийг саармагжуулж мөн цус нөхнө\n\n**Position 3**: `Attacker:` **|** <a:ldeer:829972739259105310> **|** 🦎 **+** <:dagger:835822889860726795> **|** {fstaff}   **|**{inv} {fox}  **|**  {eagle} **|** {snake} **+** <:bow:835822890573234247>\nУчруулах damage өндөр ч гэсэн **Mortality**-ийн дараа дайрах нь илүү ашигтай учир хамгийн сүүлд', color=3447003)
  embed3.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  await ctx.send(embed=embed3)

@client.command()
async def stall(ctx):
  embed4 = discord.Embed(title='Stall team', description='Stall team нь ирж буй damage-ийг саармагжуулж turn бүрт багийн pet бүрийн цусыг нөхөж өндөр level-тэй багын эсрэг амьд үлдэн Streak-ээ хамгаалхад тохиромжтой баг. 35+ дээш level дээр хийхэд тохиромжтой\n\n**Position 1**: `Attacker` **|** <a:lfox:829972695281172530> **|** <a:feagle:828506744018960394> **|** 🐍 **+** <:shield:835822891114299452>\nБагаас хамгийн өндөр учруулах учир эхэнд хийх нь ашигтай\n\n**Position 2**: `Support` **|** <a:lsquid:829972695025844236> **+** <:scepter:835822891807408169>\nPos1-ийн дараа Healer-ийн WP-г нөхөхийн тулд энэ байрлалд орно\n\n**Position 3:** `Attacker/Healer` **|** <a:ldeer:829972739259105310> **|** 🦎 **+** <:sstaff:835822892557140048>\nScepter-ээс WP авч багын амьтдын цусыг нөхөж **Def up**  идэвхжүүлнэ.', color=344703)
  embed4.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  await ctx.send(embed=embed4)

#WEAPONS #WEAPONS___________________________________________ #WEAPONS #WEAPONS
#WEAPONS #WEAPONS___________________________________________ #WEAPONS #WEAPONS

#SSTAFF
@client.command()
async def sstaff(ctx):
  embed = discord.Embed(title='Spirit Staff:', description='Spirit Staff нь тухайн Pet-ний 30-50%-тай тэнцэх хувиар багын бүх Pet-ийн цусыг нөхөж 2 turns **Def Up** buff өгнө.\n**Defense Up** нь тухын Pet-ний 20-30%-тай тэнцах хувиар ирсэн Damage-ийг багасгана.\n**WP COST**: 125-225<:mana:835822890536402955>\n\n**Passive**: <:energize:835822758176227368> <:wp:835822759661404200> <:mag:835822758851903489>\n**Useless**: <:mtap:835822759459815424> \n\n**Pet**: <a:lsquid:829972695025844236> **|** <:new_owo:824913223043907594>', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/594613521581473851.png?v=1')
  await ctx.send(embed=embed)

#ESTAFF
@client.command()
async def estaff(ctx):
  embed = discord.Embed(title='Energy Sstaff:', description='Тухайн Pet-ний нийт MAG 35-65% тай тэнцэх хувийн Damage-ийг эсрэг багын бүх Pet-d үзүүлнэ\n**WP Cost**: 100-200<:mana:835822890536402955>\n\n**Passive**: <:mtap:835822759459815424> <:mag:835822758851903489> <:energize:835822758176227368>\n\n**Pet**: <a:ldeer:829972739259105310> **|** <a:gfish:829972695583948801> **|** 🦎', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/594613521736663051.png?v=1')
  embed.set_footer(icon_url='')
  await ctx.send(embed=embed)
#VSTAFF
@client.command()
async def vstaff(ctx):
  embed = discord.Embed(title='Vampiric Staff:', description='Тухайн Pet-ний нийт MAG 25-45% тай тэнцэх хувийн Damage-ийг эсрэг багын бүх Pet-d үзүүлж багын бүх Pet-ийн цусыг нийт үзүүлсэн Damage-ийн хэмжээгээр нөхнө.\n**WP Cost**: 100-200<:mana:835822890536402955>\n\n**Passive**: <:mtap:835822759459815424> <:mag:835822758851903489> <:energize:835822758176227368>\n\n**Pet**: <a:ldeer:829972739259105310> **|** <a:gfish:829972695583948801> **|** 🦎', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/594613521371627561.png?v=1')
  embed.set_footer(icon_url='')
  await ctx.send(embed=embed)
#DAGGER
@client.command()
async def dagger(ctx):
  embed = discord.Embed(title='Poison Dagger:', description='Нийт STR-ийн 60-100%тай тэнцэх хэмжээгээр Physical Damage учруулж 3 үеийн турш Poison buff идэвхжинэ.\n**Poison Buff**<:poison:835822758318833716> нь нийт MAG-ийн 40-65%-тай тэнцэх хэмжээгээр True damage учруулна.\n**WP Cost**: 100-200<:mana:835822890536402955>\n\n**Passive**: <:mtap:835822759459815424> <:mag:835822758851903489> <:energize:835822758176227368>\n\n**Pet**: <a:ldeer:829972739259105310> **|** 🦎', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/594613521543856128.png?v=1')
  embed.set_footer(icon_url='')
  await ctx.send(embed=embed)
#SWORD
@client.command()
async def sword(ctx):
  embed = discord.Embed(title='Great Sword:', description='Sword нь тухайн Pet-ний Physical damage-ийн 35-55%тай тэнцэх хэмжээгээр AOE damage учруулна\n**WP Cost**:150-250<:mana:835822890536402955>\n\n**Passive**: <:mtap:835822759459815424> <:str:835822759396638751> <:critical:835822758251462676> <:enrage:835822757999935499>\n\n**Pet**: <a:lfox:829972695281172530> **|** <a:feagle:828506744018960394> **|** 🐍', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/538196865129250817.png?v=1')
  embed.set_footer(icon_url='')
  await ctx.send(embed=embed)
#BOW
@client.command()
async def bow(ctx):
  embed = discord.Embed(title='Bow:', description='Тухайн Pet-ний нийт Damage-ийн 110-160%тай тэнцэх хэмжээгээр дайрна.\n**WP Cost**: 120-220<:mana:835822890536402955>\n\n**Passive**: <:mtap:835822759459815424> **|** <:str:829193030786744350> <:critical:835822758251462676> <:enrage:835822757999935499>\n\n**Pet**: <a:lfox:829972695281172530> **|** <a:feagle:828506744018960394> **|** 🐍', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/594613521367695364.png?v=1')
  embed.set_footer(icon_url='')
  await ctx.send(embed=embed)
#RUNE
@client.command()
async def rune(ctx):
  embed = discord.Embed(title='Rune of the forgotten', description='2019 оны 2 сард OwO Battle System-ээ бүхэлд нь өөрчилж шинээр эхэлж rank-аар эхний 10\'000 тоглогчдод өгсөн weapon юм\nТухын Pet-ний бүх үзүүлэлтийг 5-15% хүртэлх хувиар өсгөн STR-ийн 65% болон MAG-ийн 65% хувьтай тэнцэх хэмжээг хооронд нь нэмсэнтэй тэнцүү хэмжээгээр **True Damage** учруулна\nWP Cost: 0<:mana:835822890536402955>', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/543662986753998874.png')
  embed.set_footer(icon_url='')
  await ctx.send(embed=embed)
#HSTAFF
@client.command()
async def hstaff(ctx):
  embed = discord.Embed(title='Healing staff:', description='Нийт MAG-ийн 100-150% хүртэлх хувьтай тэнцүү хэмжээгээр багын хамгийн бага HPтэй pet-ийг нөхнө.\n**WP Cost**: 125-200<:mana:835822890536402955>\n\n**Passive:** <:energize:835822758176227368> <:wp:835822759661404200>\n\n**Pet**: <a:lsquid:829972695025844236> **|** 🦓', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/594613521950441481.png?v=1')
  embed.set_footer(icon_url='')
  await ctx.send(embed=embed)
#SCEPTER
@client.command()
async def scepter(ctx):
  embed = discord.Embed(title='Arcane Scepter:', description='Нийт MAG-ийн 40-70% хүртэлх хувьтай тэнцүү хэмжээний WP-г өөрийн багын хамгийн бага WP-тэй pet-д өгнө.\n**WP Cost**: 125-200<:mana:835822890536402955>\n\n**Passive**: <:energize:835822758176227368> <:wp:835822759661404200> <:mag:835822758851903489>\n\n**Pet**:  <a:lsquid:829972695025844236>', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/622681759330598913.png?v=1')
  embed.set_footer(icon_url='')
  await ctx.send(embed=embed)
#SHIELD
@client.command()
async def shield(ctx):
  embed = discord.Embed(title='Defender’s Aegis:', description='Ирэх бүх damage-ийг өөр дээрээ 2 turn турш 30-50% хүртэлх хувиар багасгаж авна.\n**WP Cost**: 150-250<:mana:835822890536402955>\n\n**Passive**: <:energize:835822758176227368> <:reg:835822759174078474> <:sprout:835822759330185216> <:thorns:835822759087046687>\n**Totally useless**: <:mtap:835822759459815424> <:safe_guard:835822759530594324> <:mag:835822758851903489>\n\n**Pet**: 🐌 **|** <a:fboar:828506994138284082> **|** 🦖 **|** 🦥', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/594613521648713767.png?v=1')
  embed.set_footer(icon_url='')
  await ctx.send(embed=embed)
#BANNER
@client.command()
async def banner(ctx):
  embed = discord.Embed(title='Banner:', description='Багын бүх Pet-ийн учруулах damage-ийг тус тус эхний 2 turn-д 10-20% дараагийн 2 turn-д 20-30% дараагийн 2 болон түүнээс цааш turn-д 30-40% хүртэлх хувиудаар өсгөнө.\n**WP COST**: 250-350<:mana:835822890536402955>\n\n**Passive**: <:energyz:828480316241870918> <:mtap:828480246331342889>\n\n**Pet**: <a:fboar:828506994138284082>', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/622681759565479956.png?v=1')
  embed.set_footer(icon_url='')
  await ctx.send(embed=embed)
#FSTAFF
@client.command()
async def fstaff(ctx):
  embed = discord.Embed(title='Flame staff:', description='Нийт MAG-ийн 60-80% хүртэлх хувиар damage учруулж 3 turns flame buff идэвхжүүлнэ.\nFlame buff: Нийт MAG-ийн 20-50% хүртэлх хувиар damage учруулж, давхар flame buff идэвхжсэн тохиолдолд 40-60% хүртэлх хувийн damage учруулна.\n**WP Cost**: 100-200<:mana:835822890536402955>\n\n**Passive**: <:mtap:835822759459815424> <:mag:835822758851903489> <:energize:835822758176227368>\n\n**Pet**: <a:ldeer:829972739259105310> **|** 🦎', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/594613521573216266.png?v=1')
  embed.set_footer(icon_url='')
  await ctx.send(embed=embed)
#AXE
@client.command()
async def axe(ctx):
  embed = discord.Embed(title='Glacial Axe', description='Нийт STR-ийн хүртэлх хувиар damage учруулж Freeze buff идэвхжүүлнэ.\nFreeze: Тухайн нь Pet дараагийн turn алгасна\n**WP Cost**: 120-220<:mana:835822890536402955>\n\n**Passive**: <:mtap:835822759459815424> **|** <:str:829193030786744350> <:critical:835822758251462676> <:enrage:835822757999935499>\n\n**Pet**: <a:lfox:829972695281172530> **|** <a:feagle:828506744018960394> **|** 🐍', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/622681663289294850.png?v=1')
  embed.set_footer(icon_url='')
  await ctx.send(embed=embed)
#SCYTHE
@client.command()
async def scythe(ctx):
  embed = discord.Embed(title='Culling Scythe:', description='Нийт STR-ийн 70-100% хүртэлх хувиар damage учруулж 2 turns Mortality buff идэхжүүлнэ\n**Mortality**<:mortality:835822758587662396>: Ирж байгаа цус нөхөлтийг 30-60% хүртэлх хувиар бууруулна.\n**WP Cost**: 100-200<:mana:835822890536402955>\n\n**Passive**: <:mtap:835822759459815424> **|** <:str:829193030786744350> <:critical:835822758251462676> <:enrage:835822757999935499>\n\n**Pet**: <a:lfox:829972695281172530> **|** <a:feagle:828506744018960394> **|** 🐍', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/622681759401639936.png?v=1')
  embed.set_footer(icon_url='')
  await ctx.send(embed=embed)
#ORBS
@client.command(aliases=['orbs'])
async def orb(ctx):
  embed = discord.Embed(title='Orb of potency', description='Random 2 passives\n\n**Passives**:\n<:kami:835822758813237289> + <:ls:835822759107624971>\n<:str:829193030786744350> + <:ls:835822759107624971>\n<:str:829193030786744350> + <:str:829193030786744350>\n<:ls:835822759107624971> + <:ls:835822759107624971>\n**Хэрэггүй passive**: <:mag:835822758851903489> <:energize:835822758176227368> <:mtap:835822759459815424>\n\n**WP Cost**: 0<:mana:835822890536402955>', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/548783035244478474.png')
  embed.set_footer(icon_url='')
  await ctx.send(embed=embed)
#Absorbtion Wand
@client.command()
async def wand(ctx):
  embed = discord.Embed(title='Absorbtion Wand', description='Нийт MAG_ийн 80-100% хүртэлх хувиар эсрэг багт damage учруулж нийт учруулсан damage-ийн 20-40% хүртэлх хувийг тухын айлын pet-ээс авч багын pet-д өгнө.\n**WP Cost**: 150-250<:mana:835822890536402955>\n\n**Passive:** <:mtap:835822759459815424> <:mag:835822758851903489> <:energize:835822758176227368>\n\n**Pet**: <a:ldeer:829972739259105310> **|** 🦎 ', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/594613521703108631.png?v=1')
  embed.set_footer(icon_url='')
  await ctx.send(embed=embed)
#RS
@client.command()
async def rstaff(ctx):
  embed = discord.Embed(title='Resurrection Sstaff:', description='Багын үхсэн Pet-ийг дахин амилуулж, нийт MAG-ийн 50-80% хүртэлх хувиар цусыг нь нөхнө.\n**WP Cost**: 300-400<:mana:835822890536402955>\n\n**Passive**: <:energyz:828480316241870918>', color=3447003)
  embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/622681759880052757.png?v=1')
  embed.set_footer(icon_url='')
  await ctx.send(embed=embed)

#------------------------BOT ENDS HERE________BOT ENDS HERE _____________________________________________________BOT ENDS HERE_______________________________________________________BOT ENDS HERE




#ON READY CHECK
@client.event
async def on_ready():
  now_time = datetime.datetime.now().strftime("%c")
  print("Bot is online\n{}".format(now_time))

@client.event
async def on_guild_join(guild):
  status = {"guild": str(guild.id), "prefix": "owm"}
  col.insert_one(status)

#WELCOME MEMBERS
@client.event
async def on_member_join(member):
  server = col.find_one({"guild": str(member.guild.id)})
  prefix = server["prefix"]
  if member.guild.id == 824701307779678229:
    channel = client.get_channel(824701307779678232)
    guild = member.guild
    count = guild.member_count
    count2 = int(count)
    channel2 = client.get_channel(826038979022815233)
    if collection_counting.count_documents({"user_id": member.id}) == 0:
      status = {"user_id": member.id, "owo": 0, "hunt": 0, "battle": 0, "time_owo": 0, "time_hunt": 0, "time_battle": 0, "daily_owo": 0, "daily_hunt": 0, "daily_battle": 0}
      collection_counting.insert_one(status)
    else:
      pass
  
    embed = discord.Embed(description=f'**Yokoso**\nYo! {member.mention} Та манай сэрвэрийн {count2}-дэх гишүүн боллоо🎉\n\nOwO тоглодог бол хэрэгтэй гэсэн бүх мэдээллээ эндээс аваарай🤗\n\n{channel2.mention} дээр мэдээлэл тараах зориулалттай role - нууд байгаа болохоор хүссэн role дээрээ дараад аваарай', color=3447003)
    embed.set_author(name='OwO Mongolia', icon_url='https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024')
    embed.set_image(url='https://cdn.discordapp.com/attachments/826347917106479154/831928339581108264/image0.jpg')
    await channel.send(embed=embed)
    await member.send(f'Hello! Манай серверт тавтай морил {member.name}\n**{channel2.mention}** гэсэн Channel-аас өөрт хэрэгтэй Role-оо сонгон аваарай\nМөн асууж тодруулах зүйл байвал:\n**{prefix}help** гэж бичэн тусламж авч болно.')


#_____________________ON MESSAGES__________________________________________________________________________________________ON MESSAGES

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
      msg = "**It's on cooldown**, please try again in **{:.2f}s**".format(error.retry_after)
      await ctx.send(msg)

#@client.event
#async def on_command_error(ctx, error):
#  if isinstance(error, commands.CommandOnCooldown):
#    if int(error.retry_after) > 60:
 #     time_dict = {"h":3600, "s":1, "m":60, "d":86400}
  #    rem_time = int(error.retry_after[0]) * time_dict[float(error.retry_after[-1])]
   #   msg = "**It's on cooldown**, please try again in **{:.2f}**".format(rem_time)
    #  await ctx.send(msg)

    #else:
     # msg = "**It's on cooldown**, please try again in **{:.2f}s**".format(error.retry_after)
      #await ctx.send(msg)
admins = [759756236996083713]
@client.command()
async def resetdaily(ctx):
  if ctx.author.id not in admins:
    await ctx.send("Permission error")
    return
  else:
    await ctx.send("Command provoked")
    users = collection_counting.find()
    await ctx.send("Got the collection\nSetting data fot each user")
    for user in users:
      if user['daily_owo'] == 0 and user['daily_hunt'] == 0 and user['daily_battle'] == 0:
        pass
      else:
        status = {"$set": {"daily_owo": 0, "daily_hunt": 0, "daily_battle": 0}}
        collection_counting.update_one(user, status)
    await ctx.send("Successfully reset the data")
    
#LEADERBOARD
@client.command(aliases=["leaderboard"])
async def lb(ctx, x = None, y = None):
  ad = [1, 2]
  now = datetime.datetime.now().strftime("%x")
  if x == None and y == None:
    dex = 1
    full = collection_counting.find().sort("owo", -1)
    for f in full:
      if f['user_id'] == int(ctx.author.id):
        rank = dex
        my = f['owo']
        break
      else:
        dex += 1
        pass
    profiles = collection_counting.find().sort("owo", -1).limit(5)
    index = 1
    embed = discord.Embed(title=f"Top 5 grinders in OwO Mongolia", description=f"`Your rank #{rank}: {my} owo`\n{inv}", color=3447003)
    for profile in profiles:
      user = client.get_user(profile['user_id'])
      count = profile['owo']
      embed.add_field(name=f"{index}) {user.name}: __{count}__ owo", value=inv, inline=False)
      index += 1
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024")
    embed.set_footer(text=now)
    await ctx.send(embed = embed)
  elif x != None and y == None:
    if len(x) not in ad:
      dex = 1
      full = collection_counting.find().sort("daily_owo", -1)
      for f in full:
        if f['user_id'] == int(ctx.author.id):
          rank = dex
          my = f['daily_owo']
          break
        else:
          dex += 1
          pass
      profiles = collection_counting.find().sort("daily_owo", -1).limit(5)
      index = 1
      embed = discord.Embed(title=f"Top 5 daily grinders", description=f"`Your rank #{rank}: {my} owo`\n{inv}", color=3447003)
      for profile in profiles:
        user = client.get_user(profile['user_id'])
        count = profile['daily_owo']
        embed.add_field(name=f"{index}) {user.name}: __{count}__ owo", value=inv, inline=False)
        index += 1
      embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024")
      embed.set_footer(text=now)
      await ctx.send(embed = embed)
    else:
      dex = 1
      full = collection_counting.find().sort("owo", -1)
      for f in full:
        if f['user_id'] == int(ctx.author.id):
          rank = dex
          my = f['owo']
          break
        else:
          dex += 1
          pass
      profiles = collection_counting.find().sort("owo", -1).limit(int(x))
      index = 1
      embed = discord.Embed(title=f"Top {x} grinders in OwO Mongolia", description=f"`Your rank #{rank}: {my} owo`\n{inv}", color=3447003)
      for profile in profiles:
        user = client.get_user(profile['user_id'])
        count = profile['owo']
        embed.add_field(name=f"{index}) {user.name}: __{count}__ owo", value=inv, inline=False)
        index += 1
      embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024")
      embed.set_footer(text=now)
      await ctx.send(embed = embed)
  else:
    if len(x) not in ad and len(y) in ad:
      dex = 1
      full = collection_counting.find().sort("daily_owo", -1)
      for f in full:
        if f['user_id'] == int(ctx.author.id):
          rank = dex
          my = f['daily_owo']
          break
        else:
          dex += 1
          pass
      profiles = collection_counting.find().sort("daily_owo", -1).limit(int(y))
      index = 1
      embed = discord.Embed(title=f"Top {y} daily grinders", description=f"`Your rank #{rank}: {my} owo`\n{inv}", color=3447003)
      for profile in profiles:
        user = client.get_user(profile['user_id'])
        count = profile['daily_owo']
        embed.add_field(name=f"{index}) {user.name}: __{count}__ owo", value=inv, inline=False)
        index += 1
      embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024")
      embed.set_footer(text=now)
      await ctx.send(embed = embed)
    elif len(x) in ad and len(y) not in ad:
      dex = 1
      full = collection_counting.find().sort("daily_owo", -1)
      for f in full:
        if f['user_id'] == int(ctx.author.id):
          rank = dex
          my = f['daily_owo']
          break
        else:
          dex += 1
          pass
      profiles = collection_counting.find().sort("daily_owo", -1).limit(int(x))
      index = 1
      embed = discord.Embed(title=f"Top {x} daily grinders", description=f"`Your rank #{rank}: {my} owo`\n{inv}", color=3447003)
      for profile in profiles:
        user = client.get_user(profile['user_id'])
        count = profile['daily_owo']
        embed.add_field(name=f"{index}) {user.name}: __{count}__ owo", value=inv, inline=False)
        index += 1
      embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/828514012013789216/5a6aa1da2371d25b1331d50d36477eff.webp?size=1024")
      embed.set_footer(text=now)
      await ctx.send(embed = embed)


@client.command(aliases=['stat'])
async def stats(ctx, member : discord.Member = None):
  duration = datetime.datetime.now().strftime("%x")
  if member == None:
    profile = collection_counting.find_one({"user_id": ctx.author.id})
    owo = profile['owo']
    hunt = profile['hunt']
    battle = profile['battle']
    daily_owo = profile['daily_owo']
    daily_hunt = profile['daily_hunt']
    daily_battle = profile['daily_battle']
    embed = discord.Embed(title=f"{ctx.author.name}'s stats in OwO Mongolia:", description=f"**OwO Count:** `{owo}`\n**Hunt count:** `{hunt}`\n**Battle Count:** `{battle}`\n\n**DAILY STATS:**\n**OwO Count:** `{daily_owo}`\n**Hunt count:** `{daily_hunt}`\n**Battle Count:** `{daily_battle}`", color=3447003)
    embed.set_thumbnail(url = ctx.author.avatar_url)
    embed.set_footer(text=f"{duration}")
    await ctx.send(embed = embed)
  else:
    profile = collection_counting.find_one({"user_id": member.id})
    owo = profile['owo']
    hunt = profile['hunt']
    battle = profile['battle']
    daily_owo = profile['daily_owo']
    daily_hunt = profile['daily_hunt']
    daily_battle = profile['daily_battle']
    embed = discord.Embed(title=f"{member.name}'s stats in OwO Mongolia:", description=f"**OwO Count:** `{owo}`\n**Hunt count:** `{hunt}`\n**Battle Count:** `{battle}`\n\n**DAILY STATS:**\n**OwO Count:** `{daily_owo}`\n**Hunt count:** `{daily_hunt}`\n**Battle Count:** `{daily_battle}`", color=3447003)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"{duration}")
    await ctx.send(embed = embed)
  
@client.command()
async def history(ctx, id : int, limit : int = 10):
  main = client.get_channel(880109375220502560)
  channel = client.get_channel(id)
  messages = await channel.history(limit=limit).flatten()
  messages.reverse()
  for message in messages:
    await main.send(f"**{message.author.mention}**:\n{message.content}")


  

def time_converter(d):
    d = int(d)
    if d < 60:
        message = f"{d} seconds ago"
        return message
    elif d >= 60 and d <= 3600:
        d = d // 60
        if d == 1:
            return "a minute ago"
        else:
            return f"{d} minutes ago"
    elif d > 3600 and d <= 86400:
        hour = d // 3600
        if d <= 43200:
            c = d % 3600
            m = c // 60
            return f"{hour} hour {m} minutes ago"
        else:
            return f"{hour} hours ago"
    elif d > 86400:
        d = d // 86400
        return "{} days ago".format(d)

#ON MESSAGES
#ON MESSAGE STARTS HERE _________________________________________________________________________________________________________________________________________________________________________________________________________________________
  

@client.event
async def on_message(message):
  member = message.author
  if collection_counting.count_documents({"user_id": member.id}) == 0:
      status = {"user_id": member.id, "owo": 0, "hunt": 0, "battle": 0, "time_owo": 0, "time_hunt": 0, "time_battle": 0, "daily_owo": 0, "daily_hunt": 0, "daily_battle": 0}
      collection_counting.insert_one(status)
  else:
    pass
  await client.process_commands(message)

    
"""@client.listen("on_message")
async def afk_on_message(message):
  document = collection_afk.find().sort("user_id")
  now = int(datetime.datetime.now().strftime("%H"))
  for item in document:
    member_id = int(item['user_id'])
    member = client.get_user(member_id)
    if message.channel == member.dm_channel:
      pass
    elif member.mentioned_in(message):
      user = collection_afk.find_one({"user_id": member_id})
      now = int(datetime.datetime.now().strftime("%s"))
      then = int(user['time'])
      reason = user['reason']
      c = now - then
      footer = time_converter(c)   
      await message.channel.send(f"**{member.name}** is AFK\n**Хэлсэн сүүлийн үг**: {reason}\n__{footer}__")
    else:
      if message.author == member:
        user = collection_afk.find_one({"user_id": member_id})
        collection_afk.delete_one(user)
        await message.channel.send(f"AFK status-ийг чинь цуцаллаа! {message.author.mention}")
        break
      else:
        pass"""

@client.listen("on_message")
async def owo_word_counting(message):
  jelly = client.get_user(759756236996083713)
  now = int(datetime.datetime.now().strftime("%H"))
  owocount = ['owo', 'w']
  battlecount = ['wb', 'owob', 'w b', 'owo b', 'owo battle', 'owobattle', 'owofight', 'owo fight']
  huntcount = ['wh', 'owoh', 'w h', 'owo h', 'owo hunt', 'owohunt']
  if message.content.lower() in battlecount:
    if message.guild.id != 824701307779678229:
      return
    else:
      now = int(datetime.datetime.now().strftime("%s"))
      profile = collection_counting.find_one({"user_id": message.author.id})
      then = profile['time_battle']
      if (now - then) >= 15:
        old = profile['battle']
        d1 = profile['daily_battle']
        new = old + 1
        daily = d1 + 1
        status = {"$set": {"battle": new, "time_battle": now, "daily_battle": daily}}
        collection_counting.update_one(profile, status)
      else:
        return
  if message.content.lower() in huntcount:
    if message.guild.id != 824701307779678229:
      return
    else:
      now = int(datetime.datetime.now().strftime("%s"))
      profile = collection_counting.find_one({"user_id": message.author.id})
      then = profile['time_hunt']
      if (now - then) >= 15:
        old = profile['hunt']
        d1 = profile['daily_hunt']
        new = old + 1
        daily = d1 + 1
        status = {"$set": {"hunt": new, "time_hunt": now, "daily_hunt": daily}}
        collection_counting.update_one(profile, status)
      else:
        return
  if message.content.lower() in owocount:
    if message.guild.id != 824701307779678229:
      return
    else:
      now = int(datetime.datetime.now().strftime("%s"))
      profile = collection_counting.find_one({"user_id": message.author.id})
      then = profile['time_owo']
      if (now - then) >= 15:
        old = profile['owo']
        d1 = profile['daily_owo']
        new = old + 1
        daily = d1 + 1
        status = {"$set": {"owo": new, "time_owo": now, "daily_owo": daily}}
        collection_counting.update_one(profile, status)
      else:
        return
@client.listen("on_message")
async def if_said(message):
  jelly = client.get_user(759756236996083713)
  sniker = client.get_user(766509844425342996)
  channel_name = message.channel
  jelly_names = ["759756236996083713", "jelly"]
  if message.author == client.user:
        return
  elif message.channel == message.author.dm_channel:
    await jelly.send(f"{message.author.mention}: {message.content}")
    await message.author.send(f"Hi!\nЮугаар туслах вэ?\nАсуух зүйл болон санал хүсэлт байвал бичээрэй! :grin:\nМөн өөрийн гэсэн custom command хийлгэх бол тайлбарийг дэлгэрэнгүй оруулаарай!! ^^")
  elif message.content.lower() in jelly_names:
    if message.author.bot:
      return
    elif message.author.id == 885872802157170698:
      return
    elif message.channel.id == 635398315688591400:
      return
    else:
      track = client.get_channel(870147131770544228)
      await jelly.send(f'__Server__: {message.guild}\n__Channel__: {channel_name.mention}\n{message.author.mention}: {message.content}\n{message.jump_url}')
      channel = message.channel
      messages = await channel.history(limit=10).flatten()
      messages.reverse()
      for message in messages:
        await track.send(f"**{message.author.name}**:\n{message.content}")
        
id1 = "ODI4NTE0MDEyMDEzNzg5MjE2.YGqrzQ."
id2 = "Q2X1KVt8F1OvNrAqBsubDaQo5do"
client.run(id1 + id2) 
