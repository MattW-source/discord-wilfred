import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *
import requests


@commands.command()
async def kitten(ctx):
    imgUrl = requests.get('https://api.thecatapi.com/v1/images/search').json()[0]['url']
    em = discord.Embed(title="Kitten", image=imgUrl, colour=colour.secondary)
    em.set_image(url=imgUrl)
    await ctx.send(embed=em)

def setup(client):
    client.add_command(kitten)
