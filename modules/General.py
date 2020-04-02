import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import time
import random
import json
import sys


class General(commands.Cog, name="General"):

    def __init__(self, bot):
        self.bot = bot
        self.information = json.loads(open('help.json', 'r').read())

    @commands.command(name='help')
    async def _help(self, beep, commands=None):
        if commands is None:
            embed = discord.Embed(title="I'm 女神ブラックハート! This is my list of commands!",
                              description="If you need help on a specific command, use ``Xhelp <command>``")
            for module in self.bot.cogs:
                if module == 'Debug':
                    continue
                cog = self.bot.get_cog(module)
                cogcmds = cog.get_commands()
                list = ""
                for c in cogcmds:
                    list += f"``{c}`` "
                embed.add_field(name=module, value=list, inline=False)
            embed.set_footer(icon_url=beep.message.author.avatar_url,
                             text="Requested by {}".format(beep.message.author.name))
        else:
            embed = self.commandhelp(commands)
        await beep.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        t_1 = time.perf_counter()
        await ctx.trigger_typing()
        t_2 = time.perf_counter()
        time_delta = round((t_2 - t_1) * 1000)
        responses = ['Pong!', 'Ack!', 'Whoa!', 'Pang!', 'How am I doing?']
        await ctx.send("{} ``Time: {}ms``".format(random.choice(responses), time_delta))

    @commands.command(aliases=['info'])
    async def about(self, beep):
        embed = discord.Embed(title="About 女神ブラックハート:", description="The Goddess Black Heart bot started out as  a random mad computer science experiment but evolved into a full scale bot!")
        embed.add_field(name="Author: ", value="Original Base Code from (<@310496481435975693>) forked by (<@318528448320634881>)", inline=False)
        embed.add_field(name="Stats: ", value="Guilds: **{}**\nUnique Players: **{}**\n"
                        .format(len(self.bot.guilds),sum(1 for _ in self.bot.get_all_members())))
        embed.add_field(name="Version: ", value="女神ブラックハート: **{}**\nPython: **{}**\nDiscord.py: **{}**"
                        .format(self.bot.version_code, sys.version, discord.__version__))
        embed.add_field(name="Source Code", value="https://github.com/Austcool-Walker/GoddessBlackHeartBot.git")
        embed.add_field(name="Discord Server", value="https://discord.gg/veVDS47")
        embed.set_image(url="https://cdn.discordapp.com/icons/692758311585579088/203473cf00ee5cde6cf7a5c52614464b.webp")
        embed.add_field(name="Invite", value="[Invite link](https://discordapp.com/api/oauth2/authorize?client_id=693568262813909072&permissions=8&scope=bot)")
        embed.set_footer(icon_url=beep.message.author.avatar_url,
                         text="Requested by {}".format(beep.message.author.name))
        await beep.send(embed=embed)

    @commands.command()
    async def user(self, ctx):
        try:
            target = ctx.message.mentions[0]
        except Exception:
            target = ctx.message.author
            await ctx.send("User not found or specified. Collecting information about sender...")
        roles = []
        for x in target.roles:
            roles.append(x.name)
        knownroles = "\n".join(roles)
        embed = discord.Embed(title="Information successfully collected!", description="Here's what we know about {} "
                                    "(also known as {})".format(target.name, target.display_name))
        embed.add_field(name="User ID: ", value=str(target.id), inline=False)
        embed.add_field(name="Current Roles: ", value=knownroles, inline=False)
        embed.add_field(name="Joined Discord on: ", value=target.created_at, inline=False)
        embed.set_thumbnail(url=target.avatar_url)
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text="Requested by {}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def avatar(self, ctx, *users:discord.User):
        """Returns the input users avatar."""
        if len(users) == 0:
            users = [ctx.message.author]
        for user in users:
            await ctx.send("`{0}`'s avatar is: {1}".format(user, user.avatar_url))

    @commands.command(pass_context=True, no_pm=True)
    async def serverinfo(self, ctx):
        """server info"""
        try:
            server = ctx.message.server
            online = str(sum(1 for member in server.members if member.status == discord.Status.online or member.status == discord.Status.idle))
            msg = ':desktop: **{0}** Information:\n'.format(server)
            msg += ":id:: `{0}`\n".format(server.id)
            msg += ":map: Region: __{0}__\n".format(str(server.region))
            msg += ":busts_in_silhouette: Users: **{0}**/{1}\n".format(online, len(server.members))
            msg += ":calendar_spiral: Created: `{0}`\n".format(str(server.created_at.strftime('%m/%d/%Y %H:%M:%S')))
            msg += ":bust_in_silhouette: Owner: `{0}`\n".format(server.owner)
            if server.verification_level:
                msg += ":exclamation: Verification Level: **{0}**\n".format(str(server.verification_level).upper())
            msg += ":speech_balloon: Default Channel: {0}\n".format(server.default_channel.mention)
            if ctx.message.server.afk_channel:
                msg += ":telephone_receiver: AFK Channel: {0}\n".format(ctx.message.server.afk_channel.mention)
                msg += ":keyboard: AFK Timeout: {0} minutes\n".format(str(int(int(ctx.message.server.afk_timeout)/60)))
            voice = 0
            text = 0
            for channel in server.channels:
                if channel.type == discord.ChannelType.text:
                    text += 1
                elif channel.type == discord.ChannelType.voice:
                    voice += 1
            msg += ":arrow_forward: Channels: `{0}` Text | `{1}` Voice | **{2}** Total\n".format(text, voice, str(len(server.channels)))
            msg += ":arrow_forward: Roles: `{0}`\n".format(str(len(server.roles)))
            if len(server.emojis) != 0:
                emotes = ""
                for emote in server.emojis:
                    emotes += "<:{0}:{1}>".format(emote.name, emote.id)
                msg += ":arrow_forward: Emotes: {0}\n".format(emotes)
            msg += ':art: Server Icon: {0}'.format(server.icon_url)
            await ctx.send(ctx.message.channel, msg)

