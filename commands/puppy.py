import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *
import requests

class Puppy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def puppy(self, ctx):
        imgUrl = requests.get('https://dog.ceo/api/breeds/image/random').json()['message']
        em = discord.Embed(title="Puppy", image=imgUrl, colour=colour.secondary)
        em.set_image(url=imgUrl)
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Puppy(client))
    
