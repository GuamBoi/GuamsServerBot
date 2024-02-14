#Import List
import discord
from discord.ext import commands
import random
import logging
import os
import asyncio

# Intents
intents = discord.Intents.all()
intents.voice_states = True

#Command Prefix
client = commands.Bot(command_prefix='!', intents=intents)

# Define Rolles
silenced_role_name = '!mute'  # Name of the role to assign

#Bot Boot Info / Playing Title
@client.event
async def on_ready():
    logging.info("Hello World! It's a Great Day to be Alive!")
    command_info = "Type '!commands' to see available commands."
    await client.change_presence(activity=discord.Game(name=command_info))

# Logging Configuration ???
logging.basicConfig(level=logging.INFO)

# Loading Random Messages Function
def load_random_messages(filepath):
    try:
        with open(filepath, 'r') as file:
            messages = file.readlines()
        return [message.strip() for message in messages]
    except FileNotFoundError:
        logging.error(f"File '{filepath}' not found.")
        return []

# Channel IDs
welcome_channel_id = 1036760459161911366
goodbye_channel_id = 1206374744719626361
suggestion_channel_id = 1197426979192971315
poll_channel_id = 1207205817640816670
ticket_category_id = 1036929287346999326 # Make sure to get the ID of a catagory, not a channel
invite_channel_id = 1036762745527357450

# Bot Path Info
base_path = '/home/guam/GuamsServerBot/'
message_folder = 'Bot Messages/'
ticket_messages = load_random_messages(os.path.join(base_path, message_folder, 'ticket_messages.txt'))
timer_messages = load_random_messages(os.path.join(base_path, message_folder, 'timer_messages.txt'))
ticket_logs_folder = '/home/guam/GuamsServerBot/Ticket Logs/'

# Embed Creator
async def send_embed(ctx_or_channel, title, description, color=discord.Color.red(), thumbnail=None, fields=None):
    if isinstance(ctx_or_channel, discord.TextChannel):
        # If ctx_or_channel is a TextChannel, set author to None
        author = None
    else:
        author = ctx_or_channel.author if hasattr(ctx_or_channel, 'author') else None
    
    embed = discord.Embed(title=title, description=description, color=color)
    if author:
        embed.set_author(name=author.name, icon_url=author.avatar.url)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if fields:
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
    if isinstance(ctx_or_channel, discord.TextChannel):
        # If ctx_or_channel is a TextChannel, send the embed directly
        return await ctx_or_channel.send(embed=embed)
    else:
        # Otherwise, send the embed to the author's channel
        return await ctx_or_channel.send(embed=embed)

# Read voice channel IDs from the file
with open('silenced_servers.txt', 'r') as f:
    target_voice_channel_ids = [line.strip() for line in f]

# Auto Give @Silenced roll when joining a Voice Channel
@client.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    silenced_role = discord.utils.get(guild.roles, name=silenced_role_name)

    if silenced_role is None:
        print(f'Role "{silenced_role_name}" not found')
        return

    for channel_id in target_voice_channel_ids:
        target_voice_channel = guild.get_channel(int(channel_id))

        if after.channel and after.channel.id == int(channel_id):
            await member.add_roles(silenced_role)
            print(f'Assigned {silenced_role_name} role to {member.display_name} in voice channel {after.channel.name}')
        elif before.channel and before.channel.id == int(channel_id):
            await member.remove_roles(silenced_role)
            print(f'Removed {silenced_role_name} role from {member.display_name} in voice channel {before.channel.name}')

# Welcome Messages
@client.event
async def on_member_join(member):
    welcome_message = random.choice(welcome_messages).format(member_mention=member.mention)
    welcome_channel = client.get_channel(welcome_channel_id)
    if welcome_channel:
        embed = discord.Embed(title="Welcome to the Server!", description=welcome_message, color=discord.Color.red())
        await welcome_channel.send(embed=embed)

# Goodbye Messages
@client.event
async def on_member_remove(member):
    goodbye_message = random.choice(goodbye_messages).format(member_mention=member.mention)
    goodbye_channel = client.get_channel(goodbye_channel_id)
    if goodbye_channel:
        embed = discord.Embed(title="Goodbye!", description=goodbye_message, color=discord.Color.red())
        await goodbye_channel.send(embed=embed)

