import discord
from discord.ext import commands
import utils.logging as log

class Command_Event(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command(self, ctx):
        log.debug("%s issued server command %s" % (str(ctx.message.author), str(ctx.message.content)))

def setup(client):
    client.add_cog(Command_Event(client))
