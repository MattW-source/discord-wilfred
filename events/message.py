import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class On_Message(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            def check(m):
                flag = False
                m_split = m.content.translate({ord(i): None for i in '",.?!;:-_`*\''}).upper().split(" ")
                banned_words = ["NIGGER", "NIGGA", "AUTISTIC", "RETARD", "RETARDED", "AIDS", "SPASTIC", "SPAZ", "RETARDS"]
                for word in banned_words:
                    if word in m_split:
                        flag = True
                        #print(m.content)
                return flag

            if check(message):
                await message.delete()
                return 0

            message.content = message.content.replace("@!", "@") #crappy fix for the mention inconsistency between platforms

            if len(message.content) == 0:
                return
            if isinstance(message.channel, discord.DMChannel):
                log.info("Ignoring Direct Message From %s: %s" % (str(message.author), str(message.content)))
                return
            mSplit = message.content.split()
            mList = []
            for word in mSplit:
                user = discord.utils.get(message.guild.members, mention=word.replace("@", "@!").replace("!!", "!"))
                if not user is None:
                    if not user.nick is None:
                        word = word.replace("@", "@!").replace("!!", "!")
                mList.append(word)
            message.content = " ".join(mList)

            if message.content.upper().startswith("V!UPDATE"):
                await message.channel.send("Syncing DB")
                for member in message.guild.members:
                    insert_db_user(member)
                await message.channel.send("Completed DB Sync")

            args = message.content.split(" ")

            if message.content[0] == "$":
                message.content = message.content.replace("$", "!tag ")
                await self.client.process_commands(message)

            if args[0].lower() in self.client.disabled_commands:
                await error("[423] This command is currently disabled", message.channel)
                return False
            channel = message.channel

            if message.content.upper().startswith("!ENTER"):
                if "Manager" in [role.name for role in message.author.roles] and self.client.raffles:
                    embed = discord.Embed(title="Raffle", description="Sorry %s, you are not allowed to enter raffles." % (message.author.mention), color=colour.reds)
                    await message.channel.send(embed=embed)
                elif self.client.raffles and not message.author.name in self.client.enteries:
                    self.client.enteries.append(message.author.name)
                    embed = discord.Embed(title="Raffle", description="**%s** has been entered!" % (message.author.name), color=0x00ff73)
                    await message.channel.send(embed=embed)
                elif self.client.raffles:
                    embed = discord.Embed(title="Raffle", description="Hey %s! You can only enter into the same raffle once!" % (message.author.mention), color=colour.reds)
                    await message.channel.send(embed=embed)

            if message.content.upper().startswith("!VOTE"):
                if self.client.polls and not message.author.name in self.client.polls_enteries:
                    args = message.content.split(" ")
                    try:
                        choice = int(args[1])
                        self.client.polls_votes[choice-1] += 1
                    except (IndexError, TypeError, ValueError):
                        embed = discord.Embed(title="Poll", description="Hey %s! That is not a valid option!" % (message.author.mention), color=colour.reds)
                        await message.channel.send(embed=embed)
                        return

                    self.client.polls_enteries.append(message.author.name)
                    embed = discord.Embed(title="Poll", description="**%s** you have voted for %s" % (message.author.name, self.client.polls_options[choice-1]), color=0x00ff73)
                    await message.channel.send(embed=embed)
                elif self.client.polls:
                    embed = discord.Embed(title="Poll", description="Hey %s! You can only vote once" % (message.author.mention), color=colour.reds)
                    await message.channel.send(embed=embed)

            if message.content.upper().startswith("!SUDO"):
                if message.author.id == 345514405775147023:
                    args = message.content.split()
                    target = discord.utils.get(message.guild.members, mention=args[1])
                    channel = self.client.get_channel(int(args[2]))
                    contents = " ".join(args[3:])
                    message.content = contents
                    message.author = target
                    message.channel = channel
                    await self.client.process_commands(message)

            if message.guild == None:
                return

            words = message.content.split()
            if not str(message.author.id) in self.client.ignore_list and not str(message.channel.id) in self.client.ignore_list and not message.author.id in self.client.cooldown and len(words) > 4 and len(message.content) > 16:
                multiplier = sql.db_query("SELECT Level FROM Members WHERE UserID = 1")[0][0]
                if "Supporter" in [role.name for role in message.author.roles]:
                    multiplier = multiplier+0.5
                bal = sql.db_query("SELECT Balance FROM Members WHERE UserID = %s" % (str(message.author.id)))[0][0]
                if not "Manager" in [role.name for role in message.author.roles]:
                    currentWeeklyPoints = sql.db_query("SELECT weeklyActivity from Members WHERE UserID = %s" % (str(message.author.id)))[0][0]
                    newWeeklyPoints = currentWeeklyPoints + 1
                    sql.execute_query("UPDATE Members set weeklyActivity = %s WHERE UserID = %s" % (str(newWeeklyPoints), str(message.author.id)))
               
                level = get_profile(message.author.id)[1]
                self.client.cooldown.append(message.author.id)
                exp_add = int(round(random.randint(15, 25)*multiplier,0))
                add_exp(message.author.id, exp_add)
                channel = self.client.get_channel(547120498568331267)
                await check_level_up(message.author.id, message.guild, message.channel)
                await asyncio.sleep(60)
                try:
                    self.client.cooldown.remove(message.author.id)
                except ValueError: #some people aren't always on cooldown
                    pass

            def check(m):
                flag = False
                m_split = m.content.translate({ord(i): None for i in '",.?!;:-_`*\''}).upper().split(" ")
                banned_words = ["FUCK", "FUCKING", "DICK", "BOLLOCK", "FUCKS", "AIDS", "BOLLOCKS", "FUCKED", "WHORE", "BASTARD", "SHIT", "SHITTING", "CUNT", "WANKER", "BASTARD", "BELLEND", "NIGGA", "NIGGER", "PISS", "PISSING", "CUNT", "CUNTS", "WANKERS", "RETARDS", "RETARD", "RETARDED", "FAGGOT", "FKING", "FK", "CRAP", "PUSSY", "PENIS", "COCK"]
                for word in banned_words:
                    if word in m_split:
                        flag = True

                return flag

        except Exception as e:
            log.error("Error Processing Message From %s - Error: %s" % (str(message.author), str(e)))



def setup(client):
    client.add_cog(On_Message(client))
