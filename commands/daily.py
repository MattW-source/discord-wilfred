import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *
import time


class Daily(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def daily(self, ctx):
        current_time = time.time()
        query = sql.db_query("SELECT dailyRewardClaimed, dailyRewardStreak FROM Members WHERE UserID = %s " % (str(ctx.author.id)))
        last_advent = query[0][0]
        streak = query[0][1]
        if last_advent < current_time:
            if current_time - last_advent > ((60*60)*24):
                streak = 0
                sql.execute_query("UPDATE Members SET dailyRewardStreak = %s WHERE UserID = %s " % (str(streak), str(ctx.author.id)))

        if "Supporter" in [role.name for role in ctx.author.roles]:
            multiplier = 2
        else:
            multiplier = 1

        if last_advent < current_time:
            cookie_chance = random.randint(1,25)
            embed=discord.Embed(description="Select your reward by typing the number in chat", color=colour.primary)
            embed.set_author(name="Daily Rewards")
            embed.add_field(name="Reward 1", value=str((1000 + (streak * 10))*multiplier) + " Exp", inline=False)
            embed.add_field(name="Reward 2", value="$" + str(round(0.10 + (streak * 0.01),2)*multiplier), inline=False)
            if cookie_chance == 1:
                embed.add_field(name="Reward 3", value="3 Cookies", inline=False)

            embed.set_footer(text="Your current reward streak is: " + str(streak))
            mssg = await ctx.send(embed=embed)
            channel = ctx.channel

            def check(m):
                return m.author.id == ctx.author.id and m.channel == channel

            try:
                msg = await self.client.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                embed = discord.Embed(description="No Message Received", color=colour.reds)
                embed.set_author(name="Daily Reward")
                await mssg.edit(embed=embed)
            else:
                await msg.delete()
                if msg.content == "1":
                    add_exp(ctx.author.id, (1000 + (streak * 10))*multiplier)
                    embed = discord.Embed(description="You unlocked **" + str((1000 + (streak * 10))*multiplier) + " EXP**!", color=colour.primary)
                    embed.set_author(name="Daily Reward")
                    await mssg.edit(embed=embed)
                    next_advent =  current_time + ((60 * 60) * 20)
                    sql.execute_query("UPDATE Members SET dailyRewardClaimed = %s WHERE UserID = %s " % (str(next_advent), str(ctx.author.id)))
                    new_streak = streak + 1
                    sql.execute_query("UPDATE Members SET dailyRewardStreak = %s WHERE UserID = %s " % (str(new_streak), str(ctx.author.id)))
                elif msg.content == "2":
                    add_balance(ctx.author, round(0.10 + (streak * 0.01),2)*multiplier)
                    embed = discord.Embed(description="You unlocked **$" + str(round(0.10 + (streak * 0.01),2)*multiplier) + " **!", color=colour.primary)
                    embed.set_author(name="Daily Reward")
                    await mssg.edit(embed=embed)
                    next_advent =  current_time + ((60 * 60) * 20)
                    sql.execute_query("UPDATE Members SET dailyRewardClaimed = %s WHERE UserID = %s " % (str(next_advent), str(ctx.author.id)))
                    new_streak = streak + 1
                    sql.execute_query("UPDATE Members SET dailyRewardStreak = %s WHERE UserID = %s " % (str(new_streak), str(ctx.author.id)))
                elif msg.content == "3" and cookie_chance == 1:
                    embed = discord.Embed(description="You unlocked **3 Cookies**!", color=colour.primary)
                    embed.set_author(name="Daily Reward")
                    await mssg.edit(embed=embed)
                    cookies_no = sql.db_query("SELECT cookiesReceived FROM Members WHERE UserID = %s" % (str(ctx.author.id)))[0][0]
                    cookies_no = cookies_no + 3
                    sql.execute_query("UPDATE Members SET cookiesReceived = %s WHERE UserID = %s" % (str(cookies_no), str(ctx.author.id)))
                else:
                    embed = discord.Embed(description="Invalid Response", color=colour.reds)
                    embed.set_author(name="Daily Reward")
                    await mssg.edit(embed=embed)
        else:
            next_advent = last_advent
            time_difference = next_advent - current_time
            time_difference_string = time_phaser(time_difference)
            embed = discord.Embed(title="Error", description="You cannot use that command for another **%s**" % (time_difference_string), color=colour.reds)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Daily(client))
