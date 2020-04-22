#              Send spam DMs to people using bots (Python3) and (Discord.py)
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

class DMspam(commands.Cog, name="DMspam"):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def dmspam(self, ctx, users: Greedy[User], Time: str, *, message: str):
#		Time = 1
		for user in users:
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)
			await user.send(message)
			await asyncio.sleep(Time)

def setup(bot):
	bot.add_cog(DMspam(bot))
