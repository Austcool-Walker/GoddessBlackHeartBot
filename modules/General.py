import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import time
import random
import json
import sys
import os
import platform
import datetime

class General(commands.Cog, name="General"):

    def __init__(self, bot, **attr):
        self.bot = bot
        self.information = json.loads(open('help.json', 'r').read())

    @staticmethod
    def _newImage(width, height, color):
        return Image.new("L", (width, height), color)

    @staticmethod
    def _getRoles(roles):
        string = ''
        for role in roles[::-1]:
            if not role.is_default():
                string += f'{role.mention}, '
        if string is '':
            return 'None'
        else:
            return string[:-2]

    @staticmethod
    def _getEmojis(emojis):
        string = ''
        for emoji in emojis:
            string += str(emoji)
        if string is '':
            return 'None'
        else:
            return string[:1000] #The maximum allowed charcter amount for embed fields

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

    @commands.command()
    async def time(self, ctx):
        now = datetime.datetime.now()
        embed = discord.Embed(color=0xff00ec, title="Time.",
                            description="Current date and time : ")
        embed.add_field(name='Date/Time', value=now.strftime("+%Y.%m.%d %H:%M:%S", inline=True)
        await ctx.send(embed=embed)

    @commands.command(aliases=['info'])
    async def about(self, beep):
        embed = discord.Embed(title="About 女神ブラックハート:", description="The Goddess Black Heart bot started out as  a random mad computer science experiment but evolved into a full scale bot!")
        embed.add_field(name="Author: ", value="Original Base Code from (<@!310496481435975693>) forked by (<@!318528448320634881>)", inline=False)
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

    @commands.command(pass_context=True, aliases=['guild', 'membercount'])
    async def serverinfo(self, ctx):
        '''Returns information about the current Discord Guild'''
        emojis = self._getEmojis(ctx.guild.emojis)
        #print(emojis)
        roles = self._getRoles(ctx.guild.roles)
        embed = discord.Embed(color=0xf1c40f) #Golden
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text='Emojis may be missing')
        embed.add_field(name='Name', value=ctx.guild.name, inline=True)
        embed.add_field(name='ID', value=ctx.guild.id, inline=True)
        embed.add_field(name='Owner', value=ctx.guild.owner, inline=True)
        embed.add_field(name='Region', value=ctx.guild.region, inline=True)
        embed.add_field(name='Members', value=ctx.guild.member_count, inline=True)
        embed.add_field(name='Created on', value=ctx.guild.created_at.strftime('%d.%m.%Y'), inline=True)
        if ctx.guild.system_channel:
            embed.add_field(name='Standard Channel', value=f'#{ctx.guild.system_channel}', inline=True)
        embed.add_field(name='AFK Voice Timeout', value=f'{int(ctx.guild.afk_timeout / 60)} min', inline=True)
        embed.add_field(name='Guild Shard', value=ctx.guild.shard_id, inline=True)
        embed.add_field(name='Rolls', value=roles, inline=True)
        embed.add_field(name='Custom Emojis', value=emojis, inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def host(self, ctx):
        embed = discord.Embed(color=0xff00ec, title="Host Information.",
                                description="Here is what we know about the machine hosting the bot.")
        embed.add_field(name='Platform', value=platform.platform(), inline=True)
        embed.add_field(name='OS Type', value=os.name, inline=True)
        embed.add_field(name='OS Release', value=platform.release(), inline=True)
        embed.add_field(name='OS Version', value=platform.version(), inline=True)
        embed.add_field(name='Hostname', value=platform.node(), inline=True)
        embed.add_field(name='CPU Architecture', value=platform.machine(), inline=True)
        embed.add_field(name='Operating System', value=platform.system(), inline=True)
        await ctx.send(embed=embed)

#    @commands.command()
#    async def invite(self, ctx):
#        embed = discord.Embed(color=discord.Colour.dark_orange(), title="Are you going to invite me to your server?",
#                              description="Invite me by clicking [here](https://discordapp.com/api/oauth2/authorize?client_id=693568262813909072&permissions=8&scope=bot).")
#        embed.set_footer(icon_url=ctx.message.author.avatar_url, text="Requested by {}".format(ctx.message.author.name))
#        await ctx.send(embed=embed)

    @commands.command()
    async def server(self, ctx):
        embed = discord.Embed(color=discord.Colour.dark_gold(), title="So you want to join my creator's server?",
                              description="Come join the support server by clicking [here](https://discord.gg/veVDS47)")
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text="Requested by {}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

    @commands.command()
    async def suggest(self, ctx, *, report: str):
        channel = self.bot.get_channel(708423667574636595)
        color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Suggestion!", description="We got a suggestion from {}".format(ctx.message.author))
        embed.add_field(name="Suggestion: ", value=report)
        await channel.send(embed=embed)
        await ctx.send("Your suggestion has been sent.")

    @commands.command()
    async def report(self, ctx, *, report: str):
        channel = self.bot.get_channel(708423667574636595)
        color = discord.Colour.red()
        embed = discord.Embed(color=color, title="Bug report!", description="We got a bug report from {}".format(ctx.message.author))
        embed.add_field(name="Full report: ", value=report)
        await channel.send(embed=embed)
        await ctx.send("Your report has been sent.")

    @commands.command()
    async def github(self, ctx):
        embed = discord.Embed(color=discord.Colour.light_grey(), title="Are you a programmer and want to help?",
                              description="You should click [here](https://github.com/Austcool-Walker/GoddessBlackHeartBot.git) to see my repository. I am an open-source bot.")
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text="Requested by {}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

#    @commands.command()
#    async def upvote(self, ctx):
#        embed = discord.Embed(color=discord.Colour.blue(), title="Come vote for 女神ブラックハート!",
#                              description="Do you really like using 女神ブラックハート? You can upvote it by clicking [here](https://discordbots.org/bot/458834071796187149/vote)!")
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