#    @commands.command()
#    async def invite(self, ctx):
#        embed = discord.Embed(color=discord.Colour.dark_orange(), title="Are you going to invite me to your server?",
#                              description="Invite me by clicking [here](https://discordapp.com/api/oauth2/authorize?client_id=693568262813909072&permissions=8&scope=bot).")
#        embed.set_footer(icon_url=ctx.message.author.avatar_url, text="Requested by {}".format(ctx.message.author.name))
#        await ctx.send(embed=embed)

#    @commands.command()
#    async def server(self, ctx):
#        embed = discord.Embed(color=discord.Colour.dark_gold(), title="So you want to join my creator's server?",
#                              description="Come join the support server by clicking [here](https://discord.gg/veVDS47)")
#        embed.set_footer(icon_url=ctx.message.author.avatar_url, text="Requested by {}".format(ctx.message.author.name))
#        await ctx.send(embed=embed)

    @commands.command()
    async def suggest(self, ctx, *, report: str):
        channel = self.bot.get_channel(460669314933063680)
        color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Suggestion!", description="We got a suggestion from {}".format(ctx.message.author))
        embed.add_field(name="Suggestion: ", value=report)
        await channel.send(embed=embed)
        await ctx.send("Your suggestion has been sent.")

    @commands.command()
    async def report(self, ctx, *, report: str):
        channel = self.bot.get_channel(460666448352641026)
        color = discord.Colour.red()
        embed = discord.Embed(color=color, title="Bug report!", description="We got a bug report from {}".format(ctx.message.author))
        embed.add_field(name="Full report: ", value=report)
        await channel.send(embed=embed)
        await ctx.send("Your report has been sent.")

#    @commands.command()
#    async def github(self, ctx):
#        embed = discord.Embed(color=discord.Colour.light_grey(), title="Are you a programmer and want to help?",
#                              description="You should click [here](https://github.com/Austcool-Walker/GoddessBlackHeartBot.git) to see my repository. I am an open-source bot.")
#        embed.set_footer(icon_url=ctx.message.author.avatar_url, text="Requested by {}".format(ctx.message.author.name))
#        await ctx.send(embed=embed)

#    @commands.command()
#    async def upvote(self, ctx):
#        embed = discord.Embed(color=discord.Colour.blue(), title="Come vote for 女神ブラックハート!",
#                              description="Do you really like using Axiro? You can upvote it by clicking [here](https://discordbots.org/bot/458834071796187149/vote)!")
#        embed.set_footer(icon_url=ctx.message.author.avatar_url, text="Requested by {}".format(ctx.message.author.name))
#        await ctx.send(embed=embed)

    def commandhelp(self, command):
        embed = discord.Embed(title="Help on {}".format(command), description="What we know about this command...")
        try:
            embed.add_field(name="Usage: ", value=self.information[command], inline=False)
        except Exception:
            embed.add_field(name="Error: ", value="This command does not exist.", inline=False)
        return embed


def setup(bot):
    bot.add_cog(General(bot))
