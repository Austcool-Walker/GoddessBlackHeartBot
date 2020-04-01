#              Send DMs to people using bots (Python)
import discord
import ast
import io
import random
import time
import json
import sys
import inspect
import os
import asyncio
import asyncpg
import logging
import aiohttp
import traceback
import requests
import subprocess
import textwrap
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands import Bot, Greedy
from discord.ext.tasks import loop
from discord import User
from asyncio import sleep
from discord.ext import commands
from datetime import datetime
from os import listdir
from os.path import isfile, join
from contextlib import redirect_stdout

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# This is prefix of my bot
bot = Bot(command_prefix='!')

# Lets send A DM
@bot.command()
async def pm(ctx, users: Greedy[User], *, message):
    for user in users:
        await user.send(message)


# About embed
@bot.command(aliases=['info'])
async def about(ctx):
    embed = discord.Embed(title="DMbot-discord", description="A bot for sending Discord DMs to users.", color=0xff00e6)

    # give info about you here
    embed.add_field(name="Author", value="<@318528448320634881>")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # Source Code URL:
    embed.add_field(name="Source Code", value="https://github.com/Austcool-Walker/DM-discord-bot.git")

    # Your personal Discord Server that the bot was made for.
    embed.add_field(name="Discord Server", value="https://discord.gg/veVDS47")
    embed.set_image(url="https://cdn.discordapp.com/icons/692758311585579088/203473cf00ee5cde6cf7a5c52614464b.webp")

    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="[Invite link](https://discordapp.com/api/oauth2/authorize?client_id=693568262813909072&permissions=8&scope=bot)")
    await ctx.send(embed=embed)

# Bots Status
# Setting `Playing ` status
# !eval await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="The Overcomplicated Weirdness 1.12.2"))

# Setting `Streaming ` status
# !eval await bot.change_presence(status=discord.Status.online, activity=discord.Streaming(name="Approaching Nirvana", url="https://www.twitch.tv/approachingnirvana"))

# Setting `Listening ` status
# !eval await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name="Reboot by Approaching Nirvana & Big Giant Circles"))

# Setting `Watching ` status
# !eval await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="Azur Lane"))

#@bot.command()
#async def (ctx):
#    await ctx.send("")

@bot.command()
async def bowtourqueen(ctx):
    embed = discord.Embed(color=discord.Colour.red(), title="Bow To Your New Queen!")
    embed.set_image(url="https://i.imgur.com/t2LE30K.png")
    await ctx.send(embed=embed)

@bot.command()
async def degen(ctx):
    embed = discord.Embed(color=discord.Colour.red(), title="You Are All Degnerates Now!")
    embed.set_image(url="https://media1.tenor.com/images/eade076432e4650c25ed82a6368d5ba4/tenor.gif?itemid=15576648")
    await ctx.send(embed=embed)

@bot.command()
async def finished(ctx):
    embed = discord.Embed(color=discord.Colour.red(), title="YOU'RE FINISHED!")
    embed.set_image(url="https://i.fiery.me/2KnBa.gif")
    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="DMbot-discord", description="A bot for sending Discord DMs to users. List of commands are:", color=0xff00e6)
    embed.add_field(name="!about", value="Gives information about this bot.", inline=False)
    embed.add_field(name="!pm", value="Sends user a message in a DM. The bot must share a server with the user you wish to send the message to.", inline=False)
    embed.add_field(name="!bowtourqueen", value="Sends a image of Goddess Black Heart from neptunia (meme)", inline=False)
    embed.add_field(name="!degen", value="Sends a image of Degenerates", inline=False)
    embed.add_field(name="!lfinished", value="Sends a image of Black Heart Destroying you with Lace Ribbon Dance!", inline=False)
    embed.add_field(name="!help", value="Gives this help message", inline=False)
    await ctx.send(embed=embed)

# Bots Status
# Setting `Playing ` status
# await bot.change_presence(activity=discord.Game(name="The Overcomplicated Weirdness 1.12.2"))

# Setting `Streaming ` status
# await bot.change_presence(activity=discord.Streaming(name="Approaching Nirvana", url="https://www.twitch.tv/approachingnirvana"))

