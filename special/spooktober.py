import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
import utils.sinusbot as sinusbot
from utils.helpers import *
import random

class Spooktober(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def spawnpumpkin(self, ctx, channelID, *, string_to_type = None):
        if "Manager" in [role.name for role in ctx.author.roles]:
            channel = discord.utils.get(ctx.guild.channels, mention=channelID)
            string_to_type_scrambled = ''.join(random.shuffle(list(string_to_type)))
            embed = discord.Embed(title="Wild Pumpkin", description = "First Person To Unscramble `" + string_to_type_scrambled + "` wins $0.25!", colour=colour.secondary)
            await channel.send(embed=embed)
            def check(m):
                return m.channel == channel and m.content == string_to_type
            try:
                msg = await self.client.wait_for('message', check=check, timeout=30.0)
            except asyncio.TimeoutError:
                embed = discord.Embed(title="Wild Pumpkin", description="Nobody got the word in time. The word was `" + string_to_type + "`.", color=colour.reds)
                await channel.send(embed=embed)
            else:
                add_balance(msg.author, 0.25)
                embed = discord.Embed(title="Wild Pumpkin", description = "Congratulations " + msg.author.mention + "! you've won $0.25!", colour=colour.secondary)
                await channel.send(embed=embed)

    @commands.command()
    async def checkteams(self, ctx):
        if ctx.author.id == 345514405775147023:
            red_team_score = sql.db_query("SELECT teamPoints FROM teams WHERE teamName = 'RED'")[0][0]
            blue_team_score = sql.db_query("SELECT teamPoints FROM teams WHERE teamName = 'BLUE'")[0][0]
            embed = discord.Embed(description="**Red Team:** %s\n**Blue Team:** %s" % (str(red_team_score), str(blue_team_score)), color=colour.secondary)
            embed.set_author(name="Halloween Event Scores")
            await ctx.send(embed=embed)

    @commands.command(alias=["removeuselesspeople"])
    async def removeinactives(self, ctx):
        if ctx.author.id == 345514405775147023:
            activity = sql.db_query("SELECT UserID FROM Members WHERE NOT UserID = 472063067014823938 AND NOT UserID = 1 AND NOT UserID = 568905827952361490 AND weeklyAcivity < 10")
            red_team_role = discord.utils.get(guild.roles, name="Red Team")
            blue_team_role = discord.utils.get(guild.roles, name="Blue Team")
            for entry in activity:
                member = discord.utils.get(ctx.guild.members, id=entry[0])
                if "Red Team" in [role.name for role in member.roles]:
                    await member.remove_roles(red_team_role)
                if "Blue Team" in [role.name for role in member.roles]:
                    await member.remove_roles(blue_team_role)
            await ctx.send("Removed Inactive People From Teams")

    @commands.command()
    async def resetteampoints(self, ctx):
        if ctx.author.id == 345514405775147023:
            sql.execute_query("UPDATE teams SET teamPoints = 0")
            await ctx.send("Team Points Reset")
            
    @commands.command()
    async def disbandred(self, ctx):
        if ctx.author.id == 345514405775147023:
            red_team_role = discord.utils.get(guild.roles, name="Red Team")
            for member in ctx.guild.members:
                if "Red Team" in [role.name for role in member.roles]:
                    await member.remove_roles(red_team_role)
            await ctx.send("Done")

    @commands.command()
    async def disbandblue(self, ctx):
        if ctx.author.id == 345514405775147023:
            blue_team_role = discord.utils.get(guild.roles, name="Blue Team")
            for member in ctx.guild.members:
                if "Blue Team" in [role.name for role in member.roles]:
                    await member.remove_roles(blue_team_role)
            await ctx.send("Done")

    @commands.command()
    async def splitred(self, ctx):
        if ctx.author.id == 345514405775147023:
            red_team_role = discord.utils.get(guild.roles, name="Red Team")
            blue_team_role = discord.utils.get(guild.roles, name="Blue Team")
            redmembers = []
            for member in ctx.guild.members:
                if "Red Team" in [role.name for role in member.roles]:
                    redmembers.append(member)
            team_members = len(redmembers)
            target_size = round(team_members/2,0)
            for i in range(0, target_size):
                await redmembers[i].remove_roles(red_team_role)
                await redmembers[i].add_roles(blue_team_role)
            await ctx.send("Done")

    @commands.command()
    async def splitblue(self, ctx):
        if ctx.author.id == 345514405775147023:
            red_team_role = discord.utils.get(guild.roles, name="Red Team")
            blue_team_role = discord.utils.get(guild.roles, name="Blue Team")
            bluemembers = []
            for member in ctx.guild.members:
                if "Blue Team" in [role.name for role in member.roles]:
                    bluemembers.append(member)
            team_members = len(bluemembers)
            target_size = round(team_members/2,0)
            for i in range(0, target_size):
                await redmembers[i].add_roles(red_team_role)
                await redmembers[i].remove_roles(blue_team_role) 
            await ctx.send("Done")

def setup(client):
    client.add_cog(Spooktober(client))
