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
@bot.command()
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

    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="[Invite link](https://discordapp.com/api/oauth2/authorize?client_id=693568262813909072&permissions=8&scope=bot)")
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


@bot.command()
async def eval(ctx, *, cmd):
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
    await ctx.send(result)

# Finally add your token number and run the client
bot.run("Discord Auth Token Here!")

