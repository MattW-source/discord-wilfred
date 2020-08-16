import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
import utils.sinusbot as sinusbot
from utils.helpers import *

class Playing(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def playing(self, ctx):
        song = sinusbot.playing()
        if song == None:
            print("wtf")
        version = song[2]
        if song[1] == "0:00":
            duration = "Unknown"
        else:
            duration = str(song[1])
        if song == None:
            song = ["_An error occurred fetching playing status. Please try again later._", "0:00"]
        if song[3]:
            embed = discord.Embed(description=song[0], color=0x940060)
            embed.set_author(name="One World Radio | Currently Playing", icon_url="https://i.foggyio.uk/tml.png")
            embed.set_thumbnail(url="https://i.foggyio.uk/one_world_radio.png")
        else:
            embed = discord.Embed(description=song[0], color=colour.reds)
            embed.set_author(name="Currently Playing", icon_url="https://i.foggyio.uk/playing.png")
            embed.set_thumbnail(url="https://i.foggyio.uk/SinusBot.png")
        if not duration == "Unknown":
            embed.set_footer(text="Duration: " + duration + " | SinusBot " + version)
        else:
            embed.set_footer(text="SinusBot " + version)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Playing(client))
