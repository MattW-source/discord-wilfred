import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class Puppy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def puppy(self, ctx):
        log.debug("%s issued server command %s" % (str(ctx.message.author), str(ctx.message.content)))
        imgUrl = random.choice(["https://media3.giphy.com/media/HKl5QYQF5aOdO/giphy.gif", "http://giphygifs.s3.amazonaws.com/media/bmrxNoGqGNMAM/giphy.gif", "https://media0.giphy.com/media/xT0xeuOy2Fcl9vDGiA/giphy.gif", "https://media3.giphy.com/media/73h3LBWraONTW/giphy.gif"])
        em = discord.Embed(title="Puppy", image=imgUrl, colour=colour.secondary)
        em.set_image(url=imgUrl)
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Puppy(client))
    
