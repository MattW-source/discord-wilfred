import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class Profile(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def weekly(self, ctx):
        args = ctx.message.content.split(" ")
        showDetails = False
        if len(args) >= 2 and ("Moderator" in [role.name for role in ctx.author.roles] or "Manager" in [role.name for role in ctx.author.roles]):
            if args[1].upper() == "DETAILS":
                activity = sql.db_query("SELECT UserID, weeklyActivity FROM Members WHERE NOT UserID = 472063067014823938 AND NOT UserID = 1 AND NOT UserID = 568905827952361490 ORDER BY weeklyActivity DESC")
                count = 1
                index = 0
                server_total = 0
                for entry in activity:
                    server_total += entry[1]
                lbString = "Server Total: **" + str(server_total) + " Points**\n\n"

                while count < 6:
                    user = discord.utils.get(ctx.guild.members, id=activity[index][0])
                    if not user == None:
                        lbString += "**" + str(count) + ")** <@" + str(activity[index][0]) + "> - **" + str(balance_formatter(activity[index][1])) +"** Points\n"
                        count += 1
                    index += 1
                embed = discord.Embed(description=lbString, color=colour.primary)
                embed.set_author(name="Weekly Activity Leaderboard")
                embed.set_thumbnail(url="https://i.foggyio.uk/varsity_discord.png")
                await ctx.send(embed=embed)
            elif args[1].upper() == "RESET":
                if "Manager" in [role.name for role in ctx.author.roles]:
                    sql.execute_query("UPDATE Members SET weeklyActivity=0")
                    await ctx.send("Reset Weekly Activity Stats")
                    return
        else:
            activity = sql.db_query("SELECT UserID, weeklyActivity FROM Members WHERE NOT UserID = 472063067014823938 AND NOT UserID = 1 AND NOT UserID = 568905827952361490 ORDER BY weeklyActivity DESC")
            count = 1
            index = 0
            server_total = 0
            for entry in activity:
                server_total += entry[1]
            lbString = "Server Total: **" + str(server_total) + " Points**\n\n"
            while count < 6:
                user = discord.utils.get(ctx.guild.members, id=activity[index][0])
                if not user == None:
                    lbString += "**" + str(count) + ")** <@" + str(activity[index][0]) + ">\n"
                    count += 1
                index += 1

            not_found = True
            i = 1
            index2 = 0
            while not_found:
                user = discord.utils.get(ctx.guild.members, id=activity[index2][0])
                if not user == None:
                    if activity[index2][0] == ctx.author.id:
                        not_found = False
                        if i >= 6:
                            lbString += "\n**" + str(i) + ")** <@" + str(activity[index2][0]) + ">\n"
                    i += 1
                index2 += 1

            embed = discord.Embed(description=lbString, color=colour.primary)
            embed.set_author(name="Weekly Activity Leaderboard")
            embed.set_thumbnail(url="https://i.foggyio.uk/varsity_discord.png")
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Profile(client))
