import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks

load_dotenv()  # Loads variables from .env into environment

TOKEN = os.getenv("DISCORD_TOKEN")

GUILD_ID = 1176896434587570269
ELIMINATED_ROLE_ID = 1370727530289692834
PARTICIPANT_ROLE_ID = 1370729934992969828
RED_CORNER_ID = 1176896434587570273
BLUE_CORNER_ID = 1370738478731755560
MODERATOR_ROLE_ID = 1370752012668375150

commands_list = ['checkvc', 'elim', 'addparticipant', 'hello']

intents = discord.Intents.default()
intents.message_content = True 
intents.voice_states = True  
intents.members = True 

client = commands.Bot(command_prefix="$", intents=intents)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))  

@client.command()
@commands.has_role(MODERATOR_ROLE_ID)
async def checkvc(ctx):
    """Eliminates users who are not in VC"""

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
        
    for member in guild.members:
        if member.bot:
            continue

        if ((member.voice and member.voice.channel.id == channel_id) and moderator_role not in member.roles):
            await member.move_to(None)
            counter += 1

    await ctx.channel.send(f"Removed {counter} people form {color} corner")

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