import discord
from discord.ext import commands, tasks
import random
import datetime
import time
import sys
import asyncio
import os
from discord.utils import get
from discord.ext.tasks import loop
from discord.ext.commands import Bot, has_permissions
from random import choice
import requests
from setup import myid, token, logschannelid, myserverid, prefix

description = 'MultiPurpose-Bot'
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=prefix, description=description,intents=intents)
counter = 0
typeStatusListen = discord.ActivityType.listening
typeStatusStream = discord.ActivityType.streaming
bot.remove_command("help")
# Below are examples of activites. Not bad stuff, just mess around with it and have some fun
# activity=discord.Activity(type=typeStatusListen, name=game))
# await bot.change_presence(status=discord.Status.idle, activity=discord.Streaming(platform='Twitch', url='https://twitch.tv/<twitch>', name=f"{prefix}help | {prefix}info", twitch_name="<twitch>"))

@bot.event
async def on_ready():
    # Important code, I suppose
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print(f'Present in {len(bot.guilds)} servers.')
    print('------')
    global game
    game = f"{prefix}help | Watching over {len(bot.guilds)} servers"
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=typeStatusListen, name=game))
    count.start()

@bot.event
async def on_member_join(member):
    # Sends a welcome message on a member's join to a server
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
        await guild.system_channel.send(to_send)

@bot.event
async def on_message(message):
    # This is a nifty little thing you can mess around with, check out the example code below
    # It allows you to "run commands" without the prefix required
    if message.content == "Creeper":
        await message.channel.send("awww man")
    await bot.process_commands(message)

@tasks.loop(seconds=1)
async def count():
    # Used for a command later on. You'll see
    global counter
    counter += 1

@bot.command()
async def stop(ctx):
    # This command forces the bot to stop running
    if ctx.author.id == myid:
        await ctx.send("Stopping...")
        print("Stopping...")
        await ctx.send("Session ended.")
        sys.exit("Session Ended.")

@bot.command()
async def restart(ctx):
    # The most useful command I have ever written. Do not disregard this one, fellow developer
    if ctx.author.id == myid:
        await ctx.send("Restarting/ending session...")
        print("Restarting...")
        os.execl(sys.executable, sys.executable, *sys.argv)

@bot.event
async def on_raw_message_edit(payload):
    # Took a lot of time to work on this. Make sure to specify a log channel id and a server id in setup.py file
    if logschannelid:
        guild = discord.utils.get(bot.guilds, id=myserverid)
        channel = discord.utils.get(guild.channels, id=payload.channel_id)
        amsg = await channel.fetch_message(payload.message_id)
        logschannel = discord.utils.get(guild.channels, id=logschannelid)
        user = amsg.author
        if channel != logschannel:
            if payload.cached_message:
                msg = payload.cached_message
                embed = discord.Embed(title=f"Message edited in #{channel.name}", colour=discord.Colour(0x226611), description=f"**Before:** \"{msg.content}\"\n"
                f"**After:** \"{amsg.content}\"\n"
                f"**View message:** https://discordapp.com/channels/{guild.id}/{channel.id}/{payload.message_id}")
                embed.set_author(name=f"{user.name}", icon_url=user.avatar_url)
                await logschannel.send(embed=embed)
            if not payload.cached_message:
                embed = discord.Embed(title=f"Message edited in #{channel.name}", colour=discord.Colour(0x226611), description=f"**Content:** \"{amsg.content}\"\n"
                "**This message is too old to be viewed**\n"
                f"**View message:** https://discordapp.com/channels/{guild.id}/{channel.id}/{payload.message_id}")
                embed.set_author(name=f"{user.name}", icon_url=user.avatar_url)
                await logschannel.send(embed=embed)

@bot.event
async def on_raw_message_delete(payload):
    # Took a lot of time to work on this. Make sure to specify a log channel id and a server id in setup.py file
    if logschannelid:
        guild = discord.utils.get(bot.guilds, id=myserverid)
        try: channel = discord.utils.get(guild.channels, id=payload.channel_id)
        except: return
        logschannel = discord.utils.get(guild.channels, id=logschannelid)
        if payload.cached_message:
            msg = payload.cached_message
            user = msg.author
            embed = discord.Embed(title=f"Message deleted in #{channel.name}", colour=discord.Colour(0x226611), description=f"**Deleted message:** \"{msg.content}\"")
            embed.set_author(name=f"{user.name}", icon_url=user.avatar_url)
            await logschannel.send(embed=embed)
        if not payload.cached_message:
            embed = discord.Embed(title=f"Message deleted in #{channel.name}", colour=discord.Colour(0x226611), description=f"**This message is too old to be viewed**")
            embed.set_author(name=f"Unknown#0000", icon_url="https://mi460.dev/images/discord.png")
            await logschannel.send(embed=embed)

