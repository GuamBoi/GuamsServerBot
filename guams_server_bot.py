# Importing necessary libraries
import discord  # Import the Discord library
from discord.ext import commands  # Import commands extension for Discord
import random  # Import the random module for generating random numbers
import logging  # Import logging module for logging messages
import os  # Import os module for interacting with the operating system

# Setting up logging configuration
logging.basicConfig(level=logging.INFO)  # Configure logging to display INFO level messages

# Function to load random messages from a file
def load_random_messages(filepath):
    try:
        with open(filepath, 'r') as file:  # Open the file in read mode
            messages = file.readlines()  # Read lines from the file
        return [message.strip() for message in messages]  # Return a list of messages with leading/trailing whitespace removed
    except FileNotFoundError:
        logging.error(f"File '{filepath}' not found.")  # Log an error if the file is not found
        return []  # Return an empty list if the file is not found

# Setting base path and message folder
base_path = '/home/guam/GuamsServerBot/'  # Specify the base path where the bot files are located
message_folder = 'Bot Messages/'  # Specify the folder containing bot messages

# Loading messages for different dice types
D4_messages = load_random_messages(os.path.join(base_path, message_folder, 'D4_messages.txt'))  # Load messages for a 4-sided dice
D6_messages = load_random_messages(os.path.join(base_path, message_folder, 'D6_messages.txt'))  # Load messages for a 6-sided dice
D8_messages = load_random_messages(os.path.join(base_path, message_folder, 'D8_messages.txt'))  # Load messages for an 8-sided dice
D10_messages = load_random_messages(os.path.join(base_path, message_folder, 'D10_messages.txt'))  # Load messages for a 10-sided dice
D12_messages = load_random_messages(os.path.join(base_path, message_folder, 'D12_messages.txt'))  # Load messages for a 12-sided dice
D20_messages = load_random_messages(os.path.join(base_path, message_folder, 'D20_messages.txt'))  # Load messages for a 20-sided dice
coinflip_messages = load_random_messages(os.path.join(base_path, message_folder, 'coinflip.txt'))  # Load messages for a coin flip
welcome_messages = load_random_messages(os.path.join(base_path, message_folder, 'welcome_messages.txt'))  # Load welcome messages for new members
goodbye_messages = load_random_messages(os.path.join(base_path, message_folder, 'goodbye_messages.txt'))  # Load goodbye messages for leaving members

# Setting up Discord intents
intents = discord.Intents.all()  # Create a Discord Intents object with all intents enabled
client = commands.Bot(command_prefix='!', intents=intents)  # Create a Bot instance with specified command prefix and intents

# Asynchronous function to send embeds
async def send_embed(ctx, title, description, color=discord.Color.red(), thumbnail=None, fields=None):
    embed = discord.Embed(title=title, description=description, color=color)  # Create an embed with specified title, description, and color
    if ctx.author.avatar:  # Check if author has an avatar
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)  # Set author's name and avatar as embed author
    if thumbnail:  # Check if thumbnail URL is provided
        embed.set_thumbnail(url=thumbnail)  # Set thumbnail for embed
    if fields:  # Check if fields are provided
        for name, value, inline in fields:  # Iterate over fields
            embed.add_field(name=name, value=value, inline=inline)  # Add each field to the embed
    return await ctx.send(embed=embed)  # Send the embed message to the channel

# Event handler for bot's readiness
@client.event
async def on_ready():
    logging.info('Hello World! It is a great day to be Alive!')  # Log a message indicating the bot is ready
    command_info = "Type '!commands' to see available commands."  # Information about available commands
    await client.change_presence(activity=discord.Game(name=command_info))  # Set bot's presence to the command information

# Event handler for new member joining
@client.event
async def on_member_join(member):
    welcome_channel_id = 1036760459161911366  # Replace with your "Welcome" channel ID
    welcome_message = random.choice(welcome_messages).format(member_mention=member.mention)  # Choose a random welcome message and mention the new member
    welcome_channel = client.get_channel(welcome_channel_id)  # Get the welcome channel
    if welcome_channel:  # Check if welcome channel exists
        embed = discord.Embed(title="Welcome to the Server!", description=welcome_message, color=discord.Color.red())  # Create a welcome embed
        await welcome_channel.send(embed=embed)  # Send the welcome message to the channel

