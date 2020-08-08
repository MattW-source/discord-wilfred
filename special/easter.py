import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
import utils.sinusbot as sinusbot
from utils.helpers import *

class Easter(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def easter(self, ctx, channelID, *, string_to_type ):
        channel = discord.utils.get(ctx.guild.channels, mention=channelID)
        embed = discord.Embed(title="Easter Egg", description = "First Person To Type `" + string_to_type + "` wins $0.50!", colour=0xFF55FF)
        await channel.send(embed=embed)
        def check(m):
            return m.channel == channel and m.content == string_to_type

        try:
            msg = await self.client.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            embed = discord.Embed(title="Easter Egg", description="Nobody typed the message in time", color=colour.reds)
            await channel.send(embed=embed)
        else:
            add_coins(msg.author, 0.50)
            embed = discord.Embed(title="Easter Egg", description = "Congratulations " + msg.author.mention + "! you've won $0.50!", colour=0xFF55FF)
            await channel.send(embed=embed)

def setup(client):
    client.add_cog(Easter(client))
