from discord.ext import commands
import discord
import io
from contextlib import redirect_stdout
import subprocess
import textwrap
import traceback
import requests
from os import listdir
from os.path import isfile, join
from asyncio import sleep
import subprocess
from clint.textui import progress

# Authorized User_ID's
AJW_Admins = (219220084982415362, 318528448320634881, 217408285542842368, 617456938904453190)

class Debug(commands.Cog, command_attrs=dict(hidden=True), name="Debug"):

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command()
    async def reload(self, ctx, *, module):
        if ctx.author.id in AJW_Admins:
            """Reloads a module."""
            try:
                self.bot.unload_extension("modules." + module)
                self.bot.load_extension("modules." + module)
            except Exception:
                await ctx.send(f'```py\n{traceback.format_exc()}\n```')
            else:
                await ctx.send(':ok_hand:')

    @commands.command()
    async def load(self, ctx, *, module):
        if ctx.author.id in AJW_Admins:
            """Loads a new module."""
            try:
                self.bot.load_extension("modules." + module)
            except Exception:
                await ctx.send(f'```py\n{traceback.format_exc()}\n```')
            else:
                await ctx.send(':ok_hand:')

    @commands.command()
    async def unload(self, ctx, *, module):
        if ctx.author.id in AJW_Admins:
            """Unloads a module."""
            try:
                self.bot.unload_extension("modules." + module)
            except Exception:
                await ctx.send(f'```py\n{traceback.format_exc()}\n```')
            else:
                await ctx.send(':ok_hand:')

    @commands.command()
    async def say(self, ctx, *, message: str):
        if ctx.author.id in AJW_Admins:
            await ctx.message.delete()
            await ctx.send(message)

    """The following two definitions come from the Monika bot (dev.py module)."""
    """It has been modified so only the creator can run this command."""
    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

    @commands.command()
    async def eval(self, ctx, *, message: str):
        if ctx.author.id in AJW_Admins:
            env = {
                'bot': self.bot,
                'ctx': ctx,
                'channel': ctx.channel,
                'author': ctx.author,
                'guild': ctx.guild,
                'message': ctx.message,
                '_': self._last_result
            }

            env.update(globals())

            body = self.cleanup_code(message)
            stdout = io.StringIO()

            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

            try:
                exec(to_compile, env)
            except Exception as e:
                return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

            func = env['func']
            try:
                with redirect_stdout(stdout):
                    ret = await func()
            except Exception:
                value = stdout.getvalue()
                await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
            else:
                value = stdout.getvalue()
                try:
                    await ctx.message.add_reaction('👌')
                except:
                    pass

                if ret is None:
                    if value:
                        await ctx.send(f'```py\n{value}\n```')
                else:
                    self._last_result = ret
                    await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command()
    async def pull(self, ctx):
        if ctx.author.id in AJW_Admins:
            c = subprocess.call(('git', 'pull'))
            if c != 0:
                await ctx.send("Updating from Git failed.")
                return
            await ctx.send("Successfully updated from Git.")

    @commands.command()
    async def download(self, ctx, link):
        if ctx.author.id in AJW_Admins:
            file = [f for f in listdir('./modules/') if isfile(join('./modules/', f))]
            r = requests.get(link)
            newmod = open('./modules/{}.py'.format('module-{}'.format(len(file))), 'wb+')
            try:
                newmod.write(r.content)
            except:
                await ctx.send(f'```py\n{traceback.format_exc()}\n```')
            await ctx.send('Downloaded new module ending in {}'.format(len(file)))

    @commands.command()
    async def dl(self, ctx, url, path):
        '''Set a new avatar (BOT OWNER ONLY)'''
        if ctx.author.id in AJW_Admins:
                r = requests.get(f'{1}', stream=True)
                with open(f'{2}', 'wb') as f:
                        total_length = int(r.headers.get('content-length'))
                        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                                if chunk:
                                    f.write(chunk)
                                    f.flush()
        await ctx.send(f':white_check_mark: downloaded file from **{url}** saved **{path}**')

    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx, id=None):
        if not self.bot.usedatabase:
            await ctx.send("This command requires a running database to work.")
            return
        elif id is None:
            await ctx.send("You need a user ID.")
            return
        check_blacklist = "SELECT blacklist FROM users WHERE id = $1"
        temp = await self.bot.db.fetchval(check_blacklist, int(id))
        if not temp:
            await ctx.send("This user is not in the database.")
            return
        blacklist_value = int(temp)
        new_value = 0 if blacklist_value != 0 else 1
        sql = "UPDATE users SET blacklist = $1 where id = $2"
        await self.bot.db.execute(sql, str(new_value), int(id))
        if new_value == 0:
            await ctx.send("User has been removed from the blacklist.")
        else:
            await ctx.send("User has been added to the blacklist.")

def setup(bot):
    bot.add_cog(Debug(bot))
