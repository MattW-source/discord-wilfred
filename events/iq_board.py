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

    @commands.Cog.listener()
    async def on_ready(self):
        self.iq_channel = self.client.get_channel(748908518840598559)  # TODO: Create channel and change ID

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if str(reaction) == self.iq_emoji:
            if reaction.count >= self.iq_requirement:
                message = reaction.message
                # Making sure people can't IQ Board IQ Boards
                if message.channel == self.iq_channel:
                    return
                embed = self.create_iq_embed(message, reaction)
                # Check if embed already exists in #iq-board
                iq_embed = await self.find_iq_embed(embed)
                if iq_embed is not None:
                    await iq_embed.edit(embed=embed)
                else:
                    await self.iq_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if str(reaction) == self.iq_emoji:
            message = reaction.message
            # Making sure people can't IQ Board IQ Boards
            if message.channel == self.iq_channel:
                return
            new_embed = self.create_iq_embed(message, reaction)
            old_embed = await self.find_iq_embed(new_embed)

            # If it does not exist anymore we'll send it again
            if old_embed is None and reaction.count > self.iq_requirement:
                await self.iq_channel.send(embed=new_embed)
            elif reaction.count == 0:
                await old_embed.delete()
            else:
                await old_embed.edit(embed=new_embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        reactions = [(str(r.emoji), r) for r in message.reactions]
        if self.iq_emoji in [r[0] for r in reactions]:
            embed_msg = await self.find_iq_embed(self.create_iq_embed(message, [r[1] for r in reactions if self.iq_emoji in r[0]][0]))
            await embed_msg.delete()

    # Find the already existing embed in the #iq-board channel
    # arguments: discord.Embed() we just created
    # return: None if the embed does not exist, if the embed/message exists it will return discord.Message
    async def find_iq_embed(self, embed):
        messages = [msg for msg in await self.iq_channel.history(limit=200).flatten() if msg.embeds]
        embeds = [msg.embeds for msg in messages]
        # Zipping together embeds, values of the first field (Jump) and messages
        for em, jump, message in zip(embeds[0], [em[0].fields[0].value for em in embeds], messages):
            # Making sure, in case some bot decides to send an embed with no fields in #iq-board
            if len(em.fields) >= 1:
                if embed.fields[0].value in jump:
                    return message
        return None

    # Create an IQ Embed (Generalizing creation, we don't want someone to forget something in reaction_remove when changing reaction_add)
    # arguments: message, reaction
    # return: discord.Embed()
    def create_iq_embed(self, message, reaction):
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
        embed.set_author(name="%s | #%s | %d IQ" % (message.author.name, message.channel.name, reaction.count), icon_url=message.author.avatar_url)
        return embed

def setup(client):
    client.add_cog(IQBoard(client))
