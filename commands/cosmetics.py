import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class Cosmetics(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["cosmetic", "inventory"])
    async def cosmetics(self, ctx, operand = None, *, cosmetic = None):
        if operand is None:
            #get inventory
            cosmetics_all = sql.db_query("SELECT cosmetic_id FROM cosmetics")
            cosmetics_total = len(cosmetics_all)
            inventory = eval(sql.db_query("SELECT cosmetics FROM Members WHERE UserID = %s" % (str(ctx.author.id)))[0][0])
            inventory_size = len(inventory)
            if len(inventory) == 0:
                embed = discord.Embed(title="Inventory", description="You have nothing in your inventory", color=reds)
                await ctx.send(embed=embed)
            else:
                inventory_string = ""
                count = 1
                for item_id in inventory:
                    cosmetic = sql.db_query("SELECT * from cosmetics WHERE cosmetic_id = %s" % (str(item_id)))[0]
                    inventory_string += str(count) + ") **" + cosmetic[2] + "** " + cosmetic[1] +"\n"
                    count = count + 1
                embed = discord.Embed(title="Inventory", description=inventory_string, color=colour.secondary)
                embed.set_footer(text="%s/%s Cosmetics Unlocked" % (str(inventory_size), str(cosmetics_total)))
                await ctx.send(embed=embed)

        elif operand.upper() == "SHOW" or operand.upper() == "DISPLAY":
            index = int(cosmetic)
            inventory = eval(sql.db_query("SELECT cosmetics FROM Members WHERE UserID = %s" % (str(ctx.author.id)))[0][0])
            inventory_size = len(inventory)
            try:
                item_id = inventory[index-1]
            except IndexError:
                await ctx.send("**Error:** You do not own a cosmetic under that id")
                return
            item = sql.db_query("SELECT * from cosmetics WHERE cosmetic_id = %s" % (str(item_id)))[0]
            if item[2] == "COMMON":
                embed_color = 0xFFFFFF
            elif item[2] == "UNCOMMON":
                embed_color = 0x55FF55
            elif item[2] == "RARE":
                embed_color = 0X5555FF
            elif item[2] == "LEGENDARY":
                embed_color = 0xFFAA00
            elif item[2] == "SPECIAL":
                embed_color = 0xFF55FF
            elif item[2] == "FESTIVE":
                embed_color = 0x00AA00
            embed = discord.Embed(title=item[1], description=item[3], color=embed_color)
            embed.set_author(name=item[2])
            if not item[4] is None:
                embed.set_thumbnail(url=item[4])
            embed.set_footer(text="Item Owned By: " + str(ctx.author))
            await ctx.send(embed=embed)

        elif operand.upper() == "CREATE":
            if "Manager" in [role.name for role in ctx.author.roles]:
                cosmetic_args = "".join(cosmetic).split("|")
                title = cosmetic_args[0]
                rarity = cosmetic_args[1].upper()
                description = cosmetic_args[2]
                if len(cosmetic_args) >= 4:
                    image_url = cosmetic_args[3]
                else:
                    image_url = None
                if rarity == "COMMON":
                    embed_color = 0xFFFFFF
                elif rarity == "UNCOMMON":
                    embed_color = 0x55FF55
                elif rarity == "RARE":
                    embed_color = 0X5555FF
                elif rarity == "LEGENDARY":
                    embed_color = 0xFFAA00
                elif rarity == "SPECIAL":
                    embed_color = 0xFF55FF
                else:
                    await ctx.send("**Error:** Invalid Rarity")
                    return
                embed = discord.Embed(title=title, description=description, color=embed_color)
                embed.set_author(name=rarity)
                if len(cosmetic_args) >= 4:
                    embed.set_thumbnail(url=image_url)

                await ctx.send(content="Confirm Creation Of Cosmetic (y/n)", embed=embed)
                def check(m):
                    return m.channel == ctx.message.channel and m.author == ctx.message.author
                msg = await self.client.wait_for('message', check=check)
                if msg.content.upper() == "Y":
                    if image_url is None:
                        sql.execute_query("INSERT INTO cosmetics (cosmetic_name, cosmetic_rarity, cosmetic_description) VALUES ('%s', '%s', '%s')" % (title.replace("'", "''"), rarity, description.replace("'", "''")))
                    else:
                        sql.execute_query("INSERT INTO cosmetics (cosmetic_name, cosmetic_rarity, cosmetic_description, cosmetic_image_url) VALUES ('%s', '%s', '%s', '%s')" % (title.replace("'", "''"), rarity, description.replace("'", "''"), image_url.replace("'", "''")))
                    await ctx.send("Cosmetic Created")
                else:
                    await ctx.send("_Cancelled_")
            else:
                await ctx.send("**Error:** Permission Denied. This command requires permission rank `MANAGER`")
        else:
            await ctx.send("**Error:** Invalid Usage")

def setup(client):
    client.add_cog(Cosmetics(client))