# Setting `Listening ` status
# await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Reboot by Approaching Nirvana & Big Giant Circles"))

# Setting `Watching ` status
# await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Azur Lane"))

# Set bot's status
async def status_task():
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game("Waiting for !help"))
        await asyncio.sleep(30)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game("Forgotten Insanity TOW [2.0.0] 1.12.2"))
        await asyncio.sleep(30)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game("Hi I'm the DM bot."))
        await asyncio.sleep(30)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game("I'm Austcool-Walker's first python3 project."))
        await asyncio.sleep(30)
        await bot.change_presence(activity=discord.Streaming(name="Approaching Nirvana", url="https://www.twitch.tv/approachingnirvana"))
        await asyncio.sleep(30)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Reboot by Approaching Nirvana & Big Giant Circles"))
        await asyncio.sleep(30)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Azur Lane"))
        await asyncio.sleep(30)

@bot.event
async def on_ready():
    ...
    bot.loop.create_task(status_task())
    #count = requests.get(file="bot.status")


# Debug code ripped from Albert Tangs Axiro

@bot.command()
async def say(ctx, *, message: str):
    await ctx.message.delete()
    await ctx.send(message)

# Moderation commands
@bot.command()
async def kick(ctx, user: discord.User, *, reason: str):
    if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).kick_members:
        await ctx.send(":x: I do not have permission to kick players.")
        return
    try:
        await ctx.message.guild.kick(user, reason=reason)
    except Exception:
        await ctx.send(":x: Player kick failed.")
        return
    await ctx.send(":white_check_mark: Player {} has been kicked from the server.".format(user.name))

@bot.command()
async def ban(ctx, user: discord.User, *, reason: str):
    if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).ban_members:
        await ctx.send(":x: I do not have permission to ban players.")
        return
    try:
        await ctx.message.guild.ban(user, reason=reason)
    except Exception:
        await ctx.send(":x: I completely failed to ban that player.")
        return
    await ctx.send(":white_check_mark: Player {} has been banned from the server.".format(user.name))

@bot.command()
async def mute(ctx, user: discord.Member):
    if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).manage_roles:
        await ctx.send(":x: I do not have permission to manage roles.")
        return
    try:
        await ctx.message.channel.category.set_permissions(user, send_messages=False, add_reactions=False)
    except Exception:
        await ctx.send("I was unable to mute that player.")
        return
    await ctx.send(":white_check_mark: Player {} has been muted.".format(user.display_name))

@bot.command()
async def unmute(ctx, user: discord.Member):
    if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).manage_roles:
        await ctx.send(":x: I do not have permission to manage roles.")
        return
    try:
        await ctx.message.channel.category.set_permissions(user, overwrite=None)
    except Exception:
        await ctx.send("I was unable to unmute that player.")
        return
    await ctx.send(":white_check_mark: Player {} has been unmuted.".format(user.display_name))

@bot.command()
async def prune(ctx, number: int):
    if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).manage_messages:
        await ctx.send("I do not have permission to delete messages.")
        return
    if number > 500:
        await ctx.send("Please specify a lower number.")
        return
    to_delete = []
    async for message in ctx.message.channel.history(limit=number+1):
        to_delete.append(message)
    while to_delete:
        if len(to_delete) > 1:
            await ctx.message.channel.delete_messages(to_delete[:100])
            to_delete = to_delete[100:]
        else:
            await to_delete.delete()
            to_delete = []
        await asyncio.sleep(1.5)

# Eval bot command

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


