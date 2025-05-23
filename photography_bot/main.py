import os
import sqlite3
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive

def user_exists(user_id):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('SELECT 1 FROM messages WHERE userid = ?', (user_id,))
    result = c.fetchone()
    conn.close()

    return result is not None

load_dotenv()
keep_alive()

conn = sqlite3.connect('messages.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        userid INTEGER NOT NULL,
        messageid INTEGER NOT NULL
    )
''')

conn.commit()
conn.close()

TOKEN = os.getenv("DISCORD_TOKEN")

SUBMISSIONS_CHANNEL = 1371015663983788073
MODERATOR_ROLE = 1371013866212950127
GUILD_ID = 1371013559571583050

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True 

client = commands.Bot(command_prefix="$", intents=intents)

@client.tree.command(name="deletedb", 
                     description="Delete all entries in the database",
                     guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_role(MODERATOR_ROLE)
async def deletedb(interaction: discord.Interaction):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('DELETE FROM messages')
    conn.commit()
    conn.close()
    await interaction.response.send_message("🗑️ All entries deleted.", ephemeral=True)

@client.command()
async def ping(ctx):
    await ctx.channel.send("Pong!")

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

    print("Commands before sync:")
    for cmd in client.tree.get_commands():
        print(cmd.name)

    try:
        guild = discord.Object(id=GUILD_ID)

        synced = await client.tree.sync(guild = guild)
        print(f"Synced {len(synced)} command(s)")

    except Exception as e:
        print(f"Sync error: {e}")

@client.event
async def on_message(message):

    isMedia = False

    if client.user == message.author:
        return
    
    if message.channel.id != SUBMISSIONS_CHANNEL:
        await client.process_commands(message)
        return
    
    #Don't add DB entry for mods
    guild = message.guild
    if guild is None:
        return  

    member = guild.get_member(message.author.id)
    if member is None:
        return 

    if any(role.id == MODERATOR_ROLE for role in member.roles):
        return
    
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
    
    for attachment in message.attachments:
        if attachment.filename.lower().endswith(image_extensions):
            isMedia = True

    if not isMedia:
        await message.delete()
        
        await message.channel.send("You are not allowed to send anything other than images here.", delete_after = 10)
        
        await client.process_commands(message)
        return

    if user_exists(message.author.id):
        await message.delete()
        await message.channel.send("You have already posted your submission. If you want to change / edit your submission, delete your original submission and create a new one.", delete_after = 10)
        
        await client.process_commands(message)
        return
    
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages (username, userid, messageid) VALUES (?, ?, ?)',
            (str(message.author), message.author.id, message.id))
    conn.commit()
    conn.close()

    await client.process_commands(message)

@client.event
async def on_message_delete(message):

    isMedia = False
    
    if client.user == message.author:
        return
    
    if message.channel.id != SUBMISSIONS_CHANNEL:
        return
    
    #Don't add DB entry for mods
    guild = message.guild
    if guild is None:
        return  

    member = guild.get_member(message.author.id)
    if member is None:
        return 

    if any(role.id == MODERATOR_ROLE for role in member.roles):
        return
    
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
    
    for attachment in message.attachments:
        if attachment.filename.lower().endswith(image_extensions):
            isMedia = True

    if isMedia:
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()
        c.execute('DELETE FROM messages WHERE messageid = ?', (message.id,))
        conn.commit()
        conn.close()

client.run(TOKEN)