import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *

class Fight(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def fight(self, ctx):
        bal = fetch_balance(ctx.author)
        if bal >= 0.05:
            add_balance(ctx.author, -0.05)
            message = ctx.message
            args = message.content.split()
            loss = 0
            rounds = 1
            init = message.author.mention
            target = " ".join(args[1:])
            fight = "%s has challenged %s to a fight!" % (init, target) + "\n"
            fightEm = discord.Embed(description=fight, colour=colour.reds)
            fightEm.set_author(name="Fight")
            fMessage = await message.channel.send(embed=fightEm)
            while not (loss == 1) and not (rounds > 7):
                fight = fight + random.choice(["%s threw a chair at %s" % (init, target), "%s whacked %s with a stick" % (init, target), "%s slapped %s to the floor" % (init, target), "%s threw %s through a wall" % (init, target), "%s bitch slapped %s" % (init, target), "%s used dark magic against %s" % (init, target), "%s used the infinity gauntlet" % (init), "%s used fake news on %s" % (init, target), "%s ran %s over with a truck" % (init, target), "%s ate %s and threw them up again" % (init, target), "%s savagely roasted %s for sunday lunch" % (init, target), "%s forced %s to watch anime" % (init, target), "%s slapped %s with a Macbook" % (init, target), "%s used TUNNELBEAR! THE FREE EASY TO USE VPN..." % (init), "%s performed a windows update on %s" % (init, target), "%s used the might of Zeus" % (init), "%s trapped %s in Flex Tape" % (init, target), "%s built a wall!" % (init)])+"\n"
                fightEm = discord.Embed(title="Fight!", description=fight, colour=colour.reds)
                await fMessage.edit(embed=fightEm)
                await asyncio.sleep(2)
                loss = random.randint(1, 4)
                if loss == 1:
                    fight = fight + "%s accepts defeat! %s has won the fight!" % (target, init)
                elif rounds == 7:
                    fight = fight + "The fight has ended in a draw!"
                else:
                    fight = fight +"%s does not giveup and continues the fight!" % (target) + "\n"
                fightEm = discord.Embed(description=fight, colour=colour.reds)
                fightEm.set_author(name="Fight")
                await fMessage.edit(embed=fightEm)
                temp = target
                target = init
                init = temp
                rounds = rounds + 1
                await asyncio.sleep(4)
        else:
            await ctx.send("%s you do not have sufficient funds for this!" % (ctx.message.author.mention))


def setup(client):
    client.add_cog(Fight(client))
