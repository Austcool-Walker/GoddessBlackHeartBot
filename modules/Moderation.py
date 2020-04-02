import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


class Moderation(commands.Cog, name="Moderation"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.User, *, reason: str):
        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).kick_members:
            await ctx.send(":x: I do not have permission to kick players.")
            return
        try:
            await ctx.message.guild.kick(user, reason=reason)
        except Exception:
            await ctx.send(":x: Player kick failed.")
            return
        await ctx.send(":white_check_mark: Player {} has been kicked from the server.".format(user.name))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User, *, reason: str):
        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).ban_members:
            await ctx.send(":x: I do not have permission to ban players.")
            return
        try:
            await ctx.message.guild.ban(user, reason=reason)
        except Exception:
            await ctx.send(":x: I completely failed to ban that player.")
            return
        await ctx.send(":white_check_mark: Player {} has been banned from the server.".format(user.name))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: discord.Member):
        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).manage_roles:
            await ctx.send(":x: I do not have permission to manage roles.")
            return
        try:
            await ctx.message.channel.category.set_permissions(user, send_messages=False, add_reactions=False)
        except Exception:
            await ctx.send("I was unable to mute that player.")
            return
        await ctx.send(":white_check_mark: Player {} has been muted.".format(user.display_name))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: discord.Member):
        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).manage_roles:
            await ctx.send(":x: I do not have permission to manage roles.")
            return
        try:
            await ctx.message.channel.category.set_permissions(user, overwrite=None)
        except Exception:
            await ctx.send("I was unable to unmute that player.")
            return
        await ctx.send(":white_check_mark: Player {} has been unmuted.".format(user.display_name))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def prune(self, ctx, number: int):
        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).manage_messages:
            await ctx.send("I do not have permission to delete messages.")
            return
        if number > 500:
            await ctx.send("Please specify a lower number.")
            return
        to_delete = []
        async for message in ctx.message.channel.history(limit=number+1):
            to_delete.append(message)
        while to_delete:
            if len(to_delete) > 1:
                await ctx.message.channel.delete_messages(to_delete[:100])
                to_delete = to_delete[100:]
            else:
                await to_delete.delete()
                to_delete = []
            await asyncio.sleep(1.5)


def setup(bot):
    bot.add_cog(Moderation(bot))