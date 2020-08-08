import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class Balance(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["bal", "money"])
    async def balance(self, ctx, target : discord.Member = None):
        if target == None:
            balance = get_profile(ctx.author.id)[0]
            target = ctx.author
        else:
            balance = get_profile(target.id)[0]
        embed = discord.Embed(description="%s currently has **$%s**!" % (target.mention, str(balance)), color=colour.primary)
        embed.set_author(name="Balance")
        await ctx.send(embed=embed)

    @balance.error
    async def on_balance_error(self, ctx, error):
        await ctx.send("Something went wrong, did you provide a valid user?")

def setup(client):
    client.add_cog(Balance(client))
