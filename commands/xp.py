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
                    await error("Cannot Give Negative EXP!", ctx.message.channel)
                else:
                    add_exp(member.id, int(amount))
                    await ctx.message.channel.send(":ok_hand: Successfully given **%s** **%s EXP**!" % (member.name, amount))
        else:
            await ctx.send("**Insufficient Permissions:** This command requires permission rank `MANAGER`")

def setup(client):
    client.add_cog(Xp(client))
