import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class Raffle(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def raffle(self, ctx):
        if "Moderator" in [role.name for role in ctx.author.roles] or "Manager" in [role.name for role in ctx.author.roles]:
            if not self.client.raffles:
                args = ctx.message.content.split(" ")
                item = " ".join(args[2:])
                time = int(args[1])*60
                em = discord.Embed(description="%s has started a raffle! Type `!enter` to be in with a chance to win `%s`!\n\n Raffle closes in `%s Minutes`" % (ctx.author.mention, item, str(args[1])), colour=0x00ff73)
                em.set_author(name="Raffle")
                await ctx.message.channel.send(embed=em)
                self.client.raffles = True
                await asyncio.sleep(time-30)
                em = discord.Embed(description="The raffle ends in 30 seconds! Type `!enter` to be in with a chance to win `%s`!" % (item), colour=0x00ff73)
                em.set_author(name="Raffle")
                await ctx.send(embed=em)
                await asyncio.sleep(30)
                self.client.raffles = False
                winner = random.choice(self.client.enteries)
                em = discord.Embed(description="The raffle has ended! Congratulations to `%s` for winning `%s`!" % (winner, item), colour=0x00ff73)
                em.set_author(name="Raffle Ended")
                await ctx.message.channel.send(embed=em)
                self.client.enteries.clear()
            else:
                embed=discord.Embed(description="A Raffle is already in progress. Please wait until the current raffle has ended.", colour=colour.reds)
                em.set_author(name="Error")
                await ctx.send(embed=embed)
        else:
            await ctx.send("**Insufficient Permissions:** This command requires permission rank `MODERATOR`")

def setup(client):
    client.add_cog(Raffle(client))
