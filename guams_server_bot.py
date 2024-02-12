# Importing necessary libraries
import discord
from discord.ext import commands
import random
import logging
import os

# Setting up logging configuration
logging.basicConfig(level=logging.INFO)

# Function to load random messages from a file
def load_random_messages(filepath):
    try:
        with open(filepath, 'r') as file:
            messages = file.readlines()
        return [message.strip() for message in messages]
    except FileNotFoundError:
        logging.error(f"File '{filepath}' not found.")
        return []

# Setting base path and message folder
base_path = '/home/kali/GuamsServerBot/'  # Specify your base path here
message_folder = 'Bot Messages/'

# Loading messages for different dice types
D4_messages = load_random_messages(os.path.join(base_path, message_folder, 'D4_messages.txt'))
D6_messages = load_random_messages(os.path.join(base_path, message_folder, 'D6_messages.txt'))
D8_messages = load_random_messages(os.path.join(base_path, message_folder, 'D8_messages.txt'))
D10_messages = load_random_messages(os.path.join(base_path, message_folder, 'D10_messages.txt'))
D12_messages = load_random_messages(os.path.join(base_path, message_folder, 'D12_messages.txt'))
D20_messages = load_random_messages(os.path.join(base_path, message_folder, 'D20_messages.txt'))
coinflip_messages = load_random_messages(os.path.join(base_path, message_folder, 'coinflip.txt'))
welcome_messages = load_random_messages(os.path.join(base_path, message_folder, 'welcome_messages.txt'))
goodbye_messages = load_random_messages(os.path.join(base_path, message_folder, 'goodbye_messages.txt'))

# Setting up Discord intents
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

# Asynchronous function to send embeds
async def send_embed(ctx, title, description, color=discord.Color.red(), thumbnail=None, fields=None):
    embed = discord.Embed(title=title, description=description, color=color)
    if ctx.author.avatar:
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if fields:
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
    return await ctx.send(embed=embed)

# Event handler for bot's readiness
@client.event
async def on_ready():
    logging.info('Bot is ready.')
    command_info = "Type '!commands' to see available commands."
    await client.change_presence(activity=discord.Game(name=command_info))

# Event handler for new member joining
@client.event
async def on_member_join(member):
    welcome_channel_id = 1036760459161911366 # Replace with your "Welcome" channel ID
    welcome_message = random.choice(welcome_messages).format(member_mention=member.mention)
    welcome_channel = client.get_channel(welcome_channel_id)
    if welcome_channel:
        embed = discord.Embed(title="Welcome to the Server!", description=welcome_message, color=discord.Color.red())
        await welcome_channel.send(embed=embed)

# Event handler for member leaving
@client.event
async def on_member_remove(member):
    goodbye_channel_id = 1206374744719626361 # Replace with your "Goodbye" channel ID
    goodbye_message = random.choice(goodbye_messages).format(member_mention=member.mention)
    goodbye_channel = client.get_channel(goodbye_channel_id)
    if goodbye_channel:
        embed = discord.Embed(title="Goodbye!", description=goodbye_message, color=discord.Color.red())
        await goodbye_channel.send(embed=embed)

# Command to display available server commands
@client.command()
async def commands(ctx):
    embed = discord.Embed(title="Server Commands", color=discord.Color.red())
    embed.add_field(name=":game_die: !dice_commands", value="Lists all the dice commands", inline=False)
    embed.add_field(name=":coin: !coinflip", value="Flips a coin", inline=False)
    embed.add_field(name=":ballot_box: !suggest", value="Creates a suggestion", inline=False)  # Updated command name here
    await ctx.send(embed=embed)

# Command to display available dice rolling commands
@client.command()
async def dice_commands(ctx):
    embed = discord.Embed(title="Dice Commands", color=discord.Color.red())
    embed.add_field(name=":game_die: !d4", value="Rolls a D4 Dice", inline=False)
    embed.add_field(name=":game_die: !roll", value="Rolls a normal D6 dice", inline=False)
    embed.add_field(name=":game_die: !d8", value="Rolls a D8 dice", inline=False)
    embed.add_field(name=":game_die: !d10", value="Rolls a D10 dice", inline=False)
    embed.add_field(name=":game_die: !d12", value="Rolls a D12 dice", inline=False)
    embed.add_field(name=":game_die: !d20", value="Rolls a D20 dice", inline=False)
    await ctx.send(embed=embed)

# Command to create a suggestion
@client.command()
async def suggest(ctx, *, question):
    embed = discord.Embed(title="Server Suggestion", description=question, color=discord.Color.red())
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.add_field(name="Everyone can vote!", value="👍 Yes    👎 No", inline=False)
    message = await send_embed(ctx, "Suggestion", question, thumbnail="https://example.com/poll_thumbnail.png", fields=[("Everyone can Vote!", "👍 Yes    👎 No", False)])
    await message.add_reaction('👍')
    await message.add_reaction('👎')

# Command to roll a D4 dice
@client.command()
async def d4(ctx):
    if D4_messages:
        response = random.choice(D4_messages)
        await send_embed(ctx, "D4 Roll", f"🎲 {response}")
    else:
        await send_embed(ctx, "D4 Roll", "No messages available for rolling a D4.")

# Command to roll a normal D6 dice
@client.command()
async def roll(ctx):
    if D6_messages:
        response = random.choice(D6_messages)
        await send_embed(ctx, "D6 Roll", f"🎲 {response}")
    else:
        await send_embed(ctx, "D6 Roll", "No messages available for rolling a D6.")

# Command to roll a D8 dice
@client.command()
async def d8(ctx):
    if D8_messages:
        response = random.choice(D8_messages)
        await send_embed(ctx, "D8 Roll", f"🎲 {response}")
    else:
        await send_embed(ctx, "D8 Roll", "No messages available for rolling a D8.")

# Command to roll a D10 dice
@client.command()
async def d10(ctx):
    if D10_messages:
        response = random.choice(D10_messages)
        await send_embed(ctx, "D10 Roll", f"🎲 {response}")
    else:
        await send_embed(ctx, "D10 Roll", "No messages available for rolling a D10.")

# Command to roll a D12 dice
@client.command()
async def d12(ctx):
    if D12_messages:
        response = random.choice(D12_messages)
        await send_embed(ctx, "D12 Roll", f"🎲 {response}")
    else:
        await send_embed(ctx, "D12 Roll", "No messages available for rolling a D12.")

# Command to roll a D20 dice
@client.command()
async def d20(ctx):
    if D20_messages:
        response = random.choice(D20_messages)
        await send_embed(ctx, "D20 Roll", f"🎲 {response}")
    else:
        await send_embed(ctx, "D20 Roll", "No messages available for rolling a D20.")

# Command to flip a coin
@client.command()
async def coinflip(ctx):
    if coinflip_messages:
        response = random.choice(coinflip_messages)
        await send_embed(ctx, "Coin Flip", f":coin: {response}")
    else:
        await send_embed(ctx, "Coin Flip", "No messages available for coin flipping.")

# Run the Discord bot with your token
client.run('YOUR_DISCORD_BOT_TOKEN')  # Run the bot with your token. Make sure to replace YOUR_DISCORD_BOT_TOKEN with your token.
