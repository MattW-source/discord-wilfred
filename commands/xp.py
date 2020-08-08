import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class Xp(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def xp(self, ctx, targetMember : discord.Member = None):
        if "Manager" in [role.name for role in ctx.message.author.roles]:
            args = ctx.message.content.split(" ")
            member = targetMember
            if args[2].upper() == "GIVE":
                amount = args[3]
                if int(amount) < 0:
                    await discord_error("Cannot give negative XP!", ctx)
                else:
                    add_exp(member.id, int(amount))
                    em = discord.Embed(description=":ok_hand: Successfully given **%s** **%s EXP**!" % (member.name, amount), color=colour.primary)
                    em.set_author(name="Success")
                    await ctx.send(embed=em)

        else:
            await discord_error("This command requires permission rank `MANAGER`", ctx)

def setup(client):
    client.add_cog(Xp(client))
