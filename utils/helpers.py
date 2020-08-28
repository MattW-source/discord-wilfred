import utils.colours as colour
import utils.database as sql
import utils.logging as log
import utils.values as value
import random
import asyncio
import discord

def insert_db_user(member):
    try:
        sql.execute_query("INSERT INTO Members (UserID) VALUES ('%s')" % (member.id))
    except:
        log.warn("User already exists in Database")
        try:
            log.debug(member.name)
        except:
            pass

def give_item(item, member):
    items_current = fetch_items(member.id)[0][0]
    if items_current is None:
        items_new = item+"_"
    else:
        items_new = items_current + item +"_"
    sql.execute_query("UPDATE Members SET items = '%s' WHERE UserID = %s" % (items_new, str(member.id)))

def balance_formatter(balance):
    cBalance = "{:,}".format(balance)
    sBalance = cBalance.split(",")
    if len(sBalance) == 1:
        return str(balance)
    elif len(sBalance) == 2:
        sign = "K"
    elif len(sBalance) == 3:
        sign = "M"
    elif len(sBalance) == 4:
        sign = "B"
    elif len(sBalance) == 5:
        sign = "T"
    elif len(sBalance) >= 6:
        sign = "Q"
    fBalance = sBalance[0] + "." + sBalance[1][0:2] + sign
    return fBalance

def set_balance(user, balance):
    user_id = user.id
    sql.execute_query("UPDATE Members SET Balance = %s WHERE UserID = %s" % (str(balance), str(user_id)))

def set_balance_id(user_id, balance):
    sql.execute_query("UPDATE Members SET Balance = %s WHERE UserID = %s" % (str(balance), str(user_id)))

def fetch_items(userID):
    return sql.db_query("SELECT items FROM Members WHERE UserID = %s" % (str(userID)))

def fetch_balance(user):
    user_id = user.id
    balance = sql.db_query("SELECT Balance FROM Members WHERE UserID = %s" % (str(user_id)))[0][0]
    return balance

def fetch_balance_id(user_id):
    balance = sql.db_query("SELECT Balance FROM Members WHERE UserID = %s" % (str(user_id)))[0][0]
    return balance

def add_balance(user, amount):
    current_balance = fetch_balance(user)
    new_balance = round(float(current_balance) + float(amount), 2)
    set_balance(user, new_balance)

def add_balance_id(user_id, amount):
    current_balance = fetch_balance_id(user_id)
    new_balance = round(float(current_balance) + float(amount), 2)
    set_balance_id(user_id, new_balance)

def get_profile(userID):
    profile = sql.db_query("SELECT Balance, Level, expTotal, Badges, profileColour, profileHashtag, exp FROM Members WHERE UserID = %s" % (userID))[0]
    return profile

def level_up(userID, level):
    sql.execute_query("UPDATE Members SET Level = %s WHERE UserID = %s" % (str(level), str(userID)))

