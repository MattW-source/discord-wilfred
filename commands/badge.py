import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *


class Badge(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def badge(self, ctx, operation, badge, user : discord.Member):
        message = ctx.message
        if "Manager" in [role.name for role in message.author.roles]:
            if operation.upper() == "ADD":
                current_badges = get_profile(str(user.id))[3]
                new_badges = current_badges + badge +" _ _"
                sql.execute_query("UPDATE Members SET Badges = '%s' WHERE UserID = %s" % (new_badges.replace("'", "''"), str(user.id)))
                await message.channel.send(":ok_hand: Successfully added %s to **%s**'s profile!" % (badge, user.name))

            if operation.upper() == "REMOVE":
                badge = badge + " _ _"
                current_badges = get_profile(str(user.id))[3]
                new_badges = current_badges.replace(badge, '')
                sql.execute_query("UPDATE Members SET Badges = '%s' WHERE UserID = %s" % (new_badges.replace("'", "''"), str(user.id)))
                await message.channel.send(":ok_hand: Successfully removed %s from **%s**'s profile!" % (badge, user.name))
        else:
            await ctx.send("**Insufficient Permissions:** This command requires permission rank `MANAGER`")

def setup(client):
    client.add_cog(Badge(client))
