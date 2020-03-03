import discord
import random
import asyncio
import requests
import json
import feedparser
from datetime import datetime
from discord.ext import commands
import variables

client = commands.Bot(command_prefix = variables.BOT_PREFIX)

# On boot
@client.event
async def on_ready():
    print("We're soaring!!")

# event per message
@client.event
async def on_message(message):
    print(str(message.author.display_name) + ' said something in ' + str(message.channel.name) + '(' + str(message.channel.id) + ')')
    await client.process_commands(message)

# Ping command
@client.command()
async def ping(ctx):
    await ctx.send(f'{ctx.message.author.mention} Pong! ({round(client.latency * 1000)}ms)')

# Status changer
async def change_status():
    await client.wait_until_ready()
    while True:
        print('Editing Status..')
        current_status =random.choice(variables.STATUSES)
        await client.change_presence(activity=discord.Game(name=current_status))
        await asyncio.sleep(variables.STATUS_SPEED)

# refresh FF@15
async def poll_ff15():
    await client.wait_until_ready()
    while True:
        print("Fetching new FF@15 news..")
        # Get previous posts
        with open(variables.SURRENDER_POSTS_FILE, 'r') as f:
            posts = json.load(f)
        # Get Feed
        resp = requests.get(variables.SURRENDER_RSS_FEED_URL)
        parsed = feedparser.parse(resp.content)
        # loop REVERSED(old first) over each entry and check if it already has been posted
        for nPost in parsed.entries[::-1]:
            await try_post(posts, nPost)        
        # Save new posts 
        with open(variables.SURRENDER_POSTS_FILE, 'w') as f:
            json.dump(posts, f) 
        await asyncio.sleep(variables.SURRENDER_POLL_INTERVAL * 60)

# fun 8ball thingie
@client.command(aliases=['8ball','predict'])
async def _8ball(ctx, *, question):
    await ctx.send(f'{ctx.message.author.mention} asked: {question}\nAnswer: {random.choice(variables.RESPONSES)}')

# Delete all (999) mesages of channel
@client.command()
async def clear(ctx, amount=999):
    await ctx.channel.purge(limit=amount)

# Get Json
@client.command()
async def dumpJson(ctx):
    print("Fetching Json..")
    with open(variables.SURRENDER_POSTS_FILE, 'r') as f:
        posts = json.load(f)
    # Get Feed
    await client.get_channel(variables.SURRENDER_CHANNEL_ID).send(posts)

# FF@20 functionality
async def send_embeded(newPost):
    # get usefull stuff out
    img = newPost.media_thumbnail[0]["url"]
    link = newPost.link
    title = newPost.title
    # cleaning them up a bit
    slashes = [i for i,c in enumerate(img) if c=='/']
    img = img[0:slashes[-2]] + img[slashes[-1]:]
    # make an nice embeded post
    embed = discord.Embed(
        title = title,
        colour = discord.Colour.orange(),
        url = link
    )
    embed.set_footer(text="Posted @ "+ datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    embed.set_image(url=img)    
    # send message
    await client.get_channel(variables.SURRENDER_CHANNEL_ID).send(embed=embed)

async def try_post(posts, nPost):
    if nPost.id in posts:
        return
    else:
        # Add it to the list
        posts[nPost.id] = {}
        posts[nPost.id] = "Posted @ "+ datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        # Make an embedded msg for it
        await send_embeded(nPost)

# Run the bot
client.loop.create_task(change_status())
client.loop.create_task(poll_ff15())
client.run(variables.BOT_TOKEN)