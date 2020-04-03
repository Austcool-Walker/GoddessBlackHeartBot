#              Send DMs to people using bots (Python)
import discord
import ast
import io
import random
import time
import json
import asyncio
from discord.ext.commands import Bot, Greedy
from discord import User
from discord.ext import commands

class DM(commands.Cog, name="DM"):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def pm(self, ctx, users: Greedy[User], *, message: str):
		for user in users:
			await user.send(message)

def setup(bot):
	bot.add_cog(DM(bot))
