import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class Ransack(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ransack(self, ctx):
        em = discord.Embed(description="Oak's words echoed... There's a time and place for everything, but not now.", colour=colour.reds)
        em.set_author(name="Ransack")
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Ransack(client))
