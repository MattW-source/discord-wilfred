import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *


class Crates(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(aliases=["loot", "crate"], invoke_without_command=True)
    async def crates(self, ctx):
        crates_no = sql.db_query("SELECT crates FROM Members WHERE UserID = %s" % (str(ctx.author.id)))[0][0]
        args = ctx.message.content.split(" ")
        if len(args) == 1:
            embed = discord.Embed(description="You currently have **%s** crate(s)" % (str(crates_no)),
                                  color=colour.reds)
            embed.set_author(name="Crates")
            await ctx.send(embed=embed)

    @crates.command(aliases=["use"])
    async def open(self, ctx, amount: int = 1):
        crates_no = sql.db_query("SELECT crates FROM Members WHERE UserID = %s" % (str(ctx.author.id)))[0][0]
        if crates_no == 0:
            await ctx.send("**Error:** You don't have any crates to open")
        else:
            if amount > 10:
                await ctx.send(embed=discord.Embed(title="Crates Opening Error",
                                                   description="You're trying to open too many crates, try a smaller number.",
                                                   color=colour.reds))
                return
            elif amount <= 0:
                await ctx.send(embed=discord.Embed(title="Crates Opening Error",
                                                   description="Please don't try to create a black hole and try a bigger number.",
                                                   color=colour.reds))
                return
            # If a user tries to open more crates than they have it'll default to how much they have
            if crates_no < amount:
                amount = crates_no
            # Open crates
            crates = [open_crate(ctx) for _ in range(0, amount)]
            # Take however many crates the user opened
            crates_no = crates_no - amount
            sql.execute_query("UPDATE Members SET crates = %s WHERE UserID = %s" % (str(crates_no), str(ctx.author.id)))
            embed = discord.Embed(description="Opening Crate" if amount == 1 else "Opening %d Crates" % amount)
            embed.set_author(name="Crate")
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(2)
            if amount == 1:
                print(crates)
                embed = discord.Embed(title=crates[0][0], description=crates[0][1], color=crates[0][2])
                embed.set_author(name=crates[0][3])
                await msg.edit(embed=embed)
            else:
                dupe_reward = 0
                description = "You won:\n"
                for c in crates:
                    description += " - " + c[0].strip("You Won:").replace("(Duplicate)", "**(Duplicate +%d XP)**" % c[4])
                    if "Duplicate" in c[0]:
                        dupe_reward += c[4]
                    description += "\n"

                if dupe_reward > 0:
                    description += "\n"
                    description += "You've earned **%d XP** from duplicates" % dupe_reward
                embed = discord.Embed(title="You've successfully opened %d crates!" % amount,
                                      description=description,
                                      colour=colour.primary)
                await msg.edit(embed=embed)

    @crates.command()
    async def give(self, ctx, target: discord.Member = None, amount: int = 0):
        if "Manager" in [role.name for role in ctx.message.author.roles]:
            if target is not None:
                crates_no = \
                    sql.db_query("SELECT crates FROM Members WHERE UserID = %s" % (str(target.id)))[0][0]
                crates_no = crates_no + amount
                sql.execute_query("UPDATE Members SET crates = %s WHERE UserID = %s" % (
                    str(crates_no), str(target.id)))
                await ctx.send("Successfully gave %s **%s** crate(s)" % (target.mention, str(amount)))
        else:
            await ctx.send("**Insufficient Permissions:** This command requires permission rank `MANAGER`")

def open_crate(ctx):
    # Pick rarity
    chance = random.randint(1, 100)
    if chance <= 50:
        rarity = "COMMON"
        embed_color = 0xFFFFFF
        dupe_reward = 250
    elif 50 < chance <= 75:
        rarity = "UNCOMMON"
        embed_color = 0x55FF55
        dupe_reward = 500
    elif 75 < chance <= 95:
        rarity = "RARE"
        embed_color = 0X5555FF
        dupe_reward = 750
    elif 95 < chance <= 99:
        rarity = "LEGENDARY"
        embed_color = 0xFFAA00
        dupe_reward = 1000
    elif chance == 100:
        rarity = "MYTHIC"
        embed_color = 0xFF5555
        dupe_reward = 0

    # select cosmetic
    if rarity == "MYTHIC":
        title = "You Won: " + "$25.00"
        description = "Some Money to spend on cool things."
        add_balance(ctx.author, float(25.00))
    else:
        items = sql.db_query("SELECT * from cosmetics WHERE cosmetic_rarity = '%s'" % (str(rarity)))
        item = random.choice(items)
        inventory = eval(
            sql.db_query("SELECT cosmetics FROM Members WHERE UserID = %s" % (str(ctx.author.id)))[0][0])
        if item[0] in inventory:
            title = "You Won: " + item[1] + " (Duplicate)"
            description = item[3] + "\nSince you already had this item you've been awarded %s exp" % (str(dupe_reward))
            add_exp(ctx.author.id, dupe_reward)
        else:
            title = "You Won: " + item[1]
            description = item[3]
            inventory.append(int(item[0]))
            sql.execute_query("UPDATE Members SET cosmetics = '%s' WHERE UserID = %s" % (
                str(inventory), str(ctx.author.id)))
    return title, description, embed_color, rarity, dupe_reward  # In this order to prevent confusion with indexes at the embed creation

def setup(client):
    client.add_cog(Crates(client))
