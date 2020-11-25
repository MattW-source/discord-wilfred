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
    async def setmessage(self, ctx, messageName, messageTitle, *, messageContents):
        '''
        Set Message Contents for rules-and-info channel

        Required Permission: @Manager
        Required Arguments: messageName, messageTitle, messageContents
        '''
        pass


def setup(client):
    client.add_cog(SetMessage(client))
