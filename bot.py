import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

# On boot
@client.event
async def on_ready():
    print("We're soaring!!")

# Ping command
@client.command()
async def ping(ctx):
    await ctx.send(f'{ctx.message.author.mention} Pong! ({round(client.latency * 1000)}ms)')

client.run('NjYyNTUzMDQzMzg0MTM5Nzg2.Xg7osQ.kXo4my7NoMSnF_3z5F3F8AtRI_k')