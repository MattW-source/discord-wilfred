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
        if operand is None: # No operand provided, default to showing inventory
            cosmetics_all = sql.db_query("SELECT cosmetic_id FROM cosmetics") # get inventory
            cosmetics_total = len(cosmetics_all) # How cosmetics exist?
            inventory = eval(sql.db_query("SELECT cosmetics FROM Members WHERE UserID = %s" % (str(ctx.author.id)))[0][0]) # Inventory is stored as a list, make python interpret it as such
            inventory_size = len(inventory) # How many cosmetics do they have?
            if len(inventory) == 0: # Do they have cosmetics?
                embed = discord.Embed(description="You have nothing in your inventory", color=colour.reds) # Tell them they don't have cosmetics
                embed.set_author(name="Inventory") # Set author/title
                await ctx.send(embed=embed) # Send the message
            else: # Yes they have cosmetics
                inventory_string = "" # Initalise Inventory String
                count = 1 # Initalise Count
                for item_id in inventory: # Go through cosmetics
                    cosmetic = sql.db_query("SELECT * from cosmetics WHERE cosmetic_id = %s" % (str(item_id)))[0] # Get the cosmetic details from the cosmetics table
                    inventory_string += str(count) + ") **" + cosmetic[2] + "** " + cosmetic[1] +"\n" # Append the cosmetic to the inventory string 
                    count += 1 # Increase our counter
                embed = discord.Embed(description=inventory_string, color=colour.secondary) # Create embed with inventory
                embed.set_author(name="Inventory") # Set author/title
                embed.set_footer(text="%s/%s Cosmetics Unlocked" % (str(inventory_size), str(cosmetics_total))) # Set footer with statistics
                await ctx.send(embed=embed) # Send Message

        elif operand.upper() == "SHOW" or operand.upper() == "DISPLAY": # Show a cosmetic from inventory
            index = int(cosmetic) # Convert cosmetic parameter to integer as all passed in args are strings
            inventory = eval(sql.db_query("SELECT cosmetics FROM Members WHERE UserID = %s" % (str(ctx.author.id)))[0][0]) # Get their cosmetics and interpret it as a list object
            inventory_size = len(inventory) # Get size
            try:
                item_id = inventory[index-1] # Get the cosmetic from their inventory using the provided ID minus 1 (as Python counts from 0 but we count from 1)
            except IndexError: # Doesn't exist
                await ctx.send("**Error:** You do not own a cosmetic under that id") # Tell the user it doesn't exist
            else: # it exists
                item = sql.db_query("SELECT * from cosmetics WHERE cosmetic_id = %s" % (str(item_id)))[0] # get the cosmetic details
                if item[2] == "COMMON": # Python needs case statements... anyway set the embed colour for rarity  
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
                embed = discord.Embed(title=item[1], description=item[3], color=embed_color) # Create Embed
                embed.set_author(name=item[2]) # Set author to cosmetic rarity (it shows above the title attribute)
                if not item[4] is None: # Does the cosmetic have a image attached?
                    embed.set_thumbnail(url=item[4]) # Attach the image of the cosmetic to the embed
                embed.set_footer(text="Item Owned By: " + str(ctx.author)) # Show the item owner
                await ctx.send(embed=embed) # Send embed 

        elif operand.upper() == "CREATE": # Create a new cosmetic 
            if "Manager" in [role.name for role in ctx.author.roles]: # Check they have perms 
                cosmetic_args = "".join(cosmetic).split("|") # Split the operands
                title = cosmetic_args[0] # Get title
                rarity = cosmetic_args[1].upper() # Get Rarity
                description = cosmetic_args[2] # Get description
                if len(cosmetic_args) >= 4: # Has image?
                    image_url = cosmetic_args[3] # Get image url
                else:
                    image_url = None # No image for this cosmetic
                if rarity == "COMMON": # Case statements plz? Anyway get the embed colour ready for preview of cosmetic
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
                    await ctx.send("**Error:** Invalid Rarity") # Rarity Provided was invalid
                    return
                embed = discord.Embed(title=title, description=description, color=embed_color) # Generate Preview
                embed.set_author(name=rarity)  
                if len(cosmetic_args) >= 4: # Do we need to add an image to the embed?
                    embed.set_thumbnail(url=image_url) # Add image to embed

                await ctx.send(content="Confirm Creation Of Cosmetic (y/n)", embed=embed) # Preview Cosmetic & tell invoker to confirm creation of cosmetic 
                def check(m): # Check the response is one we care about
                    return m.channel == ctx.message.channel and m.author == ctx.message.author
                msg = await self.client.wait_for('message', check=check) # Wait indefinetly for response
                if msg.content.upper() == "Y": # Create cosmetic
                    if image_url is None:
                        sql.execute_query("INSERT INTO cosmetics (cosmetic_name, cosmetic_rarity, cosmetic_description) VALUES ('%s', '%s', '%s')" % (title.replace("'", "''"), rarity, description.replace("'", "''"))) # Store cosmetic in DB
                    else:
                        sql.execute_query("INSERT INTO cosmetics (cosmetic_name, cosmetic_rarity, cosmetic_description, cosmetic_image_url) VALUES ('%s', '%s', '%s', '%s')" % (title.replace("'", "''"), rarity, description.replace("'", "''"), image_url.replace("'", "''"))) # Store cosmetic in DB
                    await ctx.send("Cosmetic Created")
                else: # Don't create
                    await ctx.send("_Cancelled_")
            else: # User doesn't have permission to run the create command
                await ctx.send("**Error:** Permission Denied. This command requires permission rank `MANAGER`") # Tell user they lack perms 
        else: # Usage is invalid
            await ctx.send("**Error:** Invalid Usage") # Tell the user they did it wrong

def setup(client):
    client.add_cog(Cosmetics(client)) # Add cog/command
