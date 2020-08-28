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
        log.debug("%s issued server command %s" % (str(ctx.message.author), str(ctx.message.content)))
        current_time = time.time()
        query = sql.db_query("SELECT dailyRewardClaimed, dailyRewardStreak FROM Members WHERE UserID = %s " % (str(ctx.author.id)))
        last_advent = query[0][0]
        streak = query[0][1]
        if last_advent < current_time:
            next_advent =  current_time + ((60 * 60) * 20)
            sql.execute_query("UPDATE Members SET dailyRewardClaimed = %s WHERE UserID = %s " % (str(next_advent), str(ctx.author.id)))
            reward = random.randint(1, 4)
            if reward == 1:
                reward_name = "5000 Exp"
                add_exp(ctx.author.id, 5000)
            if reward == 2:
                reward_name = "$5.00"
                add_coins(ctx.author, float(5.00))
            if reward == 3:
                reward_name = "2 Crates"
                crates_no = sql.db_query("SELECT crates FROM Members WHERE UserID = %s" % (str(ctx.author.id)))[0][0]
                crates_no = crates_no + 2
                sql.execute_query("UPDATE Members SET crates = %s WHERE UserID = %s" % (str(crates_no), str(ctx.author.id)))
            if reward == 4:
                reward_name = "3 Crates"
                crates_no = sql.db_query("SELECT crates FROM Members WHERE UserID = %s" % (str(ctx.author.id)))[0][0]
                crates_no = crates_no + 3
                sql.execute_query("UPDATE Members SET crates = %s WHERE UserID = %s" % (str(crates_no), str(ctx.author.id)))
            embed = discord.Embed(title="Easter Reward", description="You Won " + reward_name, color=colour.primary)
            await ctx.send(embed=embed)
            new_streak = streak + 1
            sql.execute_query("UPDATE Members SET dailyRewardStreak = %s WHERE UserID = %s " % (str(new_streak), str(ctx.author.id)))
        else:
            next_advent = last_advent
            time_difference = next_advent - current_time
            time_difference_string = time_phaser(time_difference)
            embed = discord.Embed(title="Error", description="You cannot use that command for another **%s**" % (time_difference_string), color=colour.reds)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Daily(client))
