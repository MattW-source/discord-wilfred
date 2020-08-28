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
        if bal >= 0.01:
            add_balance(ctx.author, -0.01)
            cookie_type = random.choice(["just gave you a chocolate chip cookie!", "just gave you a otis spunkmeyer cookie!", "just gave you a super sized cookie!", "just gave you a sainsburys taste the difference cookie!"])
            embed = discord.Embed(description="Hey %s, %s %s" % (args[1], ctx.message.author.mention, cookie_type), color=colour.secondary)
            embed.set_author(name="Cookie")
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Oxygen480-apps-preferences-web-browser-cookies.svg/1024px-Oxygen480-apps-preferences-web-browser-cookies.svg.png")
            await ctx.message.channel.send(embed=embed)
            if not target.id == ctx.author.id:
                cookies_no = sql.db_query("SELECT cookiesReceived FROM Members WHERE UserID = %s" % (str(target.id)))[0][0]
                cookies_no = cookies_no + 1
                sql.execute_query("UPDATE Members SET cookiesReceived = %s WHERE UserID = %s" % (str(cookies_no), str(target.id)))
        else:
            await ctx.send("%s you do not have sufficient funds for this!" % (ctx.message.author.mention))

def setup(client):
    client.add_cog(Cookie(client))
