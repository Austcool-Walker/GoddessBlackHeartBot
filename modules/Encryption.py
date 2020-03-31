import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import base64
import binascii
import hashlib


class Encryption(commands.Cog, name="Encryption"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def encode(self, ctx, target, *, message: str):
        if "base64".lower() in target:
            crypto = str(base64.b64encode(bytes(message, 'utf-8')))
            crypto = crypto[2:-1]
        elif "binary".lower() in target:
            crypto = ' '.join(format(ord(x), 'b') for x in message)
        else:
            await ctx.send('That is not a valid target.')
            return
        embed = discord.Embed(title="Encryption complete.", color=discord.Colour.dark_blue(),
                              description="Here's your new message in {}".format(target))
        embed.add_field(name="Before: ", value="{}".format(message), inline=False)
        embed.add_field(name="After: ", value="{}".format(crypto), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def hash(self, ctx, target, *, message: str):
        if "md5".lower() in target:
            hash = hashlib.md5(message.encode('utf-8')).hexdigest()
        elif "sha1".lower() in target:
            hash = hashlib.sha1(message.encode('utf-8')).hexdigest()
        elif "sha224".lower() in target:
            hash = hashlib.sha224(message.encode('utf-8')).hexdigest()
        elif "sha256".lower() in target:
            hash = hashlib.sha256(message.encode('utf-8')).hexdigest()
        elif "sha384".lower() in target:
            hash = hashlib.sha384(message.encode('utf-8')).hexdigest()
        elif "sha512".lower() in target:
            hash = hashlib.sha512(message.encode('utf-8')).hexdigest()
        else:
            await ctx.send('That is not a valid target.')
            return
        embed = discord.Embed(title="Hash complete.", color=discord.Colour.dark_blue(),
                              description="Here's your new message in {}".format(target))
        embed.add_field(name="Before: ", value="{}".format(message), inline=False)
        embed.add_field(name="After: ", value="{}".format(hash), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def decode(self, ctx, target, *, message: str):
        if "base64".lower() in target:
            decoded = str(base64.b64decode(bytes(message, 'utf-8')))
            decoded = decoded[2:-1]
        elif "binary".lower() in target:
            """This currently does not work."""
            # decoded = ''.join(chr(int(message[i*8:i*8+8],2)) for i in range(len(message)//8))
            #decoded = binascii.b2a_qp(message)
            #await ctx.send(decoded)
            await ctx.send("Binary decryption is currently not ready.")
            return
        else:
            await ctx.send('That is not a valid target.')
            return
        embed = discord.Embed(title="Decryption complete.", color=discord.Colour.dark_red(),
                              description="Here's your new message from {}".format(target))
        embed.add_field(name="Before: ", value="{}".format(message), inline=False)
        embed.add_field(name="After: ", value="{}".format(decoded), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def encipher(self, ctx, target, *, message: str):
        if "caesar".lower() in target:
            L2I = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", range(26)))
            I2L = dict(zip(range(26), "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
            key = 3
            ciphertext = ""
            for c in message.upper():
                if c.isalpha():
                    ciphertext += I2L[(L2I[c] + key) % 26]
                else:
                    ciphertext += c
            await ctx.send(ciphertext)
        else:
            await ctx.send('That\'s not a valid cipher option.')

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def decipher(self, ctx, target, *, message: str):
        if "caesar".lower() in target:
            L2I = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", range(26)))
            I2L = dict(zip(range(26), "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
            key = 3
            plaintext = ""
            for c in message.upper():
                if c.isalpha():
                    plaintext += I2L[(L2I[c] - key) % 26]
                else:
                    plaintext += c
            await ctx.send(plaintext)
        else:
            await ctx.send('That\'s not a valid cipher option.')

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def reverse(self, ctx, *, message: str):
        new_msg = message[::-1]
        await ctx.send(new_msg)

def setup(bot):
    bot.add_cog(Encryption(bot))
