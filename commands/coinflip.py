import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class Coinflip(commands.Cog):

    def __init__(self, client):
        self.client = client

    '''
      CoinFlip Command

      Usage: !coinflip [@user] [amount] [heads|tails]
      Permissions: None
    '''
    @commands.command(aliases=["cf"])
    async def coinflip(self, ctx, target : discord.Member = None, amount = None, side = "heads"):

        async def flip_coin():
           coinflip_string = "Flipping Coin."
           embed = discord.Embed(description=coinflip_string, color=colour.primary)
           embed.set_author(name="Coinflip")
           coinflip_msg = await ctx.send(embed=embed)
           await asyncio.sleep(0.5)
           for i in range(1,3):
               coinflip_string += "."
               embed.description=coinflip_string
               await coinflip_msg.edit(embed=embed)
               await asyncio.sleep(0.5)
           embed.description = "The coin landed on **" + coin_side + "**!"
           await coinflip_msg.edit(embed=embed)

        if target == None:
           # normal coinflip
           coin_side = random.choice(["heads", "tails"])
           await flip_coin()

        elif amount == None or not side.lower() in ["heads", "tails"]:
            await ctx.send("**Invalid Usage**: !coinflip [@user] [amount] [heads|tails]")
        else:
            # fight to the death coinflip
            if float(amount) < 0.10:
                await ctx.send("**You must bet at least $0.10!**")
            else:
                user_bal = fetch_balance(ctx.author)
                target_bal = fetch_balance(target)
                if user_bal < float(amount):
                    await ctx.send("**You do not have enough money for this, try a lower amount.**")
                elif target_bal < float(amount):
                    await ctx.send("**The target does not have enough money for this, try a lower amount.**")
                else:
                    add_balance(ctx.author, -float(amount))
                    await ctx.send("%s type !accept to accept a coinflip with %s (%s) for $%s" % (target.mention, ctx.author.mention, side, str(amount)))

                    def check(msg):
                        return msg.author == target and msg.content.upper() == "!ACCEPT"
                    try:
                        await self.client.wait_for('message', check=check, timeout=30)
                    except asyncio.TimeoutError:
                        await ctx.send("Target did not respond in time")
                        add_balance(ctx.author, float(amount))
                    else:
                        add_balance(target, -float(amount))
                        coin_side = random.choice(["heads", "tails"])
                        await flip_coin()
                        if coin_side == side.lower():
                            # user wins
                            add_balance(ctx.author, float(amount)*2)
                            await ctx.send(ctx.author.mention + " Has Won $" + amount)
                        else:
                            # target wins
                            add_balance(target, float(amount)*2)
                            await ctx.send(target.mention + " Has Won $" + amount)

def setup(client):
    client.add_cog(Coinflip(client))
