import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *
import requests

class Kitten(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kitten(self, ctx):
        imgUrl = requests.get('https://api.thecatapi.com/v1/images/search').json()[0]['url']
        em = discord.Embed(title="Kitten", image=imgUrl, colour=colour.secondary)
        em.set_image(url=imgUrl)
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Kitten(client))
