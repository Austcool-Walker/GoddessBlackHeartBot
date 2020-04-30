#              Change Bots Prefix (Python)
import discord
from discord.ext.commands import Bot
from discord.ext import commands

class Prefix(commands.Cog, name="Prefix"):

	def __init__(self, bot):
		self.bot = bot

custom_prefixes = {}
#You'd need to have some sort of persistance here,
#possibly using the json module to save and load
#or a database
default_prefixes = ['.']

async def determine_prefix(bot, message):
    guild = message.guild
    #Only allow custom prefixs in guild
    if guild:
        return custom_prefixes.get(guild.id, default_prefixes)
    else:
        return default_prefixes

bot = commands.Bot(command_prefix = determine_prefix, ...)
bot.run()

@commands.command()
@commands.guild_only()
async def setprefix(self, ctx, *, prefixes=""):
    #You'd obviously need to do some error checking here
    #All I'm doing here is if prefixes is not passed then
    #set it to default 
    custom_prefixes[ctx.guild.id] = prefixes.split() or default_prefixes
    await ctx.send("Prefixes set!")

def setup(bot):
	bot.add_cog(Prefix(bot))