@bot.command(pass_context=True)
async def help(ctx):
    # You can mess around with the embed to get it to your taste. This is just an example of what mine looks like
    embed = discord.Embed(title="Delta Inc.", colour=discord.Colour(0x2EA64E), url="https://mi460.dev/", description="```Commands for Github-Bot```")

    embed.set_thumbnail(url="https://mi460.dev/images/cubeicon.png")
    embed.set_author(name="Github-Bot#1370", url="https://mi460.dev/mpbot/", icon_url="https://mi460.dev/images/cubeicontransparent.png")
    embed.set_footer(text="Check out my website and discord server!", icon_url="https://mi460.dev/images/bb3e970011dc603cf63eb73182a33122.png")

    embed.add_field(name=f"`{prefix}kick`", value="Kicks a specified member. Requires admin priviledges.")
    embed.add_field(name=f"`{prefix}ban`", value="Bans a specified member. Requires admin priviledges.")
    embed.add_field(name=f"`{prefix}purge`", value="Deletes specified number of messages in the channel the command was issued in. Requires admin priviledges.")
    embed.add_field(name=f"`{prefix}<math command>`", value="Performs basic operations like: `add, subtract, multiply, divide, modulo, and exponent`.")
    embed.add_field(name=f"`{prefix}ping`", value="Checks the bot/server latency relationship.")
    embed.add_field(name=f"`{prefix}joined`", value="Shows specified user's join date to that discord server.")
    embed.add_field(name=f"`{prefix}uptime`", value="Displays the amount of time the bot has been up consecutively")
    embed.add_field(name=f"`{prefix}time`", value="Displays the current time (timezones vary)")
    embed.add_field(name=f"`{prefix}roll`", value="Rolls dice in NdN format")
    embed.add_field(name=f"`{prefix}talk`", value="Impersonates people! Use =talk @(someone) <text> to speak as them!")
    embed.add_field(name=f"`{prefix}choose`", value="Chooses between multiple choices")
    embed.add_field(name=f"`{prefix}cool`", value="Says if a <anything> is cool")

    await ctx.send(content="If a command doesn't work, make sure to check the permissions of the bot.", embed=embed)

@bot.command(description='For adding numbers.')
async def add(ctx, left: int, right: int):
    # Drop the calculation if the input is none.
    if left == None or right == None:
        await ctx.send("Please give proper values to add.")
    # Finds the sum of two numbers
    await ctx.send(f"The sum of {left} and {right} is: {left + right}")

@bot.command(description='For subtracting numbers.')
async def subtract(ctx, left: int, right: int):
    # Drop the calculation if the input is none.
    if left == None or right == None:
        await ctx.send("Please give proper values to subtract.")
    # Finds the difference between two numbers
    await ctx.send(f"The difference of {left} and {right} is: {left - right}")

@bot.command(description='For multiplying numbers.')
async def multiply(ctx, left: int, right: int):
    # Drop the calculation if the input is none.
    if left == None or right == None:
        await ctx.send("Please give proper values to multiply.")
    # Finds the product of two numbers
    await ctx.send(left * right)

@bot.command(description='For dividing numbers.')
async def divide(ctx, left: int, right: int):
    # Drop the calculation if the input is none.
    if left == None or right == None:
        await ctx.send("Please give proper values to divide.")
    # Finds the result of two numbers
    await ctx.send(left / right)

@bot.command(description='For dividing numbers, but...')
async def modulo(ctx, left: int, right: int):
    # Divides two numbers, but only outputs the remainder
    await ctx.send(left % right)

@bot.command(description='For exponents.')
async def exponent(ctx, left: int, right: int):
    # Outputs the base to the power of the index
    await ctx.send(left ** right)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member = None, reason: str = "None"):
    # Kicks a specified member. Remember, the command only has as much power as the bot
    if not member:
        await ctx.send("Please specify a member")
        return
    await member.kick()
    await ctx.send(f"{member.mention} has been kicked by {ctx.author.mention}.\nReason: {reason}")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have the permissions to kick this person.")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the permissons to do that.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member = None, reason: str = "None"):
    # Bans a specified member. Remember, the command only has as much power as the bot
    if not member:
        await ctx.send("Please specify a member.")
        return
    await member.ban()
    await ctx.send(f"{member.mention} has been banned by {ctx.author.mention}.\nReason: {reason}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have the permissions to ban this person.")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the permissons to do that.")

