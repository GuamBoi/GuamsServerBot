import discord  # Importing the Discord API library
from discord.ext import commands  # Importing commands extension from discord
import random  # Importing random module for generating random numbers
import logging  # Importing logging module for logging messages
import os  # Import os module for file path operations

# Configure logging
logging.basicConfig(level=logging.INFO)  # Setting up logging configuration

# Function to load random messages from a text file
def load_random_messages(filepath):
    try:
        with open(filepath, 'r') as file:  # Open the file in read mode
            messages = file.readlines()  # Read all lines from the file
        return [message.strip() for message in messages]  # Strip newline characters from messages and return
    except FileNotFoundError:
        logging.error(f"File '{filepath}' not found.")  # Log error message if file not found
        return []  # Return empty list if file not found

# Define file paths
base_path = '/home/kali/GuamsServerBot/'  # Define base path for the bot files
message_folder = 'Bot Messages/'  # Define folder containing message files

# Load random messages from the D6 and D20 text files
D4_messages = load_random_messages(os.path.join(base_path, message_folder, 'D4_messages.txt'))  # Load D4 messages
D6_messages = load_random_messages(os.path.join(base_path, message_folder, 'D6_messages.txt'))  # Load D6 messages
D8_messages = load_random_messages(os.path.join(base_path, message_folder, 'D8_messages.txt'))  # Load D8 messages
D10_messages = load_random_messages(os.path.join(base_path, message_folder, 'D10_messages.txt'))  # Load D10 messages
D12_messages = load_random_messages(os.path.join(base_path, message_folder, 'D12_messages.txt'))  # Load D12 messages
D20_messages = load_random_messages(os.path.join(base_path, message_folder, 'D20_messages.txt'))  # Load D20 messages
coinflip_messages = load_random_messages(os.path.join(base_path, message_folder, 'coinflip.txt'))  # Load coinflip messages

# Discord bot client with all intents enabled
intents = discord.Intents.all()  # Enable all intents for the bot
client = commands.Bot(command_prefix='!', intents=intents)  # Create a bot instance with specified command prefix and intents

# Command: !commands
@client.command()
async def commands(ctx):
    # Create an embed to display commands and descriptions
    embed = discord.Embed(title="Server Commands Anyone Can Use", color=0xff0000)  # Create embed with title and color
    embed.add_field(name="!dice_commands", value="lists all the commands to roll different dice", inline=False)  # Add field for dice commands
    embed.add_field(name="!coinflip", value="Flips a coin", inline=False)  # Add field for coinflip command
    await ctx.send(embed=embed)  # Send the embed

# Command: !dice_commands
@client.command()
async def dice_commands(ctx):
    # Create an embed to display commands and descriptions
    embed = discord.Embed(title="Dice Commands", color=0xff0000)  # Create embed with title and color
    embed.add_field(name="!d4", value="Rolls a d4 dice", inline=False)  # Adds field for d4 command
    embed.add_field(name="!roll", value="Rolls a normal D6 dice", inline=False)  # Adds field for roll command
    embed.add_field(name="!d8", value="Rolls a d8 dice", inline=False)  # Adds field for d8 command
    embed.add_field(name="!d10", value="Rolls a d10 dice", inline=False)  # Adds field for d10 command
    embed.add_field(name="!d12", value="Rolls a d12 dice", inline=False)  # Adds field for d12 command
    embed.add_field(name="!d20", value="Rolls a D20 dice", inline=False)  # Adds field for d20 command
    await ctx.send(embed=embed)  # Send the embed

# Command: !d4
@client.command()
async def d4(ctx):
    if D4_messages:  # If there are messages for D4
        response = random.choice(D4_messages)  # Choose a random message from D4 messages
        await ctx.send(response)  # Send the chosen message
    else:
        await ctx.send("No messages available for rolling a D4.")  # Send message if no D4 messages available

# Command: !roll
@client.command()
async def roll(ctx):
    if D6_messages:  # If there are messages for D6
        response = random.choice(D6_messages)  # Choose a random message from D6 messages
        await ctx.send(response)  # Send the chosen message
    else:
        await ctx.send("No messages available for rolling a D6.")  # Send message if no D6 messages available

# Command: !d8
@client.command()
async def d8(ctx):
    if D8_messages:  # If there are messages for D8
        response = random.choice(D8_messages)  # Choose a random message from D8 messages
        await ctx.send(response)  # Send the chosen message
    else:
        await ctx.send("No messages available for rolling a D8.")  # Send message if no D8 messages available

# Command: !d10
@client.command()
async def d10(ctx):
    if D10_messages:  # If there are messages for D10
        response = random.choice(D10_messages)  # Choose a random message from D10 messages
        await ctx.send(response)  # Send the chosen message
    else:
        await ctx.send("No messages available for rolling a D10.")  # Send message if no D10 messages available

# Command: !d12
@client.command()
async def d12(ctx):
    if D12_messages:  # If there are messages for D12
        response = random.choice(D12_messages)  # Choose a random message from D12 messages
        await ctx.send(response)  # Send the chosen message
    else:
        await ctx.send("No messages available for rolling a D12.")  # Send message if no D12 messages available

# Command: !d20
@client.command()
async def d20(ctx):
    if D20_messages:  # If there are messages for D20
        response = random.choice(D20_messages)  # Choose a random message from D20 messages
        await ctx.send(response)  # Send the chosen message
    else:
        await ctx.send("No messages available for rolling a D20.")  # Send message if no D20 messages available

# Command: !coinflip
@client.command()
async def coinflip(ctx):
    if coinflip_messages:  # If there are messages for coinflip
        response = random.choice(coinflip_messages)  # Choose a random message from coinflip messages
        await ctx.send(response)  # Send the chosen message
    else:
        await ctx.send("No messages available for coin flipping.")  # Send message if no coinflip messages available

# Set bot's presence
@client.event
async def on_ready():
    logging.info('Bot is ready.')  # Log message indicating bot is ready
    # Create a custom status with command information
    command_info = "Type '!commands' to see available commands."  # Define the status message
    await client.change_presence(activity=discord.Game(name=command_info))  # Set bot's presence with the status message

# Run the Discord bot with your token
client.run('YOUR_DISCORD_BOT_TOKEN')  # Run the bot with your token. Make sure to replace YOUR_DISCORD_BOT_TOKEN with your token. 
