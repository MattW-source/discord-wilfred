import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class Tag(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def tag(self, ctx):
        args = ctx.message.content.split()
        if args[1].upper() == "CREATE":
            if get_profile(ctx.author.id)[1] >= 30 or "Moderator" in [role.name for role in ctx.message.author.roles] or "Manager" in [role.name for role in ctx.message.author.roles]:
                tagContent = " ".join(args[3:]).replace("'", "''")
                print(tagContent)
                tagSubmitter = str(ctx.message.author)
                tagName = args[2]
                try:
                    sql.execute_query("INSERT INTO tags (name, content, submittedBy) VALUES ('%s', '%s', '%s')" % (tagName.replace("'", "''"), tagContent.replace("'", "''"), tagSubmitter.replace("'", "''")))
                    await ctx.send("Tag successfully created")
                except:
                    await ctx.send("A tag already exists with that name")
            else:
                await ctx.send("You are not allowed to create tags yet!")
        elif args[1].upper() == "CREATE_IMG":
            if get_profile(ctx.author.id)[1] >= 30 or "Moderator" in [role.name for role in ctx.message.author.roles] or "Manager" in [role.name for role in ctx.message.author.roles]:
                tagContent = " ".join(args[3:]).replace("'", "''")
                tagSubmitter = str(ctx.message.author)
                tagName = args[2]
                try:
                    sql.execute_query("INSERT INTO tags (name, content, submittedBy, isImage) VALUES ('%s', '%s', '%s', 1)" % (tagName.replace("'", "''"), tagContent.replace("'", "''"), tagSubmitter.replace("'", "''")))
                    await ctx.send("Tag successfully created")
                except:
                    await ctx.send("A tag already exists with that name")
            else:
                await ctx.send("You are not allowed to create tags yet!")
        elif args[1].upper() == "DELETE":
            if "Moderator" in [role.name for role in ctx.message.author.roles] or "Manager" in [role.name for role in ctx.message.author.roles]:
                tagName = args[2]
                tag = sql.db_query("SELECT name FROM tags WHERE name = '%s'" % (tagName.replace("'", "''")))
                if len(tag) == 0: # tag does not exists
                    await ctx.send("There is no tag with that name")
                else:
                    sql.execute_query("DELETE FROM tags WHERE name = '%s'" % (tagName.replace("'", "''")))
                    await ctx.send("Tag has been successfully deleted")
        else:
            tagName = args[1]
            tag = sql.db_query("SELECT name, content, submittedBy, isImage FROM tags WHERE name = '%s'" % (tagName.replace("'", "''")))
            if not len(tag) == 0:
                if tag[0][3] == 1:
                    embed = discord.Embed(title=tag[0][0], color=colour.secondary)
                    embed.set_image(url=tag[0][1])
                else:
                    embed = discord.Embed(title=tag[0][0], description=tag[0][1], color=colour.secondary)
                embed.set_footer(text="Submitted By: " + tag[0][2])
                await ctx.send(embed=embed)
            else:
                await ctx.send("That tag does not exist")

def setup(client):
    client.add_cog(Tag(client))