@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    # Deletes a large, specified amount of messages from a channel. Requires admin priviledges
    await ctx.message.delete()
    await ctx.channel.purge(limit=limit)
    await ctx.send('{} Messages cleared by {}'.format(limit, ctx.author.mention))

@purge.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the permissons to do that.")

@bot.command()
async def ping(ctx):
    # Shows the current Discord/Bot latency relationship
    await ctx.send('`Pong! My current latency is {0} seconds.`'.format(round(bot.latency)))

@bot.command(pass_context = True)
async def say(ctx, *, mg = None):
    # Says anything you want your bot to say. By default, limited to you only
    await ctx.message.delete()
    if ctx.author.id == myid:
        if not mg: await ctx.author.send("Please specify a message to send")
        else: await ctx.send(mg)

@bot.command()
async def roll(ctx, dice: str):
    # Rolls dice in NdN format. Not mine, Discord's code
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def choose(ctx, *choices: str):
    # A command that chooses between multiple choices
    await ctx.send(f"`{random.choice(choices)}` was chosen out of `{choices}`")

@bot.command(pass_context = True)
async def getuser(ctx, user:discord.Member = None):
    # Gets basic user data from a mentioned user
    if not user:     # If user is not mentioned, show the stats of the msg author
        user = ctx.author
    embed = discord.Embed(title="Click here for support", colour=discord.Colour(0x4287f5), url="https://mi460.dev/bugs", description=f"Info about `{user.name}#{user.discriminator}`")
    embed.set_author(name=f"{user.name}#{user.discriminator}", url=f"{user.avatar_url}", icon_url=f"{user.avatar_url}")
    embed.add_field(name=f"{user.display_name}'s join date", value=f"User account joined server at `{ctx.guild.get_member(int(userid)).joined_at}`")
    embed.add_field(name=f"{user.display_name}'s creation date", value=f"User account created at `{user.created_at}`")
    await ctx.send(embed=embed)

@bot.command()
async def uptime(ctx):
    # The amount of time the bot has been up consecutively
    await ctx.send(f"This bot has been up for `{counter}` seconds.")

@bot.command()
async def time(ctx):
    # Displays current time. Remember timezones.
    currentTime = datetime.datetime.now().time()
    await ctx.send(f'`The current time is {currentTime}`')

@bot.command(pass_context=True)
async def status(ctx, *, tempgame = None):
    # Changes the bot's status. By default, it is limited to the owner only
    if ctx.author.id == myid:
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=typeStatusListen, name=tempgame))

@bot.command()
async def cool(ctx, *, object = None):
    # The original repo had this command as an example, but I thought it should give you an equal chance at coolness
    # The `` around {object} prevents @everyone pings
    if not object:
        await ctx.send("Please specify what should be cool.")
    else:
        flip = random.randint(0, 1)
        if flip == 1:
            await ctx.send(f"No, `{object}` is not cool >:(")
        else:
            await ctx.send(f"Yes, `{object}` is very cool!")

@bot.command(pass_context=True)
async def talk(ctx, userid: str, *, text = None):
    # A neat webhook impersonation command I came up with
    await ctx.message.delete()
    if userid and text:
        channel = ctx.channel
        userid = userid.replace("<@!", "")
        userid = userid.replace("<@", "")
        userid = userid.replace(">", "")
        userid = int(userid)
        text = text.replace("@everyone", "")
        text = text.replace("@here", "")
        user = discord.utils.get(ctx.guild.members, id=userid)
        userpicurl = user.avatar_url
        if user.nick:
            username = user.nick
        if not user.nick:
            username = user.name
        userpic = requests.get(userpicurl)
        webhook = await channel.create_webhook(name=username, avatar=userpic.content)
        await webhook.send(text)
        await webhook.delete()
        # Get rid of the next line of code if you'd like it to be untraceable.
        await user.send(f"Psssst.... {ctx.author} is impersonating you in {ctx.channel}.")
    if not text:
        await ctx.author.send("Please specify a message to send.")

bot.run(token)
