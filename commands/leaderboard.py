import discord
from discord.ext import commands
import asyncio
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
import math
from utils.helpers import *

class Leaderboard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["lb", "lboard", "topusers", "top"])
    async def leaderboard(self, ctx):
        await leaderboard_main(ctx, self=self)

def generate_leaderboard_string(guild, page=1):
    leaderboard_2d_array = sql.db_query("SELECT UserID, Level, expTotal FROM Members WHERE NOT UserID = 1 ORDER BY expTotal DESC")
    leaderboard_2d_array_processed = []
    server_total = 0
    for entry in leaderboard_2d_array:
        entry_member_object = discord.utils.get(guild.members, id=entry[0])
        if not entry_member_object is None:
            if not entry_member_object.bot:
                leaderboard_2d_array_processed.append(entry)
                server_total += entry[2]

    start_index = 0 + ((page-1)*10)
    leaderboard_string = "Server Total: **" + str(server_total) + " EXP**\n\n"
    for i in range(start_index,start_index+10):
        try:
            leaderboard_string += "**" + str(i+1) + ")** <@" + str(leaderboard_2d_array_processed[i][0]) + "> - **Lvl " + str(leaderboard_2d_array_processed[i][1]) + "** (" + str(leaderboard_2d_array_processed[i][2]) + " exp)\n"
        except IndexError:
            break
    return leaderboard_string

async def leaderboard_main(ctx, page=1, leaderboard_message_object=None, self=None):
    max_pages = math.ceil((len(ctx.guild.members)-2)/10)
    leaderboard_string = generate_leaderboard_string(ctx.guild, page)
    embed = discord.Embed(description=leaderboard_string, color=colour.primary)
    embed.set_author(name="Leaderboard (Page %s)" % (str(page)))
    embed.set_thumbnail(url="https://i.foggyio.uk/varsity_discord.png")
    if leaderboard_message_object is None:
        leaderboard_message_object = await ctx.send(embed=embed)
        await leaderboard_message_object.add_reaction("◀")
        await leaderboard_message_object.add_reaction("▶")
    else:
        await leaderboard_message_object.edit(embed=embed)

    def check(reaction, user):
        return user == ctx.author and (str(reaction.emoji) == "◀" or str(reaction.emoji) == "▶")

    try:
        reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await leaderboard_message_object.clear_reactions()
    else:
        await reaction.remove(user)
        if str(reaction.emoji) == "◀":
            if not page == 1:
                await leaderboard_main(ctx, page-1, leaderboard_message_object, self=self)
            else:
                await leaderboard_main(ctx, page, leaderboard_message_object, self=self)

        elif str(reaction.emoji) == "▶":
            if not page+1 > max_pages:
                await leaderboard_main(ctx, page+1, leaderboard_message_object, self=self)
            else:
                await leaderboard_main(ctx, page, leaderboard_message_object, self=self)

def setup(client):
    client.add_cog(Leaderboard(client))
