import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *


class IQBoard(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.iq_emoji = "<:WeSmart:682352802202386472>"
        self.iq_requirement = 7
        self.channel_cache = {}

    @commands.Cog.listener()
    async def on_ready(self):
        self.iq_channel = self.client.get_channel(748908518840598559)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.handle_reaction_event(payload)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        await self.handle_reaction_event(payload)

    # This is it's own function because both on_raw_reaction_add and on_raw_reaction_remove should do the same thing
    async def handle_reaction_event(self, payload):
        if str(payload.emoji) == self.iq_emoji:
            # Caching so we don't get_channel every time
            if payload.channel_id not in self.channel_cache:
                self.channel_cache[payload.channel_id] = self.client.get_channel(payload.channel_id)
            channel = self.channel_cache[payload.channel_id]
            message = await channel.fetch_message(payload.message_id)
            count = [reaction.count for reaction in message.reactions if str(reaction) == self.iq_emoji]
            if not count:  # If all reactions are removed
                count = 0
            else:
                count = count[0]
            # Disallow IQ'ing messages in the IQ channel
            if channel == self.iq_channel:
                return

            embed_msg = await self.find_iq_embed(message.id)
            if embed_msg is None:
                if count >= self.iq_requirement:
                    msg = await self.iq_channel.send(embed=self.create_iq_embed(message, count))
                    sql.execute_query("INSERT INTO iq_board (EmbedID, MessageID, ChannelID) VALUES (%d, %d, %d)" % (msg.id, message.id, channel.id))
            else:
                if count > 0:
                    await embed_msg.edit(embed=self.create_iq_embed(message, count))
                else:
                    await embed_msg.delete()
                    sql.execute_query("DELETE FROM iq_board WHERE EmbedID = %d" % embed_msg.id)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        embed_msg = await self.find_iq_embed(payload.message_id)
        if embed_msg is not None:
            await embed_msg.delete()
            sql.execute_query("DELETE FROM iq_board WHERE EmbedID = %d" % embed_msg.id)

    # Find the already existing embed in the #iq-board channel
    # arguments: message id
    # return: None if the embed does not exist, if the embed/message exists it will return discord.Message
    async def find_iq_embed(self, message_id):
        embed_id = sql.db_query("SELECT EmbedID FROM iq_board WHERE MessageID = %d" % message_id)
        if not embed_id:
            return None
        return await self.iq_channel.fetch_message(embed_id[0][0])

    # Create an IQ Embed (Generalizing creation, we don't want someone to forget something in reaction_remove when changing reaction_add)
    # arguments: message, reaction
    # return: discord.Embed()
    def create_iq_embed(self, message, count):
        embed = discord.Embed(description=message.content, color=colour.primary)
        # Keep this first or find_iq_embed will break
        embed.add_field(name="_ _", value="[Jump!](%s)" % message.jump_url)
        if message.attachments:
            url = message.attachments[0].url
            # If it's an image we can just display it, else give a hyperlink the the media
            if url.split(".")[-1] in ["jpg", "jpeg", "png", "gif", "bmp"]:
                embed.set_image(url=message.attachments[0].url)
                embed.add_field(name="Attachments:", value="_ _", inline=False)
            else:
                embed.add_field(name="Attachments:", value="[%s](%s)" % (url.split("/")[-1], url), inline=False)
        embed.set_author(name="%s | #%s | %d IQ" % (message.author.name, message.channel.name, count), icon_url=message.author.avatar_url)
        return embed

def setup(client):
    client.add_cog(IQBoard(client))
