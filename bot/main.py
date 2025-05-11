import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()  # Loads variables from .env into environment

TOKEN = os.getenv("DISCORD_TOKEN")

GUILD_ID = 1176896434587570269
ELIMINATED_ROLE_ID = 1370727530289692834
PARTICIPANT_ROLE_ID = 1370729934992969828
RED_CORNER_ID = 1176896434587570273
BLUE_CORNER_ID = 1370738478731755560
MODERATOR_ROLE_ID = 1370752012668375150
GENERAL_CHANNEL_ID = 1176896434587570272

remove_role_enabled = False

intents = discord.Intents.default()
intents.message_content = True 
intents.voice_states = True  
intents.members = True 

client = commands.Bot(command_prefix="$", intents=intents)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))  

@client.event
async def on_voice_state_update(member, before, after):
    guild = client.get_guild(GUILD_ID)
    log_channel = guild.get_channel(GENERAL_CHANNEL_ID)

    if guild is None:
        print("Guild not found!")
        return
    
    eliminated_role = guild.get_role(ELIMINATED_ROLE_ID)
    participant_role = guild.get_role(PARTICIPANT_ROLE_ID)
    moderator_role = guild.get_role(MODERATOR_ROLE_ID)

    if not remove_role_enabled:
        return
    
    if before.channel is not None and after.channel is None:
        if moderator_role in member.roles:
            return
        
        await member.remove_roles(participant_role)
        await member.add_roles(eliminated_role)
        await log_channel.send(f"User {member.display_name} `{member.id}` has been eliminated.")

@client.command()
@commands.has_role(MODERATOR_ROLE_ID)
async def startcheck(ctx):
    "Enables the opertation of removing participant role if a user leaves a VC"

    global remove_role_enabled 

    if remove_role_enabled == True:
        await ctx.channel.send(f"Voice check is already enabled.")
        return
    
    remove_role_enabled = True
    await ctx.channel.send(f"Voice check has been enabled.")

@client.command()
@commands.has_role(MODERATOR_ROLE_ID)
async def stopcheck(ctx):
    "Disables the opertation of removing participant role if a user leaves a VC"

    global remove_role_enabled 

    if remove_role_enabled == False:
        await ctx.channel.send(f"Voice check is already disabled.")
        return
    
    remove_role_enabled = False
    await ctx.channel.send(f"Voice check has been disabled.")

@client.command()
@commands.has_role(MODERATOR_ROLE_ID)
async def checkvc(ctx):
    "A manual commnad which eliminates users who are not in VC"

    counter = 0
    guild = client.get_guild(GUILD_ID)

    if guild is None:
        print("Guild not found!")
        return

    eliminated_role = guild.get_role(ELIMINATED_ROLE_ID)
    participant_role = guild.get_role(PARTICIPANT_ROLE_ID)
    moderator_role = guild.get_role(MODERATOR_ROLE_ID)

    if eliminated_role is None or participant_role is None:
        print("Role(s) not found!")
        return

    for member in guild.members:
        if member.bot:
            continue

        if not (member.voice and member.voice.channel):
            if eliminated_role not in member.roles and moderator_role not in member.roles:
                await member.remove_roles(participant_role)
                await member.add_roles(eliminated_role)
                counter += 1

    await ctx.channel.send(f"Eliminated {counter} users.")

@client.command(help = "Eliminates users in the specified channel\n\n"
    "Usage: $elim {color_name}\n"
    "Arguments: blue red")
@commands.has_role(MODERATOR_ROLE_ID)
async def elim(ctx, color):
    channel_id = None
    counter = 0

    guild = client.get_guild(GUILD_ID)
    moderator_role = guild.get_role(MODERATOR_ROLE_ID)

    if guild is None:
        print("Guild not found!")
        return
    
    if color == "red":
        channel_id = RED_CORNER_ID
    elif color == "blue":
        channel_id = BLUE_CORNER_ID
    else:
        await ctx.channel.send(f"Invalid color given: {color}")
        return
    
    global remove_role_enabled
    remove_role_enabled_temp_state = remove_role_enabled
    remove_role_enabled = False
    
    for member in guild.members:
        if member.bot:
            continue

        if ((member.voice and member.voice.channel.id == channel_id) and moderator_role not in member.roles):
            await member.move_to(None)
            counter += 1

    await ctx.channel.send(f"Removed {counter} people form {color} corner")

    remove_role_enabled = remove_role_enabled_temp_state

    command = client.get_command("checkvc")
    if command:
        await ctx.invoke(command)

@client.command(help = "Adds participant role to all members")
@commands.has_role(MODERATOR_ROLE_ID)
async def addparticipant(ctx):
    guild = client.get_guild(GUILD_ID)
    counter = 0

    if guild is None:
        print("Guild not found!")
        return
    
    participant_role = guild.get_role(PARTICIPANT_ROLE_ID)
    eliminated_role = guild.get_role(ELIMINATED_ROLE_ID)
    moderator_role = guild.get_role(MODERATOR_ROLE_ID)

    for member in guild.members:
        if member.bot:
            continue
        
        if (eliminated_role in member.roles) and moderator_role not in member.roles:
            await member.remove_roles(eliminated_role)

        if (participant_role not in member.roles) and moderator_role not in member.roles:
            await member.add_roles(participant_role)
            counter += 1

    await ctx.channel.send(f"Added {participant_role.name} to {counter} members.")

@client.command()
async def hello(ctx):
    "Sends a hello message"

    await ctx.channel.send("Hello!")

client.run(TOKEN)