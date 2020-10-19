import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class On_Ready(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await asyncio.sleep(2)
        if member in member.guild.members:
            insert_db_user(member)
            channel = self.client.get_channel(547122996717027328)
            em = discord.Embed(title="Welcome", description="Welcome %s to **Varsity 4.0**! Make sure to read <#612764973478969354> so you stay out of trouble!" % (member.name), colour=colour.primary)
            em.set_footer(text="We now have %s Members!" % (str(len(member.guild.members))))
            await channel.send(embed=em)

def setup(client):
    client.add_cog(On_Ready(client))
