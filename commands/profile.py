import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class Profile(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def profile(self, ctx, user : discord.Member = None):
        message = ctx.message
        if user is None:
            user = ctx.author

        profile = get_profile(user.id)

        if "Supporter" in [role.name for role in user.roles]:
            em = discord.Embed(title=user.name, colour=0xf231ff)
        else:
            em = discord.Embed(title=user.name, colour=eval(profile[4]))

        exps = sql.db_query("SELECT UserID FROM Members WHERE NOT UserID = 472063067014823938 AND NOT UserID = 1 ORDER BY expTotal DESC")
        lpos = 1
        for userl in exps:
            userlOb = discord.utils.get(ctx.guild.members, id=userl[0])
            if userlOb is None or userlOb.bot:
                pass
            elif not userl[0] == user.id:
                lpos = lpos + 1
            else:
                break

        activity = sql.db_query("SELECT UserID FROM Members WHERE NOT UserID = 472063067014823938 AND NOT UserID = 1 ORDER BY weeklyActivity DESC")
        apos = 1
        for usera in activity:
            if not usera[0] == user.id:
                apos = apos + 1
            else:
                break

        bals = sql.db_query("SELECT UserID FROM Members WHERE NOT UserID = 472063067014823938 AND NOT UserID = 1 ORDER BY Balance DESC")
        bpos = 1
        for userb in bals:
            if not userb[0] == user.id:
                bpos = bpos + 1
            else:
                break


        rank = get_rank(user)
        cookies_no = sql.db_query("SELECT cookiesReceived FROM Members WHERE UserID = %s" % (str(user.id)))[0][0]
        em.set_author(name=rank[0], icon_url=rank[1])

        badges = profile[3]

        exp = profile[6]
        expCost = 5 * (profile[1]*profile[1]) + 50 * profile[1] + 100

        preLevelTotal = profile[2] - exp
        nextRequiredAmount = preLevelTotal + expCost

        cosmetics_all = sql.db_query("SELECT cosmetic_id FROM cosmetics")
        cosmetics_total = len(cosmetics_all)
        inventory = eval(sql.db_query("SELECT cosmetics FROM Members WHERE UserID = %s" % (str(user.id)))[0][0])
        inventory_size = len(inventory)

        em.add_field(name=badges, value="_ _ _ _ ")
        em.set_thumbnail(url=user.avatar_url)
        em.add_field(name="_ _ _ _", value="_ _ _ _", inline=False)
        em.add_field(name="Level", value=str(profile[1])+ " [**#" + str(lpos) + "**]")
        em.add_field(name="Experience", value=str(profile[2])+ "/" + str(nextRequiredAmount))
        em.add_field(name="Member Since", value=str(user.joined_at)[0:19])

        em.add_field(name="Balance", value="$"+str(balance_formatter(round(float(profile[0]),2 ))))
        em.add_field(name="Cookies Received", value=str(cookies_no))
        em.add_field(name="Cosmetics Unlocked", value="%s/%s" % (str(inventory_size), str(cosmetics_total)))
        if not profile[5] is None:
            em.set_footer(text=""+profile[5])

        await message.channel.send(embed=em)

def setup(client):
    client.add_cog(Profile(client))
