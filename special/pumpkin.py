import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
import utils.sinusbot as sinusbot
from utils.helpers import *
import random

class Pumpkin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def spawnpumpkin(self, ctx, channelID, *, string_to_type = None):
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

def setup(client):
    client.add_cog(Pumpkin(client))