# Event handler for member leaving
@client.event
async def on_member_remove(member):
    goodbye_channel_id = 1206374744719626361  # Replace with your "Goodbye" channel ID
    goodbye_message = random.choice(goodbye_messages).format(member_mention=member.mention)  # Choose a random goodbye message and mention the leaving member
    goodbye_channel = client.get_channel(goodbye_channel_id)  # Get the goodbye channel
    if goodbye_channel:  # Check if goodbye channel exists
        embed = discord.Embed(title="Goodbye!", description=goodbye_message, color=discord.Color.red())  # Create a goodbye embed
        await goodbye_channel.send(embed=embed)  # Send the goodbye message to the channel

# Command to display available server commands
@client.command()  # Decorator to define a command
async def commands(ctx):  # Command function to display available server commands
    embed = discord.Embed(title="Server Commands", color=discord.Color.red())  # Create an embed for server commands
    embed.add_field(name=":game_die: !dice_commands", value="Lists all the dice commands", inline=False)  # Add field for dice commands
    embed.add_field(name=":coin: !coinflip", value="Flips a coin", inline=False)  # Add field for coin flip command
    embed.add_field(name=":ballot_box: !suggest", value="Creates a Server Suggestion", inline=False)  # Add field for suggestion command
    embed.add_field(name=":bar_chart: !poll", value="Creates a Server Poll", inline=False)  # Add field for poll command
    embed.add_field(name=":tickets: !ticket", value="Creates a New Private Ticket with the Server Mods", inline=False)  # Add field for ticket command
    await ctx.send(embed=embed)  # Send the embed message with server commands

# Command to display available dice rolling commands
@client.command()  # Decorator to define a command
async def dice_commands(ctx):  # Command function to display available dice rolling commands
    embed = discord.Embed(title="Dice Commands", color=discord.Color.red())  # Create an embed for dice commands
    embed.add_field(name=":game_die: !d4", value="Rolls a D4 Dice", inline=False)  # Add field for D4 command
    embed.add_field(name=":game_die: !roll", value="Rolls a normal D6 dice", inline=False)  # Add field for roll command
    embed.add_field(name=":game_die: !d8", value="Rolls a D8 dice", inline=False)  # Add field for D8 command
    embed.add_field(name=":game_die: !d10", value="Rolls a D10 dice", inline=False)  # Add field for D10 command
    embed.add_field(name=":game_die: !d12", value="Rolls a D12 dice", inline=False)  # Add field for D12 command
    embed.add_field(name=":game_die: !d20", value="Rolls a D20 dice", inline=False)  # Add field for D20 command
    await ctx.send(embed=embed)  # Send the embed message with dice commands

# Command to create a New Server Suggestion
@client.command()  # Decorator to define a command
async def suggest(ctx, *, question):  # Command function to create a suggestion
    embed = discord.Embed(title="Server Suggestion", description=question, color=discord.Color.red())  # Create a suggestion embed
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)  # Set author's name and avatar
    embed.add_field(name="Everyone can vote!", value="👍 Yes    👎 No", inline=False)  # Add voting options
    message = await send_embed(ctx, "Server Suggestion", question, thumbnail="https://images.emojiterra.com/twitter/v13.1/512px/1f5f3.png", fields=[("Everyone can Vote!", "👍 Yes    👎 No", False)])  # Send the suggestion as an embed
    await message.add_reaction('👍')  # Add thumbs-up reaction
    await message.add_reaction('👎')  # Add thumbs-down reaction

# Command to create a New Server Poll
@client.command()  # Decorator to define a command
async def poll(ctx, *, question):  # Command function to create a new server poll
    embed = discord.Embed(title="Server Suggestion", description=question, color=discord.Color.red())  # Create a poll embed
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)  # Set author's name and avatar
    embed.add_field(name="Everyone can vote!", value="👍 Yes    👎 No", inline=False)  # Add voting options
    message = await send_embed(ctx, "Server Poll", question, thumbnail="https://images.emojiterra.com/google/noto-emoji/unicode-15.1/color/1024px/1f4ca.png", fields=[("Everyone can Vote!", "👍 Yes    👎 No", False)])  # Send the poll as an embed
    await message.add_reaction('👍')  # Add thumbs-up reaction
    await message.add_reaction('👎')  # Add thumbs-down reaction