@bot.command(aliases=['eval'])
async def eval_fn(ctx, *, cmd):
    """Evaluates input.

    Input is interpreted as newline seperated statements.
    If the last statement is an expression, that is the return value.

    Usable globals:
      - `bot`: the bot instance
      - `discord`: the discord module
      - `commands`: the discord.ext.commands module
      - `ctx`: the invokation context
      - `__import__`: the builtin `__import__` function

    Such that `>eval 1 + 1` gives `2` as the result.

    The following invokation will cause the bot to send the text '9'
    to the channel of invokation and return '3' as the result of evaluating

    >eval ```
    a = 1 + 2
    b = a * 2
    await ctx.send(a + b)
    a
    ```
    """
    fn_name = "_eval_expr"

    cmd = cmd.strip("` ")

    # add a layer of indentation
    cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

    # wrap in async def body
    body = f"async def {fn_name}():\n{cmd}"

    parsed = ast.parse(body)
    body = parsed.body[0].body

    insert_returns(body)

    env = {
        'bot': ctx.bot,
        'discord': discord,
        'commands': commands,
        'ctx': ctx,
        '__import__': __import__
    }
    exec(compile(parsed, filename="<ast>", mode="exec"), env)

    result = (await eval(f"{fn_name}()", env))
    await ctx.message.add_reaction('👌')

# Admin bot commands

@bot.command(aliases=['quit'], hidden=True)
async def shutdown(ctx):
    '''Schaltet mich ab :( (BOT OWNER ONLY)'''
    await ctx.send('**:ok:** Bye!')
    #bot.gamesLoop.cancel()
    await bot.logout()
    sys.exit(0)

@bot.command(hidden=True)
async def restart(ctx):
    '''Startet mich neu (BOT OWNER ONLY)'''
    await ctx.send('**:ok:** Bis gleich!')
    await bot.logout()
    sys.exit(6)

@bot.command(hidden=True)
async def botavatar(ctx, url: str):
    '''Setzt einen neuen Avatar (BOT OWNER ONLY)'''
    tempAvaFile = 'tempAva.png'
    async with aiohttp.get(''.join(url)) as img:
        with open(tempAvaFile, 'wb') as f:
            f.write(await img.read())
    f = discord.File(tempAvaFile)
    await bot.edit_profile(avatar=f.read())
    os.remove(tempAvaFile)
    asyncio.sleep(2)
    await ctx.send('**:ok:** Mein neuer Avatar!\n %s' % bot.user.avatar_url)

@bot.command(hidden=True, aliases=['game'])
async def changegame(ctx, gameType: str, *, gameName: str):
    '''?ndert das derzeit spielende Spiel (BOT OWNER ONLY)'''
    gameType = gameType.lower()
    if gameType == 'playing':
        type = discord.Activity.playing
    elif gameType == 'watching':
        type = discord.Activity.watching
    elif gameType == 'listening':
        type = discord.Activity.listening
    elif gameType == 'streaming':
        type = discord.Activity.streaming
    guildsCount = len(bot.guilds)
    memberCount = len(list(bot.get_all_members()))
    gameName = gameName.format(guilds = guildsCount, members = memberCount)
    await bot.change_presence(activity=discord.Activity(type=type, name=gameName))
    await ctx.send(f'**:ok:** ?ndere das Spiel zu: {gameType} **{gameName}**')

@bot.command(hidden=True)
async def changestatus(ctx, status: str):
    '''?ndert den Online Status vom Bot (BOT OWNER ONLY)'''
    status = status.lower()
    if status == 'offline' or status == 'off' or status == 'invisible':
        discordStatus = discord.Status.invisible
    elif status == 'idle':
        discordStatus = discord.Status.idle
    elif status == 'dnd' or status == 'disturb':
        discordStatus = discord.Status.dnd
    else:
        discordStatus = discord.Status.online
    await bot.change_presence(status=discordStatus)
    await ctx.send(f'**:ok:** ?ndere Status zu: **{discordStatus}**')

@bot.command(hidden=True)
async def name(ctx, name: str):
    '''?ndert den globalen Namen vom Bot (BOT OWNER ONLY)'''
    await bot.edit_profile(username=name)
    msg = f':ok: ?ndere meinen Namen zu: **{name}**'
    await ctx.send(msg)

@bot.command(hidden=True, aliases=['guilds'])
async def servers(ctx):
    '''Listet die aktuellen verbundenen Guilds auf (BOT OWNER ONLY)'''
    msg = '```js\n'
    msg += '{!s:19s} | {!s:>5s} | {} | {}\n'.format('ID', 'Member', 'Name', 'Owner')
    for guild in bot.guilds:
        msg += '{!s:19s} | {!s:>5s}| {} | {}\n'.format(guild.id, guild.member_count, guild.name, guild.owner)
    msg += '```'
    await ctx.send(msg)

