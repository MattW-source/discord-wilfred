import discord
from discord.ext import commands
import asyncio
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
import math
from utils.helpers import *

class Baltop(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["balancetop", "bt", "btop"])
    async def baltop(self, ctx):
        await leaderboard_main(ctx, self=self)

def generate_leaderboard_string(guild, page=1):
    leaderboard_2d_array = sql.db_query("SELECT UserID, Balance FROM Members WHERE NOT UserID = 1 ORDER BY Balance DESC") # Get current balance of all users ordered by their balance
    leaderboard_2d_array_processed = [] # Initalise new list
    server_total = 0 # Initalise to track the total balance of everyone in the server.
    for entry in leaderboard_2d_array: # Iterate through entry
        entry_member_object = discord.utils.get(guild.members, id=entry[0]) # Get member object
        if not entry_member_object is None: # Does member still exist in the server?
            if not entry_member_object.bot: # It's not a robot is it?
                leaderboard_2d_array_processed.append(entry) # Append the balance entry
                server_total += entry[1] # Increase the server total

    start_index = 0 + ((page-1)*10) # Calculate which point we should look at based on the current page
    leaderboard_string = "Server Total: **$" + str(round(server_total,2)) + "**\n\n" # Generate Leaderboard String + Server Total Header
    for i in range(start_index,start_index+10): # Now we need to append all the relevant enteries to the page
        try:
            leaderboard_string += "**" + str(i+1) + ")** <@" + str(leaderboard_2d_array_processed[i][0]) + "> - **$" + str(leaderboard_2d_array_processed[i][1]) + "**\n"
        except IndexError: # Page doesn't have 10 enteries
            break # We've ran out of enteries so finish here.
    return leaderboard_string # Return the string we just made

async def leaderboard_main(ctx, page=1, leaderboard_message_object=None, self=None):
    max_pages = math.ceil((len(ctx.guild.members)-2)/10) # How many pages are possible?
    leaderboard_string = generate_leaderboard_string(ctx.guild, page) # Generate our leaderboard
    embed = discord.Embed(description=leaderboard_string, color=colour.primary) # Make an embed containing the leaderboard page
    embed.set_author(name="Baltop (Page %s)" % (str(page))) # Set our embed author (well, title)
    embed.set_thumbnail(url="https://i.foggyio.uk/varsity_discord.png") # add Varsity Discord thumbnail to embed
    if leaderboard_message_object is None: # If we don't already have a message then we want to send one
        leaderboard_message_object = await ctx.send(embed=embed)
        await leaderboard_message_object.add_reaction("◀") # Reaction button for page changes
        await leaderboard_message_object.add_reaction("▶") # Reaction button for page changes
    else: # Otherwise edit the existing one
        await leaderboard_message_object.edit(embed=embed) # Edit the existing embed

    def check(reaction, user): # Check reaction is one we care about
        return user == ctx.author and (str(reaction.emoji) == "◀" or str(reaction.emoji) == "▶")

    try:
        reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=check) # Wait for reaction event
    except asyncio.TimeoutError: # Didn't happen
        await leaderboard_message_object.clear_reactions() # Remove buttons as no longer relevant
    else: # Valid reaction was given
        await reaction.remove(user)
        if str(reaction.emoji) == "◀": # We need to go back a page
            if not page == 1: # Can we go back a page?
                await leaderboard_main(ctx, page-1, leaderboard_message_object, self=self) # Recursivly go back to this method and do it again with page number changed.
            else: # We can't go back a page, stay where we are.
                await leaderboard_main(ctx, page, leaderboard_message_object, self=self) # Recursivly go back to this method and do it again

        elif str(reaction.emoji) == "▶": # We need to go forward a page
            if not page+1 > max_pages: # Can we go forward a page?
                await leaderboard_main(ctx, page+1, leaderboard_message_object, self=self) # Recursivly go back to this method and do it again with page number changed.
            else: # We've reach the last page already so say where we are. 
                await leaderboard_main(ctx, page, leaderboard_message_object, self=self) # Recursivly go back to this method and do it again

def setup(client):
    client.add_cog(Baltop(client)) # Add cog/command
