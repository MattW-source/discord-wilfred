import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *


class Multiplier(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def multiplier(self, ctx):
        if "Manager" in [role.name for role in ctx.message.author.roles]:
            args = ctx.message.content.split(" ")
            multiplier = int(args[1])
            level_up(1, multiplier)
            await ctx.message.channel.send(":ok_hand: Successfully set exp multiplier to %s" % (args[1]))
        else:
            await ctx.send("**Insufficient Permissions:** This command requires permission rank `MANAGER`")


def setup(client):
    client.add_cog(Multiplier(client))
