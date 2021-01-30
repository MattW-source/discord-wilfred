import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class Cookie(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def cookie(self, ctx, target : discord.Member):
        '''
        Give someone a cookie

        Required Permission: None
        Required Arguments: Mention

        '''
        bal = fetch_balance(ctx.author)
        args = ctx.message.content.split(' ')
        if bal >= 0.01: # Check user has required amount to give a cookie
            add_balance(ctx.author, -0.01) # Take away the cost of the cookie from the user
            cookie_type = random.choice(["just gave you a chocolate chip cookie!", "just gave you a otis spunkmeyer cookie!", "just gave you a super sized cookie!", "just gave you a sainsburys taste the difference cookie!"]) # Pick a random cookie
            embed = discord.Embed(description="Hey %s, %s %s" % (args[1], ctx.message.author.mention, cookie_type), color=colour.secondary) # Format Output and put it in an embed
            embed.set_author(name="Cookie") # Set the embed author/title
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Oxygen480-apps-preferences-web-browser-cookies.svg/1024px-Oxygen480-apps-preferences-web-browser-cookies.svg.png") # Add an image of a cookie
            await ctx.send(embed=embed) # Send Message
            if not target.id == ctx.author.id: # Check the person giving the cookie wasn't giving it to themselves
                cookies_no = sql.db_query("SELECT cookiesReceived FROM Members WHERE UserID = %s" % (str(target.id)))[0][0] # get the current cookie stats of the target
                cookies_no = cookies_no + 1 # Increase it by one
                sql.execute_query("UPDATE Members SET cookiesReceived = %s WHERE UserID = %s" % (str(cookies_no), str(target.id))) # Update their cookie stats
        else: # User does not have required amount
            await ctx.send("%s you do not have sufficient funds for this!" % (ctx.message.author.mention)) # Tell the invoker they're broke.

def setup(client):
    client.add_cog(Cookie(client)) # Add cog/command
