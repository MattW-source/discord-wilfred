import discord
from discord.ext import commands
import os
import time
import utils.logging as log
import utils.values as value

client = commands.Bot(command_prefix = '!')
client.remove_command("help")

client.up = time.time()

client.conCooldown = []
client.cooldown = []
client.cooldown2 = []
client.disabled_commands = []
client.ignore_list = []
client.raffles = False
client.enteries = []

client.polls = False
client.polls_options = []
client.polls_votes = []
client.polls_enteries = []

'''Module Manager'''
@client.command()
async def load(ctx, extension):
    if "Manager" in [role.name for role in ctx.author.roles]:
        log.info("Loading extension %s" % (extension))
        client.load_extension(extension)
        log.info("Loaded extension %s" % (extension))
        await ctx.send("Successfully loaded %s!" % (extension))
    else:
        await ctx.send("**Insufficient Permissions:** This command requires permission rank `MANAGER`")

@client.command()
async def unload(ctx, extension):
    if "Manager" in [role.name for role in ctx.author.roles]:
        log.info("Unloading extension %s" % (extension))
        client.unload_extension(extension)
        log.info("Unloaded extension %s" % (extension))
        await ctx.send("Successfully unloaded %s!" % (extension))
    else:
        await ctx.send("**Insufficient Permissions:** This command requires permission rank `MANAGER`")

@client.command()
async def reload(ctx, extension):
    if "Manager" in [role.name for role in ctx.author.roles]:
        log.info("Reloading extension %s" % (extension))
        client.unload_extension(extension)
        client.load_extension(extension)
        log.info("Reloaded extension %s" % (extension))
        await ctx.send("Successfully reloaded %s!" % (extension))
    else:
        await ctx.send("**Insufficient Permissions:** This command requires permission rank `MANAGER`")

'''Initalisation'''
for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        client.load_extension("commands.%s" % (filename[:-3]))
        log.info("Loaded commands.%s" % (filename[:-3]))

for filename in os.listdir('./events'):
    if filename.endswith('.py'):
        client.load_extension("events.%s" % (filename[:-3]))
        log.info("Loaded events.%s" % (filename[:-3]))

client.run(value.token)