# Load ticket messages
ticket_messages = load_random_messages(os.path.join(base_path, message_folder, 'ticket_messages.txt'))

# Command to create a new ticket
@client.command()  # Decorator to define a command
async def ticket(ctx):  # Command function to create a new ticket
    category = discord.utils.get(ctx.guild.categories, name="Tickets")  # Get the category named "Tickets"
    if not category:  # If "Tickets" category doesn't exist
        category = await ctx.guild.create_category("Tickets")  # Create "Tickets" category

    # Check if the user already has an open ticket
    for channel in category.channels:  # Iterate over channels in the category
        if channel.name.startswith("Ticket-") and channel.topic == str(ctx.author.id):  # If channel is a ticket and topic matches user ID
            await ctx.author.send("You already have an open ticket.")  # Send a message to the user
            return

    # Generate ticket channel name
    ticket_channel_name = f"Ticket-{ctx.author.name.replace(' ', '-')}"

    overwrites = {  # Define permission overwrites for the ticket channel
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }

    ticket_channel = await category.create_text_channel(ticket_channel_name, overwrites=overwrites)  # Create the ticket channel
    ticket_channel.topic = str(ctx.author.id)  # Set the topic to user's ID to track their ticket

    # Send a random ticket message to the new ticket channel
    if ticket_messages:  # If ticket messages exist
        ticket_message = random.choice(ticket_messages)  # Choose a random ticket message
        await ticket_channel.send(ticket_message.format(user_mention=ctx.author.mention))  # Send the ticket message

    await ctx.message.delete()  # Delete the command message

# Command to delete a ticket
@client.command()  # Decorator to define a command
async def delete_ticket(ctx):  # Command function to delete a ticket
    if isinstance(ctx.channel, discord.TextChannel) and ctx.channel.category.name == "Tickets":  # If command is run in a ticket channel
        await ctx.channel.delete()  # Delete the ticket channel
    else:
        await ctx.send("This command can only be used in a ticket channel.")  # Send a message if command is not used in a ticket channel

ticket_logs_folder = '/home/guam/GuamsServerBot/Ticket Logs/'  # Specify the folder to store ticket logs

# Command to log a ticket conversation
@client.command()  # Decorator to define a command
async def log_ticket(ctx):  # Command function to log a ticket conversation
    if isinstance(ctx.channel, discord.TextChannel) and ctx.channel.category.name == "Tickets":  # If command is run in a ticket channel
        # Create the Ticket Logs folder if it doesn't exist
        if not os.path.exists(ticket_logs_folder):  # If Ticket Logs folder doesn't exist
            os.makedirs(ticket_logs_folder)  # Create Ticket Logs folder

        # Generate the filename
        filename = f"{ctx.channel.name}.txt"  # Generate filename based on channel name
        filepath = os.path.join(ticket_logs_folder, filename)  # Generate full file path

        # Get the entire conversation from the ticket channel
        messages = []  # Initialize a list to store messages
        async for message in ctx.channel.history(limit=None):  # Iterate over channel history
            messages.append(f"{message.created_at} - {message.author.display_name}: {message.content}")  # Append message to the list

        # Reverse the order of messages
        messages.reverse()  # Reverse the list of messages

        # Write the conversation to the file
        with open(filepath, 'w') as file:  # Open file in write mode
            file.write("\n".join(messages))  # Write messages to the file

        await ctx.send(f"This conversation has been logged for further review.")  # Send a confirmation message
    else:
        await ctx.send("This command can only be used in a ticket channel.")  # Send a message if command is not used in a ticket channel

# Command functions for rolling dice are defined similarly and omitted for brevity

# Run the Discord bot with your token
client.run('YOUR_DISCORD_BOT_TOKEN')  # Run the bot with your token. Make sure to replace YOUR_DISCORD_BOT_TOKEN with your token.