# Event listener to handle reaction events
@client.event
async def on_raw_reaction_add(payload):
    # Check if the reaction event is from a guild (server)
    if payload.guild_id is None:
        return

    # Get the channel object based on the channel ID from the payload
    channel = client.get_channel(payload.channel_id)
    if not channel:
        return

    # Get the message object based on the message ID from the payload
    message = await channel.fetch_message(payload.message_id)
    if not message:
        return

    # Get the member object from the payload
    guild = client.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if not member:
        return

# - - - - - - - - - - - - - - !!!EDIT FROM HERE DOWN TO ADD REACTION ROLLS!!! - - - - - - - - - - - - - -


    # Check if the message is the one you sent and handle reactions accordingly 
    if message.author == client.user:
        # Check the reaction emoji and assign roles based on the emoji
        if payload.emoji.name == 'your_emoji_name':  # Replace 'your_emoji_name' with the actual emoji name
            role = discord.utils.get(guild.roles, name='Your Role Name')  # Replace 'Your Role Name' with the actual role name
            if role:
                await member.add_roles(role)

# - - - - - - - - - - - - - - !!!STOP EDITING FOR REACTION ROLLS!!! - - - - - - - - - - - - - -

# Event listener to handle reaction removal events
@client.event
async def on_raw_reaction_remove(payload):
    # Check if the reaction event is from a guild (server)
    if payload.guild_id is None:
        return

    # Get the channel object based on the channel ID from the payload
    channel = client.get_channel(payload.channel_id)
    if not channel:
        return

    # Get the message object based on the message ID from the payload
    message = await channel.fetch_message(payload.message_id)
    if not message:
        return

    # Get the member object from the payload
    guild = client.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if not member:
        return

# - - - - - - - - - - - - - - !!!EDIT FROM HERE DOWN TO ADD REACTION ROLLS!!! - - - - - - - - - - - - - -

    # Check if the message is the one you sent and handle reactions accordingly
    if message.author == client.user:
        # Check the reaction emoji and remove roles based on the emoji
        if payload.emoji.name == 'your_emoji_name':  # Replace 'your_emoji_name' with the actual emoji name
            role = discord.utils.get(guild.roles, name='Your Role Name')  # Replace 'Your Role Name' with the actual role name
            if role:
                await member.remove_roles(role)

# - - - - - - - - - - - - - - !!!STOP EDITING FOR REACTION ROLLS!!! - - - - - - - - - - - - - -


# Send a message as the Bot
@client.command()
async def send_bot_message(ctx, *, args):
    # Split the arguments into title and message
    split_args = args.split(':')

    if len(split_args) < 2:
        await ctx.send("Please provide both title and message separated by a colon (':').")
        return

    title = split_args[0].strip()
    message = ':'.join(split_args[1:]).strip()

    # Create an embed with the provided title and message
    embed = discord.Embed(title=title, description=message, color=discord.Color.red())
    
    # Send the embed to the same channel where the command was invoked
    await ctx.send(embed=embed)
    
    # Delete the original command message
    await ctx.message.delete()

# Add Reaction Emojis to Messages
@client.command()
async def add_reactions(ctx, message_id: int, *emojis):
    # Fetch the message object based on the provided message ID
    try:
        message = await ctx.channel.fetch_message(message_id)
    except discord.NotFound:
        await ctx.send("Message not found.")
        return

    # Add reactions to the message
    for emoji in emojis:
        try:
            await message.add_reaction(emoji)
        except discord.HTTPException:
            await ctx.send(f"Failed to add reaction for emoji: {emoji}")
    await ctx.message.delete()

