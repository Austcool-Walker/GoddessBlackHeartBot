import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import random


class Economy(commands.Cog, name="Economy"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def balance(self, ctx):
        if not self.bot.usedatabase:
            await ctx.send("This command requires a running database to work.")
            return
        try:
            user = ctx.message.mentions[0]
        except Exception:
            user = ctx.message.author
        if user.id == self.bot.user.id:
            await ctx.send("I do not need money, since I'm a bot.")
            return
        sql = "SELECT money FROM users WHERE id = $1"
        temp = await self.bot.db.fetchval(sql, user.id)
        money = int(temp)
        if user.id != ctx.message.author.id:
            await ctx.send(":chicken: **{} has {} chickens.**".format(user.name, money))
        else:
            await ctx.send(":chicken: **You have {} chickens.**".format(money))

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def pay(self, ctx, user: discord.User, payment):
        if not self.bot.usedatabase:
            await ctx.send("This command requires a running database to work.")
            return
        try:
            check = int(payment)
        except Exception:
            await ctx.send("Please specify an actual amount.")
            return
        if user.id == self.bot.user.id:
            await ctx.send("You can't give me money, since I'm a bot.")
            return
        sql = "SELECT money FROM users WHERE id = $1"
        payer = await self.bot.db.fetchval(sql, ctx.message.author.id)
        receiver = await self.bot.db.fetchval(sql, user.id)
        money = int(payer)
        money_two = int(receiver)
        if money < check:
            await ctx.send("You do not have enough chickens to perform this payment.")
            return
        elif check < 0:
            await ctx.send("Using negative numbers will not work.")
            return
        paid = money - check
        paid_two = money_two + check
        next_sql = "UPDATE users SET money = $1 WHERE id = $2"
        await self.bot.db.execute(next_sql, str(paid), ctx.message.author.id)
        await self.bot.db.execute(next_sql, str(paid_two), user.id)
        await ctx.send("Successfully paid {} chickens to {}!".format(payment, user.name))

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def gamble(self, ctx, money):
        if not self.bot.usedatabase:
            await ctx.send("This command requires a running database to work.")
            return
        try:
            check = int(money)
        except Exception:
            await ctx.send("Please specify an actual amount.")
            return
        if check < 0:
            await ctx.send("Gambling a negative amount of chickens, eh? Nice try.")
            return
        sql = "SELECT money FROM users WHERE id = $1"
        balance = await self.bot.db.fetchval(sql, ctx.message.author.id)
        if balance < money:
            await ctx.send("You do not have enough chickens for this gamble!")
            return
        raw_chance = 10  # 90% of the time, gamblers will lose their chickens.
        did_i_win = random.randint(1, 100)
        if did_i_win <= raw_chance:
            result = int(balance) + int((check / 2))
            await ctx.send("Congrats, you won {} chickens and got to keep what you bet!".format(int(check / 2)))
        else:
            result = int(balance) - check
            await ctx.send("You just lost {} chickens in a gamble! :frowning:".format(check))
        next_sql = "UPDATE users SET money = $1 WHERE id = $2"
        await self.bot.db.execute(next_sql, str(result), ctx.message.author.id)

    @commands.command()
    @commands.cooldown(1, 86400, BucketType.user)
    @commands.guild_only()
    async def daily(self, ctx):
        if not self.bot.usedatabase:
            await ctx.send("This command requires a running database to work.")
            return
        try:
            user = ctx.message.mentions[0]
        except Exception:
            user = ctx.message.author
        if user.id == self.bot.user.id:
            user = ctx.message.author
        sql = "SELECT money FROM users WHERE id = $1"
        temp = await self.bot.db.fetchval(sql, user.id)
        money = int(temp) + 100
        next_sql = "UPDATE users SET money = $1 WHERE id = $2"
        await self.bot.db.execute(next_sql, str(money), user.id)
        if user.id != ctx.message.author.id:
            await ctx.send("You just gave your ${} to {}".format(money, user.name))
        else:
            await ctx.send("You just got 100 chickens.")

    @commands.command()
    @commands.cooldown(1, 300, BucketType.user)
    @commands.guild_only()
    async def raid(self, ctx):
        if not self.bot.usedatabase:
            await ctx.send("This command requires a running database to work.")
            return
        sql = "SELECT money FROM users WHERE id = $1"
        tmp = await self.bot.db.fetchval(sql, ctx.message.author.id)
        success = random.randint(1, 10)
        if success > 4:
            award = random.randint(5, 25)
            money = int(tmp) + award
            next_sql = "UPDATE users SET money = $1 WHERE id = $2"
            await self.bot.db.execute(next_sql, str(money), ctx.message.author.id)
            await ctx.send("You successfully raided a farm and got {} chickens.".format(award))
        else:
            await ctx.send("You were attacked by farmers during a raid. :frowning:")

    @commands.command()
    @commands.cooldown(1, 300, BucketType.user)
    @commands.guild_only()
    async def mine(self, ctx):
        if not self.bot.usedatabase:
            await ctx.send("This command requires a running database to work.")
            return
        sql = "SELECT money FROM users WHERE id = $1"
        tmp = await self.bot.db.fetchval(sql, ctx.message.author.id)
        success = random.randint(1,10)
        if success > 6:
            award = random.randint(20, 60)
            money = int(tmp) + award
            next_sql = "UPDATE users SET money = $1 WHERE id = $2"
            await self.bot.db.execute(next_sql, str(money), ctx.message.author.id)
            await ctx.send("You mined some minerals and traded them for {} chickens.".format(award))
        else:
            await ctx.send("You couldn't find anything valuable while mining. :frowning:")

    @commands.command()
    @commands.cooldown(1, 300, BucketType.user)
    @commands.guild_only()
    async def fish(self, ctx):
        if not self.bot.usedatabase:
            await ctx.send("This command requires a running database to work.")
            return
        sql = "SELECT money FROM users WHERE id = $1"
        tmp = await self.bot.db.fetchval(sql, ctx.message.author.id)
        success = random.randint(1,10)
        if success > 6:
            award = random.randint(20, 60)
            money = int(tmp) + award
            next_sql = "UPDATE users SET money = $1 WHERE id = $2"
            await self.bot.db.execute(next_sql, str(money), ctx.message.author.id)
            await ctx.send("You caught some fish and sold them for {} chickens.".format(award))
        else:
            await ctx.send("You couldn't find anything while fishing. :frowning:")


def setup(bot):
    bot.add_cog(Economy(bot))