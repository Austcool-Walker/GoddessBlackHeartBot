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

#    @commands.command()
#    @commands.has_permissions(ban_members=True)
#    async def ban(self, ctx, user: discord.User, *, reason: str):
#        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).ban_members:
#            await ctx.send(":x: I do not have permission to ban players.")
#            return
#        try:
#            await ctx.message.guild.ban(user, reason=reason)
#        except Exception:
#            await ctx.send(":x: I completely failed to ban that player.")
#            return
#        await ctx.send(":white_check_mark: Player {} has been banned from the server.".format(user.name))

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, userid: int=None, *reason):
        '''Bans a member with a reason (MOD ONLY)
        The user ID must be specified, name + discriminator is not enough
        example:
        -----------
        :ban 102815825781596160
        '''
        user = self.bot.get_user(id=userid)
        if user is not None:
            if reason:
                reason = ' '.join(reason)
            else:
                reason = None
            await ctx.guild.ban(user, reason=reason)
        else:
            await ctx.send(":white_check_mark: Player <@!{}> has been banned from the server.".format(userid))

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
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, user: int = None, *, reason=None):
        """Unban a person from the guild"""
        if user is None:
            return await ctx.send("Please provide the user's ID to unban him.")
        elif len(str(user)) > 18 or len(str(user)) < 18:
            return await ctx.send("Please provide a valid user's ID")
        try:
            await ctx.guild.unban(discord.Object(user), reason=reason)
            await ctx.send(":white_check_mark: Successfully unbanned the user: {}.".format(user.display_name))
        except (discord.Forbidden, discord.HTTPException):
            await ctx.send(":negative_squared_cross_mark: Unban failed! or No user specified!") 

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def bans(self, ctx):
        '''Lists currently banned users (MOD ONLY)'''
        users = await ctx.guild.bans()
        if len(users) > 0:
            msg = f'`{"ID":21}{"Name":25} Reason\n'
            for entry in users:
                userID = entry.user.id
                userName = str(entry.user)
                if entry.user.bot:
                    username = '🤖' + userName #:robot: emoji
                reason = str(entry.reason) #Could be None
                msg += f'{userID:<21}{userName:25} {reason}\n'
            embed = discord.Embed(color=0xe74c3c) #Red
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text=f'Server: {ctx.guild.name}')
            embed.add_field(name='Ranks', value=msg + '`', inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send('**:negative_squared_cross_mark:** There are no banned users!')

    @commands.command(alias=['clearreactions'])
    @commands.has_permissions(manage_messages = True)
    async def removereactions(self, ctx, messageid : str):
        '''Removes all emoji reactions from a message (MOD ONLY)
        example:
        -----------
        :removereactions 247386709505867776
        '''
        message = await ctx.channel.get_message(messageid)
        if message:
            await message.clear_reactions()
        else:
            await ctx.send('**:x:** Could not find a message with this ID!')

    @commands.command()
    async def permissions(self, ctx):
        '''Lists all rights of the bot'''
        permissions = ctx.channel.permissions_for(ctx.me)

        embed = discord.Embed(title=':customs:  Permissions', color=0x3498db) #Blue
        embed.add_field(name='Server', value=ctx.guild)
        embed.add_field(name='Channel', value=ctx.channel, inline=False)

        for item, valueBool in permissions:
            if valueBool == True:
                value = ':white_check_mark:'
            else:
                value = ':x:'
            embed.add_field(name=item, value=value)

        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    async def hierarchy(self, ctx):
        '''Lists the role hierarchy of the current server'''
        msg = f'Role hierarchy for servers **{ctx.guild}**:\n\n'
        roleDict = {}

        for role in ctx.guild.roles:
            if role.is_default():
                roleDict[role.position] = 'everyone'
            else:
                roleDict[role.position] = role.name

        for role in sorted(roleDict.items(), reverse=True):
            msg += role[1] + '\n'
        await ctx.send(msg)

    @commands.command(alies=['setrole', 'sr'])
    @commands.has_permissions(manage_roles = True)
    async def setrank(self, ctx, member: discord.Member=None, *rankName: str):
        '''Assigns a rank to a user
        example:
        -----------
        :setrole @Der-Eddy#6508 Member
        '''
        rank = discord.utils.get(ctx.guild.roles, name=' '.join(rankName))
        if member is not None:
            await member.add_roles(rank)
            await ctx.send(f':white_check_mark: Rolle **{rank.name}** was on **{member.name}** distributed')
        else:
            await ctx.send(':no_entry: You have to specify a user!')

    @commands.command(pass_context=True, alies=['rmrole', 'removerole', 'removerank'])
    @commands.has_permissions(manage_roles = True)
    async def rmrank(self, ctx, member: discord.Member=None, *rankName: str):
        '''Eremoves a rank from a user
        example:
        -----------
        :rmrole @Der-Eddy#6508 Member
        '''
        rank = discord.utils.get(ctx.guild.roles, name=' '.join(rankName))
        if member is not None:
            await member.remove_roles(rank)
            await ctx.send(f':white_check_mark: Rolle **{rank.name}** was from **{member.name}** away')
        else:
            await ctx.send(':no_entry: You have to specify a user!')

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