#Command List
@client.command()
async def commands(ctx):
    embed = discord.Embed(title="Server Commands", color=discord.Color.red())
    embed.add_field(name=":ballot_box: !suggest <your suggestion>", value="Creates a Server Suggestion", inline=False)
    embed.add_field(name=":bar_chart: !poll <poll question>", value="Creates a Server Poll", inline=False)
    embed.add_field(name=":tickets: !ticket", value="Creates a New Private Ticket with the Server Mods", inline=False)
    embed.add_field(name=":game_die: !dice_commands", value="Lists all the dice commands", inline=False)
    embed.add_field(name=":incoming_envelope: !invite", value="Sends an invite to the General chat for the game you're playing", inline=False)
    embed.add_field(name=":coin: !coinflip", value="Flips a coin", inline=False)
    embed.add_field(name=":alarm_clock: !timer <HH:MM>", value="Set a timer. Make sure your time amount matches the code format!", inline=False)
    embed.add_field(name=":loud_sound: !voice_commands", value="Lists all the Voice Chat Commands", inline=False)
    await ctx.send(embed=embed)
    await ctx.message.delete()

# Voice Command List
@client.command()
async def voice_commands(ctx):
    embed = discord.Embed(title="Voice Chat Commands", color=discord.Color.red())
    embed.add_field(name=":mute: !mute", value="Mutes you and all members in the voice chat with you", inline=False)
    embed.add_field(name=":sound: !unmute", value="Unmutes you and all members in the voice chat with you", inline=False)
    await ctx.send(embed=embed)
    await ctx.message.delete()

# Dice Command List
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
    await ctx.message.delete()

# Dice Message Paths
D4_messages = load_random_messages(os.path.join(base_path, message_folder, 'D4_messages.txt'))
D6_messages = load_random_messages(os.path.join(base_path, message_folder, 'D6_messages.txt'))
D8_messages = load_random_messages(os.path.join(base_path, message_folder, 'D8_messages.txt'))
D10_messages = load_random_messages(os.path.join(base_path, message_folder, 'D10_messages.txt'))
D12_messages = load_random_messages(os.path.join(base_path, message_folder, 'D12_messages.txt'))
D20_messages = load_random_messages(os.path.join(base_path, message_folder, 'D20_messages.txt'))
coinflip_messages = load_random_messages(os.path.join(base_path, message_folder, 'coinflip.txt'))
welcome_messages = load_random_messages(os.path.join(base_path, message_folder, 'welcome_messages.txt'))
goodbye_messages = load_random_messages(os.path.join(base_path, message_folder, 'goodbye_messages.txt'))

# Dice Commands
@client.command()
async def d4(ctx):
    if D4_messages:
        response = random.choice(D4_messages)
        await send_embed(ctx, "D4 Roll", f"🎲 {response}")
    else:
        await send_embed(ctx, "D4 Roll", "No messages available for rolling a D4.")
    await ctx.message.delete()

# Roll Command
@client.command()
async def roll(ctx):
    if D6_messages:
        response = random.choice(D6_messages)
        await send_embed(ctx, "D6 Roll", f"🎲 {response}")
    else:
        await send_embed(ctx, "D6 Roll", "No messages available for rolling a D6.")
    await ctx.message.delete()

# D8 Command
@client.command()
async def d8(ctx):
    if D8_messages:
        response = random.choice(D8_messages)
        await send_embed(ctx, "D8 Roll", f"🎲 {response}")
    else:
        await send_embed(ctx, "D8 Roll", "No messages available for rolling a D8.")
    await ctx.message.delete()

# D10 Command
@client.command()
async def d10(ctx):
    if D10_messages:
        response = random.choice(D10_messages)
        await send_embed(ctx, "D10 Roll", f"🎲 {response}")
    else:
        await send_embed(ctx, "D10 Roll", "No messages available for rolling a D10.")
    await ctx.message.delete()

# D12 Command
@client.command()
async def d12(ctx):
    if D12_messages:
        response = random.choice(D12_messages)
        await send_embed(ctx, "D12 Roll", f"🎲 {response}")
    else:
        await send_embed(ctx, "D12 Roll", "No messages available for rolling a D12.")
    await ctx.message.delete()

# D20 Command
@client.command()
async def d20(ctx):
    if D20_messages:
        response = random.choice(D20_messages)
        await send_embed(ctx, "D20 Roll", f"🎲 {response}")
    else:
        await send_embed(ctx, "D20 Roll", "No messages available for rolling a D20.")
    await ctx.message.delete()

