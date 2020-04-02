#              Send DMs to people using bots (Python)
import discord
from discord.ext import commands

class Reactions(commands.Cog, name="Reactions"):

    def __init__(self, bot, Client):
#        self.bot = bot
        bot = Client

    @Client.event
    async def on_message(message):
            channel = message.channel
            if message.content.startswith('rage'):
                await ctx.message.add_reaction('🤬')

    @Client.event
    async def on_message(message):
            channel = message.channel
            if message.content.startswith('mad', 'angry'):
                await ctx.message.add_reaction('😡')

    @Client.event
    async def on_message(message):
            channel = message.channel
            if message.content.startswith('sad' , 'despair'):
                await ctx.message.add_reaction('😭')

    @Client.event
    async def on_message(message):
            channel = message.channel
            if message.content.startswith('love'):
                await ctx.message.add_reaction('❤️')

    @Client.event
    async def on_message(message):
            channel = message.channel
            if message.content.startswith('happy', 'joy'):
                await ctx.message.add_reaction('😁')


def setup(bot):
    bot.add_cog(Reactions(bot))
