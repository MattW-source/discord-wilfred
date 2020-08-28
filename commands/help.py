import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        helpEm = discord.Embed(description="", color=colour.primary)
        helpEm.set_author(name="Command Help")
        helpEm.set_thumbnail(url="https://i.foggyio.uk/varsity_discord.png")
        helpEm.add_field(name="User Commands", value="**!daily**\n**!profile** [user]\n**!playing**\n**!coinflip**\n**!ransack** <user> <amount>\n**!ping**\n**!cookie** <user>\n**!hug** <user>\n**!tag** <tag name | create>\n**!streaks**\n**!leaderboard**\n**!weekly**\n**!shop** [buy] [item]\n**!kitten**\n**!puppy**\n**!cosmetics** [show] <id>\n**!crates** [open]\n**!pay** <user> <amount>", inline=False)
        helpEm.add_field(name="Supporter Commands", value="**!poll** <time> <question>|<option1>|<option2>|...", inline=False)
        if "Moderator" in [role.name for role in ctx.message.author.roles] or "Manager" in [role.name for role in ctx.message.author.roles]:
            helpEm.add_field(name="Administration Commands", value="**!unload** <module>\n**!load** <module>\n**!reload** <module>\n**!multiplier** <amount>\n**!economy** <user> <give| take | set> <amount>\n**!badge** <add | remove> <emoji> <user>\n**!xp** <user> give [amount]\n**!raffle** <time> <item>")
        await ctx.message.channel.send(embed=helpEm)

def setup(client):
    client.add_cog(Help(client))