# Coinflip Command
@client.command()
async def coinflip(ctx):
    if coinflip_messages:
        response = random.choice(coinflip_messages)
        await send_embed(ctx, "Coin Flip", f":coin: {response}")
    else:
        await send_embed(ctx, "Coin Flip", "No messages available for coin flipping.")
    await ctx.message.delete()

# Create Suggestions Command
@client.command()
async def suggest(ctx, *, question):
    suggestion_channel = client.get_channel(suggestion_channel_id)
    
    if suggestion_channel:
        embed = discord.Embed(title="Server Suggestion", description=question, color=discord.Color.red())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.add_field(name="Everyone can vote!", value="👍 Yes    👎 No", inline=False)
        message = await suggestion_channel.send(embed=embed)
        await message.add_reaction('👍')
        await message.add_reaction('👎')
        await ctx.message.delete()
    else:
        await ctx.send("Suggestion channel not found.")

# Create Polls Command
@client.command()
async def poll(ctx, *, question):
    poll_channel = client.get_channel(poll_channel_id)
    
    if poll_channel:
        embed = discord.Embed(title="Server Poll", description=question, color=discord.Color.red())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.add_field(name="Everyone can vote!", value="👍 Yes    👎 No", inline=False)
        message = await poll_channel.send(embed=embed)
        await message.add_reaction('👍')
        await message.add_reaction('👎')
        await ctx.message.delete()
    else:
        await ctx.send("Poll channel not found.")

# Create Tickets Command
@client.command()
async def ticket(ctx):
    # Get the ticket category or return if it doesn't exist
    category = ctx.guild.get_channel(ticket_category_id)
    if not category or not isinstance(category, discord.CategoryChannel):
        await ctx.send("Ticket category not found.")
        return

    # Check if the user already has an open ticket
    for channel in category.channels:
        if channel.name.startswith("Ticket-") and channel.topic == str(ctx.author.id):
            await ctx.author.send("You already have an open ticket.")
            return

    # Define permissions for the ticket channel
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }

    # Define the name for the ticket channel
    ticket_channel_name = f"Ticket-{ctx.author.name.replace(' ', '-')}"

    # Create the ticket channel under the specified category with the defined permissions
    ticket_channel = await category.create_text_channel(ticket_channel_name, overwrites=overwrites)
    ticket_channel.topic = str(ctx.author.id)

    # Send a message to the ticket channel if there are ticket messages available
    if ticket_messages:
        ticket_message = random.choice(ticket_messages)
        await ticket_channel.send(ticket_message.format(user_mention=ctx.author.mention))

    await ctx.message.delete()

# Delete Ticket Command
@client.command()
async def delete_ticket(ctx):
    if isinstance(ctx.channel, discord.TextChannel) and ctx.channel.category.name == "Tickets":
        await ctx.channel.delete()
    else:
        await ctx.send("This command can only be used in a ticket channel.")

# Log Tocket Command
@client.command()
async def log_ticket(ctx):
    if isinstance(ctx.channel, discord.TextChannel) and ctx.channel.category.name == "Tickets":
        if not os.path.exists(ticket_logs_folder):
            os.makedirs(ticket_logs_folder)

        filename = f"{ctx.channel.name}.txt"
        filepath = os.path.join(ticket_logs_folder, filename)

        messages = []
        async for message in ctx.channel.history(limit=None):
            messages.append(f"{message.created_at} - {message.author.display_name}: {message.content}")

        messages.reverse()

        with open(filepath, 'w') as file:
            file.write("\n".join(messages))

        await ctx.send(f"This conversation has been logged by a mod.")
    else:
        await ctx.send("This command can only be used in a ticket channel.")
    await ctx.message.delete()

# Timer Command
@client.command()
async def timer(ctx, time_duration):
    try:
        hours, minutes = map(int, time_duration.split(':'))
        time_in_seconds = (hours * 3600) + (minutes * 60)

        embed = discord.Embed(title="Timer Set", color=discord.Color.green())
        embed.add_field(name="Duration", value=f"{hours} hours and {minutes} minutes", inline=False)
        confirmation_message = await ctx.send(embed=embed)
        await ctx.message.delete()

        await asyncio.sleep(time_in_seconds)

        if timer_messages:
            timer_message = random.choice(timer_messages)
            user_mention = ctx.author.mention
            timer_message = timer_message.replace("{user_mention}", user_mention)
            await send_embed(ctx, "Timer Notification", timer_message, color=discord.Color.red())

        await confirmation_message.delete()
    except ValueError:
        await ctx.send("Invalid time duration format. Please provide the time in the format 'HH:MM'.")
        