@bot.command(hidden=True)
async def leaveserver(ctx, guildid: str):
    '''Tritt aus einem Server aus (BOT OWNER ONLY)

    Beispiel:
    -----------

    :leaveserver 102817255661772800
    '''
    if guildid == 'this':
        await ctx.guild.leave()
        return
    else:
        guild = bot.get_guild(guildid)
        if guild:
            await guild.leave()
            msg = f':ok: Austritt aus {guild.name} erfolgreich!'
        else:
            msg = ':x: Konnte keine passende Guild zu dieser ID finden!'
    await ctx.send(msg)

@bot.command(hidden=True)
async def echo(ctx, channel: str, *message: str):
    '''Gibt eine Nachricht als Bot auf einem bestimmten Channel aus (BOT OWNER ONLY)'''
    ch = bot.get_channel(int(channel))
    msg = ' '.join(message)
    await ch.send(msg)
    await ctx.message.delete()

@bot.command(hidden=True)
async def discriminator(ctx, disc: str):
    '''Gibt Benutzer mit dem jeweiligen Discriminator zur?ck'''

    discriminator = disc
    memberList = ''

    for guild in bot.guilds:
        for member in guild.members:
            if member.discriminator == discriminator and member.discriminator not in memberList:
                memberList += f'{member}\n'

    if memberList:
        await ctx.send(memberList)
    else:
        await ctx.send(':x: Konnte niemanden finden')

@bot.command(hidden=True)
async def nickname(ctx, *name):
    '''?ndert den Server Nickname vom Bot (BOT OWNER ONLY)'''
    nickname = ' '.join(name)
    await ctx.me.edit(nick=nickname)
    if nickname:
        msg = f':ok: ?ndere meinen Server Nickname zu: **{nickname}**'
    else:
        msg = f':ok: Reset von meinem Server Nickname auf: **{ctx.me.name}**'
    await ctx.send(msg)

@bot.command(hidden=True)
async def setnickname(ctx, member: discord.Member=None, *name):
    '''?ndert den Nickname eines Benutzer (BOT OWNER ONLY)'''
    if member == None:
        member = ctx.author
    nickname = ' '.join(name)
    await member.edit(nick=nickname)
    if nickname:
        msg = f':ok: ?ndere Nickname von {member} zu: **{nickname}**'
    else:
        msg = f':ok: Reset von Nickname f?r {member} auf: **{member.name}**'
    await ctx.send(msg)

@bot.command(hidden=True)
async def geninvite(ctx, serverid: str):
    '''Generiert einen Invite f?r eine Guild wenn m?glich (BOT OWNER ONLY)'''
    guild = bot.get_guild(int(serverid))
    invite = await bot.create_invite(guild, max_uses=1, unique=False)
    msg = f'Invite f?r **{guild.name}** ({guild.id})\n{invite.url}'
    await ctx.author.send(msg)

@bot.command(hidden=True, aliases=['wichteln'])
async def wichtel(ctx, *participants: str):
    '''N?tzlich f?r das Community Wichtel Event 2018 (BOT OWNER ONLY)'''
    participantsList = list(participants)
    random.shuffle(participantsList)
    msg = 'Wichtelpartner stehen fest:\n```'
    for i, val in enumerate(participantsList):
        if i == len(participantsList) - 1:
            msg += f'{val.ljust(10)} ===> {participantsList[0]}\n'
        else:
            msg += f'{val.ljust(10)} ===> {participantsList[i + 1]}\n'

    msg += '```'
    await ctx.send(msg)

@bot.command(hidden=True)
async def test(ctx):
    '''Test Test Test'''
    await ctx.send('Test')
    await bot.AppInfo.owner.send('Test')
    await ctx.send(bot.cogs)

# Finally add your token number and run the client
bot.run("Discord Auth Token Here!")

