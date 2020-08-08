import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class Kitten(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kitten(self, ctx):
        log.debug("%s issued server command %s" % (str(ctx.message.author), str(ctx.message.content)))
        imgUrl = random.choice(["https://cdn.discordapp.com/avatars/283388594608013312/ddc6f6ae51689a382eecc100103e1b79.png?size=1024", "https://media.tenor.com/images/fe9cdda998e9d121f318c2d938c9c6a2/tenor.gif", "https://media.giphy.com/media/kvrvnB158J4fm/giphy.gif", "https://media.giphy.com/media/r1OyZ5NfRJigg/giphy.gif", "https://media.giphy.com/media/4rep3f9ih9u12/giphy.gif"])
        em = discord.Embed(title="Kitten", image=imgUrl, colour=colour.secondary)
        em.set_image(url=imgUrl)
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Kitten(client))
