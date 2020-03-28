#															Send DMs to people using bots (Python)
import asyncio
import converter
from discord.ext.commands import Bot, Greedy
from discord import User

# This is prefix of my bot
bot = Bot(command_prefix='!')

# Lets send A DM
@bot.command()
async def spam(ctx, victim: discord.User, amount, *, message):
    for _ in range(amount):
        await victim.send(message)


# Finally add your token number and run the client
bot.run("Discord Auth Token Here!")


