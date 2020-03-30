#              Send DMs to people using bots (Python)
import discord
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands import Bot, Greedy
from discord.ext.tasks import loop
from discord import User
from asyncio import sleep
import discord
from discord.ext import commands
import random
import time
import random
import json
import sys
import asyncio
import inspect
import json
import os
import asyncio
import asyncpg
from datetime import datetime
import random
import logging
import aiohttp
import traceback

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
    embed.set_image(name="Source Code", url="https://github.com/Austcool-Walker/DM-discord-bot.git")

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
    embed = discord.Embed(color=discord.Colour.red(), title="YOUR FINISHED!")
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

client = discord.Client()
async def my_background_task():
    await client.wait_until_ready()
    counter = 0
    channel = discord.Object(id='channel_id_here')
    while not client.is_closed:
        counter += 1
        await client.send_message(channel, counter)
        await asyncio.sleep(60) # task runs every 60 seconds
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
client.loop.create_task(my_background_task())

# Bots Status
# Setting `Playing ` status
# await bot.change_presence(activity=discord.Game(name="The Overcomplicated Weirdness 1.12.2"))

# Setting `Streaming ` status
# await bot.change_presence(activity=discord.Streaming(name="Approaching Nirvana", url="https://www.twitch.tv/approachingnirvana"))

# Setting `Listening ` status
# await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Reboot by Approaching Nirvana & Big Giant Circles"))

# Setting `Watching ` status
# await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Azur Lane"))

# Eval command
@bot.command(name='eval', pass_context=True)
async def eval_(ctx, *, command):
    res = eval(command)
    if inspect.isawaitable(res):
        await bot.say(await res)
    else:
        await bot.say(res)

# Finally add your token number and run the client
bot.run("Discord Auth Token Here!")

