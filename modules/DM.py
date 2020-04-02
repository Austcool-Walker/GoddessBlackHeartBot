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

class DM(commands.Cog, name="DM"):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def pm(self, ctx, users: Greedy[User], *, message: str):
		for user in users:
			await user.send(message)

def setup(bot):
	bot.add_cog(DM(bot))
