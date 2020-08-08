import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class Hug(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hug(self, ctx):
        '''
        Hug Someone

        Required Permission: @Outstandingly Regular
        Required Arguments: Mention

        '''
        bal = fetch_balance(ctx.author)
        if bal >= 0.01:
            add_balance(ctx.author, -0.01)
            args = ctx.message.content.split()
            hug_type = random.choice(["just gave you a big hug!", "just gave you a big big hug!", "just gave you a tight squeeze!", "just gave you a cute hug!"])
            embed = discord.Embed(description="Hey %s, %s %s" % (args[1], ctx.message.author.mention, hug_type), color=colour.secondary)
            embed.set_author(name="Hug")
            await ctx.message.channel.send(embed=embed)
        else:
            await ctx.send("%s you do not have sufficient funds for this!" % (ctx.message.author.mention))

def setup(client):
    client.add_cog(Hug(client))
