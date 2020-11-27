import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class SetMessage(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def setmessage(self, ctx, message_name, message_title, *, message_contents):
        '''
        Set Message Contents for rules-and-info channel

        Required Permission: @Manager
        Required Arguments: messageName, messageTitle, messageContents
        '''
        if "Manager" in [role.name for role in ctx.message.author.roles]:
            if message_name.lower() in ["rules", "rules2", "comps", "lvl_rewards", "badges", "server_invite", "misc"]: # Limit what values will be accepted
                message_id      = eval("value." + message_name.lower())
                message_channel = self.client.get_channel(781258948783112264)
                message_obj     = await message_channel.fetch_message(message_id)
                message_embed   = discord.Embed(description=message_contents, color=colour.primary)
                message_embed.set_author(name=message_title)
                await message_obj.edit(content=None, embed=message_embed)
                await ctx.send("Successfully edited message!")
            else:
                await ctx.send("Invalid Message Name")
        else:
            await ctx.send("You have insufficient privilidges to do this")

def setup(client):
    client.add_cog(SetMessage(client))
