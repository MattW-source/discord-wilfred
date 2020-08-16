import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
import time
from utils.helpers import *
from events.ready import up

from pythonping import ping

class Ping(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        pongStr = "Pong!"
        pongEmbed = discord.Embed(title="Pong!", description="_Pinging..._", color=colour.secondary)
        start = time.time() * 1000
        msg = await ctx.message.channel.send(embed=pongEmbed)
        end = time.time() * 1000
        response_list = ping('gateway.discord.gg', size=56, count=5)
        gateway_ping = response_list.rtt_avg_ms
        pongEmbed = discord.Embed(title="Pong!", description="Gateway: `%sms`\nRest: `%sms`" % (str(gateway_ping), str(int(round(end-start, 0)))), color=colour.secondary)
        pongEmbed.set_footer(text="Online For: " + str(time_phaser(int(time.time()-self.client.up))))
        await msg.edit(embed=pongEmbed)

def setup(client):
    client.add_cog(Ping(client))
