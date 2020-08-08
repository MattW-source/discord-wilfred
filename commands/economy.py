import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["eco"])
    async def economy(self, ctx, targetMember : discord.Member = None):
        if "Manager" in [role.name for role in ctx.author.roles]:
            args = ctx.message.content.split()
            try:
                action = args[2] #give, take, set
                value = args[3]
            except IndexError:
                await ctx.send("Incorrect Usage, !economy <user> <give|take|set> <amount>")
            if action.upper() == "GIVE":
                add_balance(targetMember, float(value))
                await ctx.send("Success! Added %s to **%s**'s balance" % (value, targetMember.name))
            elif action.upper() == "TAKE":
                add_balance(targetMember, -float(value))
                await ctx.send("Success! Removed %s from **%s**'s balance" % (value, targetMember.name))
            elif action.upper() == "SET":
                set_balance(targetMember, float(value))
                await ctx.send("Success! Set **%s**'s balance to %s" % (targetMember.name, value))
        else:
            await ctx.send("**Insufficient Permissions:** This command requires permission rank `MANAGER`")


def setup(client):
    client.add_cog(Economy(client))
