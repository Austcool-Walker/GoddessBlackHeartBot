import sys
import os
import random
import discord
import asyncio
import aiohttp
from discord.ext import commands

# Authorized User_ID's
AJW_Admins = (219220084982415362, 318528448320634881, 217408285542842368, 617456938904453190)

class Admin(commands.Cog, name="Admin"):
    '''Commands for the bot admin'''

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))

    async def cog_check(self, ctx):
        return await ctx.bot.is_owner(ctx.author)

    @commands.command(aliases=['quit'], hidden=True)
    @commands.is_owner()    
    async def shutdown(self, ctx):
        '''Turn me off :( (BOT OWNER ONLY)'''
        await ctx.send('**:ok:** Bye!')
        #self.bot.gamesLoop.cancel()
        await self.bot.logout()
        sys.exit(0)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def restart(self, ctx):
        ''''Restart me (BOT OWNER ONLY)'''
        await ctx.send('**:ok:** See you soon!')
        try:
                await self.bot.logout()
        except:
            pass
        finally:
            os.system("python3 GoddessBlackHeartBot.py")
        await ctx.send('**:ok_hand:** Restart Successful!')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def botavatar(self, ctx, url: str):
        '''Set a new avatar (BOT OWNER ONLY)'''
        tempAvaFile = 'tempAva.png'
        async with aiohttp.get(''.join(url)) as img:
            with open(tempAvaFile, 'wb') as f:
                f.write(await img.read())
        f = discord.File(tempAvaFile)
        await self.bot.edit_settings(avatar=f.read())
        os.remove(tempAvaFile)
        asyncio.sleep(2)
        await ctx.send('**:ok:** My new avatar!\n %s' % self.bot.user.avatar_url)

    @commands.command(hidden=True, aliases=['game'])
    async def changegame(self, ctx, status: str, gameType: str, *, gameName: str):
        if ctx.author.id in AJW_Admins:
            '''Changes the game currently playing (BOT OWNER ONLY)'''
        gameType = gameType.lower()
        if gameType == 'playing':
            type2 = discord.ActivityType.playing
        elif gameType == 'watching':
            type2 = discord.ActivityType.watching
        elif gameType == 'listening':
            type2 = discord.ActivityType.listening
        elif gameType == 'streaming':
            type2 = discord.ActivityType.streaming
        status = status.lower()
        if status == 'offline' or status == 'off' or status == 'invisible':
            discordStatus = discord.Status.invisible
        elif status == 'idle':
            discordStatus = discord.Status.idle
        elif status == 'dnd' or status == 'disturb':
            discordStatus = discord.Status.dnd
        else:
            discordStatus = discord.Status.online
        guildsCount = len(self.bot.guilds)
        memberCount = len(list(self.bot.get_all_members()))
        gameName = gameName.format(guilds = guildsCount, members = memberCount)
        await self.bot.change_presence(status=discordStatus, activity=discord.Activity(type=type2, name=gameName))
        await ctx.send(f'**:ok:** Changed the status & game to: **{discordStatus}** {gameType} **{gameName}**')

    @commands.command(hidden=True)
    async def changestatus(self, ctx, status: str):
        if ctx.author.id in AJW_Admins:
            '''Changes bot online status (BOT OWNER ONLY)'''
        status = status.lower()
        if status == 'offline' or status == 'off' or status == 'invisible':
            discordStatus = discord.Status.invisible
        elif status == 'idle':
            discordStatus = discord.Status.idle
        elif status == 'dnd' or status == 'disturb':
            discordStatus = discord.Status.dnd
        else:
            discordStatus = discord.Status.online
        await self.bot.change_presence(status=discordStatus)
        await ctx.send(f'**:ok:** to another status: **{discordStatus}**')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def name(self, ctx, name: str):
        '''changes bot global name (BOT OWNER ONLY)'''
        await self.bot.edit_profile(username=name)
        msg = f':ok: change my name: **{name}**'
        await ctx.send(msg)

    @commands.command(hidden=True, aliases=['guilds'])
    async def servers(self, ctx):
        '''Lists the current connected guilds (BOT OWNER ONLY)'''
        msg = '```js\n'
        msg += '{!s:19s} | {!s:>5s} | {} | {}\n'.format('ID', 'Member', 'Name', 'Owner')
        for guild in self.bot.guilds:
            msg += '{!s:19s} | {!s:>5s}| {} | {}\n'.format(guild.id, guild.member_count, guild.name, guild.owner)
        msg += '```'
        await ctx.send(msg)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def leaveserver(self, ctx, *, guild_id):
        guild = discord.utils.get(self.bot.guilds, name=guild_id)
        if guild is None:
            await ctx.send("I don't recognize that guild ID.")
            return
        await self.bot.leave_guild(guild)
        await ctx.send(f":ok_hand: Exit from: {guild.name} ({guild.id}) successful!")
    

    @commands.command(hidden=True)
    async def echo(self, ctx, channel: str, *message: str):
        '''Outputs a message as a bot on a specific channel (BOT OWNER ONLY)'''
        ch = self.bot.get_channel(int(channel))
        msg = ' '.join(message)
        await ch.send(msg)
        await ctx.message.delete()

    @commands.command(hidden=True)
    async def discriminator(self, ctx, disc: str):
        '''Returns users with the respective discriminator'''

        discriminator = disc
        memberList = ''

        for guild in self.bot.guilds:
            for member in guild.members:
                if member.discriminator == discriminator and member.discriminator not in memberList:
                    memberList += f'{member}\n'

        if memberList:
            await ctx.send(memberList)
        else:
            await ctx.send(":x: Couldn't find anyone")
    @commands.command(hidden=True)
    @commands.bot_has_permissions(manage_nicknames = True)
    async def nickname(self, ctx, *name):
        '''Changes the server nickname from the bot (BOT OWNER ONLY)'''
        nickname = ' '.join(name)
        await ctx.me.edit(nick=nickname)
        if nickname:
            msg = f':ok: Change my server nickname: **{nickname}**'
        else:
            msg = f':ok: Reset from my server nickname: **{ctx.me.name}**'
        await ctx.send(msg)

    @commands.command(hidden=True)
    @commands.bot_has_permissions(manage_nicknames = True)
    async def setnickname(self, ctx, member: discord.Member=None, *name):
        '''Changes a user's nickname (BOT OWNER ONLY)'''
        if member == None:
            member = ctx.author
        nickname = ' '.join(name)
        await member.edit(nick=nickname)
        if nickname:
            msg = f':ok: Change nickname of {member} to: **{nickname}**'
        else:
            msg = f':ok: Reset nickname for {member} on: **{member.name}**'
        await ctx.send(msg)

    @commands.command(hidden=True)
    async def geninvite(self, ctx, serverid: str):
        '''Generates an invite for a guild if possible (BOT OWNER ONLY)'''
        guild = self.bot.get_guild(int(serverid))
        invite = await ctx.create_invite(guild, max_uses=1, unique=False)
        msg = f'Invite for **{guild.name}** ({guild.id})\n{invite.url}'
        await ctx.author.send(msg)

    @commands.command(hidden=True, aliases=['wichteln'])
    async def wichtel(self, ctx, *participants: str):
        '''Useful for the Community Wichtel Event 2018 (BOT OWNER ONLY)'''
        participantsList = list(participants)
        random.shuffle(participantsList)
        msg = 'Imp partners have been determined:\n```'
        for i, val in enumerate(participantsList):
            if i == len(participantsList) - 1:
                msg += f'{val.ljust(10)} ===> {participantsList[0]}\n'
            else:
                msg += f'{val.ljust(10)} ===> {participantsList[i + 1]}\n'

        msg += '```'
        await ctx.send(msg)

    @commands.command(hidden=True)
    async def test(self, ctx):
        '''Test Test Test'''
        await ctx.send('Test')
        await self.bot.AppInfo.owner.send('Test')
        await ctx.send(self.bot.cogs)

def setup(bot):
    bot.add_cog(Admin(bot))
