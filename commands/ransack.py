import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *


@commands.command()
async def ransack(ctx):
    em = discord.Embed(description="Oak's words echoed... There's a time and place for everything, but not now.", colour=colour.reds)
    em.set_author(name="Ransack")
    await ctx.send(embed=em)

def setup(client):
    client.add_command(ransack)
