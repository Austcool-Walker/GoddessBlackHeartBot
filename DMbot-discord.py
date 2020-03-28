#															Send DMs to people using bots (Python)
import asyncio
from discord.ext.commands import Bot, Greedy
from discord import User, Converter

# This is prefix of my bot
bot = Bot(command_prefix='!')

# Lets send A DM
@bot.command()
async def pm(ctx, users: Greedy[User], *, message):
    for user in users:
        await user.send(message)


# Finally add your token number and run the client
bot.run("Discord Auth Token Here!")


