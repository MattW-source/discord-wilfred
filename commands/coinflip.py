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
           coinflip_string = "Flipping Coin." # Initalise String
           embed = discord.Embed(description=coinflip_string, color=colour.primary) # Create Embed
           embed.set_author(name="Coinflip") # Set Author/Title
           coinflip_msg = await ctx.send(embed=embed) # Send message
           await asyncio.sleep(0.5) # Wait half a second, asyncronously. 
           for i in range(1,3): # Loop a few times
               coinflip_string += "." # Add another "." to the string for suspense.
               embed.description=coinflip_string # Update description
               await coinflip_msg.edit(embed=embed) # Edit the sent message
               await asyncio.sleep(0.5) # Wait half a second, asyncronously. 
           embed.description = "The coin landed on **" + coin_side + "**!" # Tell them what side the coin landed on
           await coinflip_msg.edit(embed=embed) # Edit the sent message

        if target == None: # normal coinflip
           coin_side = random.choice(["heads", "tails"])
           await flip_coin()

        elif amount == None or not side.lower() in ["heads", "tails"]: # invalidate usage for fight to the death coinflip
            await ctx.send("**Invalid Usage**: !coinflip [@user] [amount] [heads|tails]") # Tell the user they did it wrong
        else: # fight to the death coinflip
            if float(amount) < 0.10: # Validate they are betting more than the minimum required amount
                await ctx.send("**You must bet at least $0.10!**") # Inform user they need to bet at least 10 cent
            else: # Bet amount is high enough 
                if ctx.author == target: # We're not coinflipping ourselves are we?
                    await ctx.send("**You cannot coinflip yourself**")
                else:  
                    user_bal = fetch_balance(ctx.author) # Get balance of invoker
                    target_bal = fetch_balance(target) # Get balance of opponent 
                    if user_bal < float(amount): # Does invoker have enough?
                        await ctx.send("**You do not have enough money for this, try a lower amount.**") # Tell them to get more money
                    elif target_bal < float(amount): # Does opponent have enough?
                        await ctx.send("**The target does not have enough money for this, try a lower amount.**") # Tell the user their opponent is poor.
                    else: # Everyone has enough
                        add_balance(ctx.author, -float(amount)) # Remove balance from the invoker.
                        await ctx.send("%s type !accept to accept a coinflip with %s (%s) for $%s" % (target.mention, ctx.author.mention, side, str(amount))) # Tell the opponent to accept

                        def check(msg):
                            return msg.author == target and msg.content.upper() == "!ACCEPT" # Check the response is the one we care about
                        try:
                            await self.client.wait_for('message', check=check, timeout=30) # Wait for response from opponent 
                        except asyncio.TimeoutError: # Opponent didn't response
                            await ctx.send("Opponent did not respond in time") # Inform the user the oppenent didn't response
                            add_balance(ctx.author, float(amount)) # Refund the balance
                        else: # Opponent Responsed
                            add_balance(target, -float(amount)) # Remove bet amount from opponent 
                            coin_side = random.choice(["heads", "tails"]) # pick the side the coin falls on
                            await flip_coin() # Flip the coin in chat
                            if coin_side == side.lower(): # Is the side it landed on the one the invoker picked?
                                # user wins
                                add_balance(ctx.author, float(amount)*2) # Give the invoker their money + winnings 
                                await ctx.send(ctx.author.mention + " Has Won $" + amount) # Put to chat who won.
                            else:
                                # target wins
                                add_balance(target, float(amount)*2) # Give the opponent their money + winnings
                                await ctx.send(target.mention + " Has Won $" + amount) # Put to chat who won.

def setup(client):
    client.add_cog(Coinflip(client)) # Add cog/command