async def check_level_up(userID, guild, channel):
    Checking = True
    while Checking:
        level_data = sql.db_query("SELECT Exp, Level FROM Members WHERE UserID = %s" % (str(userID)))[0]
        Exp = level_data[0]
        lvl = level_data[1]
        Required = 5 * (lvl * lvl) + (50 * lvl) + 100
        if Exp >= Required:
            level_up(userID, lvl+1)
            sub_exp_only(userID, Required)
            lvl = lvl+1
            balAdd = float(lvl/100)
            add_balance_id(userID, float(balAdd))
            user = discord.utils.get(guild.members, id=userID)
            if lvl in [3, 15, 30, 45, 60, 75, 90]:
                if lvl == 3:
                    new_role = discord.utils.get(guild.roles, id=547132381073768494)
                    await user.add_roles(new_role)
                    await channel.send(embed=discord.Embed(title="Level Up!", description="Congratulations %s! You've reached Level 3! That means you've unlocked the `%s` role!" % (user.mention, new_role.name), color=colour.primary))
                else:
                    if lvl == 15:
                        new_role = discord.utils.get(guild.roles, id=547132866094432260)
                        old_role = discord.utils.get(guild.roles, id=547132381073768494)
                    elif lvl == 30:
                        new_role = discord.utils.get(guild.roles, id=547133065298837525)
                        old_role = discord.utils.get(guild.roles, id=547132866094432260)
                    elif lvl == 45:
                        new_role = discord.utils.get(guild.roles, id=547133123503194112)
                        old_role = discord.utils.get(guild.roles, id=547133065298837525)
                    elif lvl == 60:
                        new_role = discord.utils.get(guild.roles, id=547133176435310603)
                        old_role = discord.utils.get(guild.roles, id=547133123503194112)
                    elif lvl == 75:
                        new_role = discord.utils.get(guild.roles, id=630451524602036254)
                        old_role = discord.utils.get(guild.roles, id=547133176435310603)
                    elif lvl == 90:
                        new_role = discord.utils.get(guild.roles, id=690185873056071721)
                        old_role = discord.utils.get(guild.roles, id=630451524602036254)
                    await user.add_roles(new_role)
                    await user.remove_roles(old_role)
                    await channel.send(embed=discord.Embed(title="Level Up!", description="Congratulations %s! You've reached Level %s! That means you've unlocked the `%s` role!" % (user.mention, str(lvl), new_role.name), color=colour.primary))
        else:
            Checking = False

def fetch_exps(userID):
    return sql.db_query("SELECT Exp, ExpTotal FROM Members WHERE UserID = %s" % (str(userID)))[0]

def set_exp(userID, amount):
    sql.execute_query("UPDATE Members SET Exp = %s WHERE UserID = %s" % (str(amount),str(userID)))

def set_exp_max(userID, amount):
    sql.execute_query("UPDATE Members SET ExpTotal = %s WHERE UserID = %s" % (str(amount),str(userID)))

def sub_exp_only(userID, amount):
    current_exps = fetch_exps(userID)
    new_exp = int(current_exps[0])-amount
    set_exp(userID, new_exp)

def add_exp(userID, amount):
    current_exps = fetch_exps(userID)
    new_exp = int(current_exps[0])+amount
    new_max = int(current_exps[1])+amount
    set_exp(userID, new_exp)
    set_exp_max(userID, new_max)

def get_rank(user):
    rank = []
    if "Manager" in [role.name for role in user.roles]:
        rank.append("Community Manager")
        rank.append("https://cdn.discordapp.com/emojis/547141066139369473.png?v=1")
    elif "Moderator" in [role.name for role in user.roles]:
        rank.append("Community Moderator")
        rank.append("https://cdn.discordapp.com/emojis/547141066139369473.png?v=1")
    elif "Extra Permissions" in [role.name for role in user.roles]:
        rank.append("Developer")
        rank.append("https://cdn.discordapp.com/emojis/614952848261775362.png?v=1")
    elif "Supporter" in [role.name for role in user.roles]:
        rank.append("Supporter")
        rank.append("https://media.discordapp.net/attachments/573994945518764091/582268065102692362/nitroBoost.png")
    else:
        rank.append("Member")
        rank.append("https://cdn.discordapp.com/emojis/547141731850780672.png?v=1")

    return rank

def time_phaser(seconds):
    output = ""
    print(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    mo, d = divmod(d, 30)
    if mo > 0:
        output = output + str(int(round(m, 0))) + " Months "
    if d > 0:
        output = output + str(int(round(d, 0))) + " Days "
    if h > 0:
        output = output + str(int(round(h, 0))) + " Hours "
    if m > 0:
        output = output + str(int(round(m, 0))) + " Minutes "
    if s > 0:
        output = output + str(int(round(s, 0))) + " Seconds "
    return output


async def discord_error(errorMessage: str, ctx):

    '''
        Generates an error embed and sends it to the provided context's channel
    '''

    em = discord.Embed(description=errorMessage, color=colour.reds)
    em.set_author(name="Error")
    await ctx.send(embed=em)
