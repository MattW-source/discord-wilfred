import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class Pay(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["transfer"])
    async def pay(self, ctx, targetMember : discord.Member = None, amount = None):
        if targetMember == None or amount == None:
            await ctx.send("Incorrect Usage, !pay <user> <amount>")
        else:
            amount = round(float(amount), 2) # Don't want people sending 0.33333... to people
            userBal = fetch_balance(ctx.author)
            targetBal = fetch_balance(targetMember)
            if float(amount) > userBal:
                await ctx.send("You have insufficient funds for this")
            elif float(amount) < 0.01:
                await ctx.send("You need to send at least 0.01.")
            else:
                try: # Begin Transaction
                    add_balance(ctx.author, -float(amount))
                    add_balance(targetMember, float(amount))
                    await ctx.send("Transaction Complete!")
                except Exception as e: # Transaction Failed, rollback everything
                    set_balance(ctx.author, userBal)
                    set_balance(targetMember, targetBal)
                    log.error("Transaction Failed | %s -> %s ($%s) | Error: %s" % (ctx.author.name, targetMember.name, str(amount), str(e)))    
                    await ctx.send("Transaction Failed. Please try again later.")

def setup(client):
    client.add_cog(Pay(client))
