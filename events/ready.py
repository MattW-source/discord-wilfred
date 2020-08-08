import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
import time
from utils.helpers import *

up = time.time()

class On_Ready(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Bot is online and connected to Discord.")
        activity=discord.Game(name=str(value.buildVersion))
        await self.client.change_presence(status=discord.Status.online, activity=activity)
        guild = self.client.get_guild(547120498509611078)
        channel = self.client.get_channel(547122972125822997)

def setup(client):
    client.add_cog(On_Ready(client))
