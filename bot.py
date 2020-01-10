import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

# On boot
@client.event
async def on_ready():
    print("We're soaring!!")

client.run('NjYyNTUzMDQzMzg0MTM5Nzg2.Xg7osQ.kXo4my7NoMSnF_3z5F3F8AtRI_k')