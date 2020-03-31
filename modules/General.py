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
    @commands.cooldown(1, 2, BucketType.user)
    @commands.guild_only()
    async def _help(self, beep, commands=None):
        if commands is None:
            embed = discord.Embed(title="I'm Axiro! This is my list of commands!",
                              description="If you need help on a specific command, use ``x!help <command>``")
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
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def ping(self, ctx):
        t_1 = time.perf_counter()
        await ctx.trigger_typing()
        t_2 = time.perf_counter()
        time_delta = round((t_2 - t_1) * 1000)
        responses = ['Pong!', 'Ack!', 'Whoa!', 'Pang!', 'How am I doing?']
        await ctx.send("{} ``Time: {}ms``".format(random.choice(responses), time_delta))

    @commands.command(aliases=['info'])
    @commands.cooldown(1, 2, BucketType.user)
    @commands.guild_only()
    async def about(self, beep):
        embed = discord.Embed(title="About Axiro:", description="This bot was created to do what most "
                                    "bots should do, and then some really weird things.")
        embed.add_field(name="Author: ", value="tangalbert919 (The Freaking iDroid)", inline=False)
        embed.add_field(name="Stats: ", value="Guilds: **{}**\nUnique Players: **{}**\n"
                        .format(len(self.bot.guilds),sum(1 for _ in self.bot.get_all_members())))
        embed.add_field(name="Version: ", value="Axiro: **{}**\nPython: **{}**\nDiscord.py: **{}**"
                        .format(self.bot.version_code, sys.version, discord.__version__))
        embed.set_footer(icon_url=beep.message.author.avatar_url,
                         text="Requested by {}".format(beep.message.author.name))
        await beep.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
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

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def invite(self, ctx):
        embed = discord.Embed(color=discord.Colour.dark_orange(), title="Are you going to invite me to your server?",
                              description="Invite me by clicking [here](https://discordapp.com/api/oauth2/authorize?client_id=458834071796187149&permissions=8&scope=bot).")
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text="Requested by {}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def server(self, ctx):
        embed = discord.Embed(color=discord.Colour.dark_gold(), title="So you want to join my creator's server?",
                              description="Come join the support server by clicking [here](https://discord.gg/NEpsy8h)")
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text="Requested by {}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def suggest(self, ctx, *, report: str):
        channel = self.bot.get_channel(460669314933063680)
        color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Suggestion!", description="We got a suggestion from {}".format(ctx.message.author))
        embed.add_field(name="Suggestion: ", value=report)
        await channel.send(embed=embed)
        await ctx.send("Your suggestion has been sent.")

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def report(self, ctx, *, report: str):
        channel = self.bot.get_channel(460666448352641026)
        color = discord.Colour.red()
        embed = discord.Embed(color=color, title="Bug report!", description="We got a bug report from {}".format(ctx.message.author))
        embed.add_field(name="Full report: ", value=report)
        await channel.send(embed=embed)
        await ctx.send("Your report has been sent.")

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def github(self, ctx):
        embed = discord.Embed(color=discord.Colour.light_grey(), title="Are you a programmer and want to help?",
                              description="You should click [here](https://github.com/tangalbert919/WeirdnessBot) to see my repository. I am an open-source bot.")
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text="Requested by {}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def upvote(self, ctx):
        embed = discord.Embed(color=discord.Colour.blue(), title="Come vote for Axiro!",
                              description="Do you really like using Axiro? You can upvote it by clicking [here](https://discordbots.org/bot/458834071796187149/vote)!")
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text="Requested by {}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

    def commandhelp(self, command):
        embed = discord.Embed(title="Help on {}".format(command), description="What we know about this command...")
        try:
            embed.add_field(name="Usage: ", value=self.information[command], inline=False)
        except Exception:
            embed.add_field(name="Error: ", value="This command does not exist.", inline=False)
        return embed


def setup(bot):
    bot.add_cog(General(bot))
