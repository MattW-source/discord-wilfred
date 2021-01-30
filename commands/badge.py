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
        if "Manager" in [role.name for role in ctx.message.author.roles]:
            if operation.upper() == "ADD":
                current_badges = get_profile(str(user.id))[3] # Get Current Badges From Profile
                new_badges = current_badges + badge +" _ _" # Format Badges String and append new badge
                sql.execute_query("UPDATE Members SET Badges = '%s' WHERE UserID = %s" % (new_badges.replace("'", "''"), str(user.id))) # Store it
                await ctx.send(":ok_hand: Successfully added %s to **%s**'s profile!" % (badge, user.name)) # Tell the user the operation is complete

            if operation.upper() == "REMOVE":
                badge = badge + " _ _" # Format Badge String
                current_badges = get_profile(str(user.id))[3] # Get Current Badges From Profile
                new_badges = current_badges.replace(badge, '') # Format badges string with selected badge removed
                sql.execute_query("UPDATE Members SET Badges = '%s' WHERE UserID = %s" % (new_badges.replace("'", "''"), str(user.id))) # Store it
                await ctx.send(":ok_hand: Successfully removed %s from **%s**'s profile!" % (badge, user.name)) # Tell the user the operation is complete
        else:
            await ctx.send("**Insufficient Permissions:** This command requires permission rank `MANAGER`") # Insufficient Permissions

def setup(client):
    client.add_cog(Badge(client)) # Add cog/command
