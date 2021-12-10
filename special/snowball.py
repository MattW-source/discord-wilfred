import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class Snowball(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def snowball(self, ctx, target : discord.Member):
        '''
        Throw a snowball at someone

        Required Permission: None
        Required Arguments: Mention

        '''
        bal = fetch_balance(ctx.author)
        args = ctx.message.content.split(' ')
        if bal >= 0.01:
            add_balance(ctx.author, -0.01)
            snowball = random.choice(["just threw a snowball at you!", "just threw a massive snowball at you!", "just threw a gigantic snowball at you!", "just threw a snowman at you!"])
            embed = discord.Embed(description="Hey %s, %s %s" % (args[1], ctx.message.author.mention, snowball), color=colour.secondary)
            embed.set_author(name="Cookie")
            embed.set_thumbnail(url="https://gamepedia.cursecdn.com/7daystodie_gamepedia/0/04/Snowball.png")
            await ctx.message.channel.send(embed=embed)
        else:
            await ctx.send("%s you do not have sufficient funds for this!" % (ctx.message.author.mention))

def setup(client):
    client.add_cog(Snowball(client))
