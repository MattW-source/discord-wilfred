import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *


@commands.command()
async def poll(ctx):
    if "Supporter" in [role.name for role in ctx.author.roles] or "Moderator" in [role.name for role in ctx.author.roles] or "Manager" in [role.name for role in ctx.author.roles]:
        if not ctx.bot.polls:
            args = ctx.message.content.split(" ")
            time = args[1]
            time_seconds = int(args[1])*60
            options = " ".join(args[2:]).split("|")[1:]
            question = " ".join(args[2:]).split("|")[0]
            i = 1
            options_string = ""
            for option in options:
                options_string += "**%s)** %s\n" % (str(i), str(option))
                i += 1
            votes_init = []
            for count in range(1, i):
                votes_init.append(0)
            embed=discord.Embed(description="%s \n\n %s\nVote using **!vote <option>**\n\nPoll Closes In **%s Minutes** " % (question, options_string, time), colour=colour.primary)
            embed.set_author(name="Poll")
            await ctx.send(embed=embed)
            ctx.bot.polls = True
            ctx.bot.polls_options = options
            ctx.bot.polls_votes = votes_init
            await asyncio.sleep(time_seconds)
            results_string = ""
            i = 1
            for option in options:
                results_string += "**%s)** %s - **%s Votes**\n" % (str(i), option, str(ctx.bot.polls_votes[i-1]))
                i = i+1
            embed=discord.Embed(description="Results are as follows:\n\n%s\n%s" % (question, results_string), colour=colour.primary)
            embed.set_author(name="Poll Results")
            await ctx.send(embed=embed)
            ctx.bot.polls_votes.clear()
            ctx.bot.polls_options.clear()
            ctx.bot.polls_enteries.clear()
            ctx.bot.polls = False
        else:
            embed=discord.Embed(description="A Poll is already in progress. Please wait until the current poll has ended.", colour=colour.reds)
            embed.set_author(name="Error")
            await ctx.send(embed=embed)
    else:
        await ctx.send("**Insufficient Permissions:** This command requires permission rank `SUPPORTER`")

def setup(client):
    client.add_command(poll)