timer_messages_filepath = os.path.join(base_path, message_folder, 'timer_messages.txt')
with open(timer_messages_filepath, 'r') as file:
    timer_messages = [line.strip() for line in file]

# Mute Command
@client.command()
async def mute(ctx):
    silenced_role = discord.utils.get(ctx.guild.roles, name="!mute")
    if silenced_role is None:
        await ctx.send("The '!mute' role does not exist.")
        return

    if ctx.author.voice is None:
        await ctx.send("You need to be in a voice channel to use this command.")
        return

    voice_channel = ctx.author.voice.channel

    members_to_tag = []

    for member in voice_channel.members:
        if silenced_role in member.roles:
            await member.edit(mute=True)
            members_to_tag.append(member)

    if members_to_tag:
        # Load messages from mute_messages.txt
        mute_messages = load_random_messages(os.path.join(base_path, message_folder, 'mute_messages.txt'))

        if mute_messages:
            message = random.choice(mute_messages)
            # Replace placeholders with role mention
            message = message.replace("{role}", silenced_role.mention)
            embed = discord.Embed(title=":mute: Mute", description=message, color=discord.Color.red())
            await ctx.send(embed=embed)
            await ctx.message.delete()

# Unmute command
@client.command()
async def unmute(ctx):
    silenced_role = discord.utils.get(ctx.guild.roles, name="!mute")
    if silenced_role is None:
        await ctx.send("The '!mute' role does not exist.")
        return

    if ctx.author.voice is None:
        await ctx.send("You need to be in a voice channel to use this command.")
        return

    voice_channel = ctx.author.voice.channel

    members_to_tag = []

    for member in voice_channel.members:
        if silenced_role in member.roles:
            await member.edit(mute=False)
            members_to_tag.append(member)

    if members_to_tag:  # Checking if there are any members to tag
        # Load messages from unmute_messages.txt
        unmute_messages = load_random_messages(os.path.join(base_path, message_folder, 'unmute_messages.txt'))

        if unmute_messages:
            message = random.choice(unmute_messages)
            # Replace placeholders with role mention
            message = message.replace("{role}", silenced_role.mention)
            embed = discord.Embed(title=":lound_sound: Unmute", description=message, color=discord.Color.green())
            await ctx.send(embed=embed)
    await ctx.message.delete()

# Game Invite Command
@client.command()
async def invite(ctx):
    if ctx.author.voice is not None:  # Check if the author is in a voice channel
        voice_channel = ctx.author.voice.channel  # Get the voice channel the user is in
        game = ctx.author.activity.name if ctx.author.activity else None
        if game:
            role = discord.utils.get(ctx.guild.roles, name=game)
            if role:
                # Fetch the invite channel using the ID
                invite_channel = ctx.guild.get_channel(invite_channel_id)
                
                if invite_channel:
                    # Load a random message from 'game_messages.txt'
                    message_filepath = os.path.join(base_path, message_folder, 'game_messages.txt')
                    random_message = random.choice(load_random_messages(message_filepath))  # Choose a random message from the file

                    # Format the message with actual values
                    formatted_message = random_message.format(
                        user_mention=ctx.author.mention,  # Mention the user who initiated the invite
                        game_name=game,  # The name of the game the user is playing
                        voice_channel_mention=voice_channel.mention,  # Mention the voice channel
                        role_mention=role.mention  # Mention the role associated with the game
                    )

                    await send_embed(invite_channel, "Game Invitation", formatted_message, color=discord.Color.green())
                else:
                    await ctx.send("Invite channel not found.")
            else:
                await ctx.send(f"No role found for {game}.")
        else:
            await ctx.send("You need to be playing a game to use this command.")
    else:
        await ctx.send("You need to be in a voice channel to use this command.")
    await ctx.message.delete()

# Bot Token
client.run('YOUR_DISCORD_BOT_TOKEN')
