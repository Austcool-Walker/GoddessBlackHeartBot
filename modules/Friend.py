#              Send Friend requests to people using bots (Python)
import discord

class Friend(commands.Cog, name="Friend"):

	def __init__(self, bot):
		self.bot = bot

@self.bot.event
async def on_ready():
    with open("id.txt") as infile:
        for line in infile:
            id = int(line)
            user = await client.get_user_info(id)
            try:
                await sleep(.305)
                await user.send_friend_request()
            except (discord.Forbidden, discord.HTTPException):
                continue

def setup(bot):
	bot.add_cog(Friend(bot))
