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
        if target == None: # If this parameter is not provided, default to the person invoking the command
            target = ctx.author # Set target to command invoker
        balance = get_profile(target.id)[0] # Get balance from profile
        embed = discord.Embed(description="%s currently has **$%s**!" % (target.mention, str(balance)), color=colour.primary) # Display Balance
        embed.set_author(name="Balance") # Set embed author (to be used as title)
        await ctx.send(embed=embed) # Send the embed

    @balance.error
    async def on_balance_error(self, ctx, error):
        await ctx.send("Something went wrong, did you provide a valid user?") # Most likely error is that the user doesn't exist

def setup(client):
    client.add_cog(Balance(client)) # Add cog/command
