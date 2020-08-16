import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class May(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def may(self, ctx):
        quote = random.choice(["The Government cannot just be consumed by Brexit. There is so much more to do", "My whole philosophy is about doing, not talking.", "I actually think I think better in high heels", "I've been clear that Brexit means Brexit", "I think we all agree that the comments Donald Trump made in relation to Muslims were divisive, unhelpful and wrong.", "There must be no attempts to remain inside the E.U., no attempts to rejoin it through the back door, and no second referendum.", "Strong and Stable leadership"])
        await ctx.send(quote)

def setup(client):
    client.add_cog(May(client))
