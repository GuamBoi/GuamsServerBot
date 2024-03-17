#Import List
import discord
from discord.ext import commands

# Other Imports
from command_explanations import commands_data
from discord.ext.commands import command
from discord.ext.commands import Cog
from discord import FFmpegPCMAudio
from collections import deque
import random
import logging
import os
import asyncio
import collections

# Initialize the bot with intents
intents = discord.Intents.all()
intents.voice_states = True
intents.messages = True
intents.reactions = True

#Command Prefix
client = commands.Bot(command_prefix='!', intents=intents)

# Define Rolles
silenced_role_name = '!mute'  # Name of the role to assign
moderator_role_name = 'Moderator'  # Name of the role for moderators
friend_role_name = 'Friend'  # Name of the role for friends

#Bot Boot Info / Playing Title
@client.event
async def on_ready():
    logging.info('Hello World! It\'s a Great Day to be Alive!')
    command_info = "Type '!commands' to see available commands."
    await client.change_presence(activity=discord.Game(name=command_info))
    await client.add_cog(FriendCommands(client))
    await client.add_cog(Moderation(client))
    
# Logging Configuration ???
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

### RANDOM MESSAGE FUNCTION ###

# Loading Random Messages Function
def load_random_messages(filepath):
    try:
        with open(filepath, 'r') as file:
            messages = file.readlines()

        return [message.strip() for message in messages]
    except FileNotFoundError:
        logging.error(f"File '{filepath}' not found.")
        return []

### PATHING AND REFRENCE INFO ###

available_commands = ['!commands', '!suggest', '!poll', '!ticket', '!invite', '!timer', '!coinflip', '!dice_commands', '!d4', '!roll', '!d8', '!d10', '!d12', '!d20', '!voice_commands', '!mute', '!unmute', '!roll_commands', '!friend_commands', 'invite_friends', '!poll_friends', '!mod_commands', '!delete_ticket', '!log_ticket', '!timeout', '!kick', '!ban']

# Version Numbers
bot_version = '1.0 BETA'
chat_bot_version = '1.0 BETA'

# Channel IDs
welcome_channel_id = 1036760459161911366
goodbye_channel_id = 1206374744719626361
suggestion_channel_id = 1197426979192971315
approved_channel_id = 1208292523379003462
declined_channel_id = 1208315165616115774
poll_channel_id = 1207205817640816670
result_channel_id = 1208639938854264852
ticket_category_id = 1036929287346999326 # Should Match
command_help_category_id = 1036929287346999326 # Should Match
invite_channel_id = 1036762745527357450
invite_friend_channel_id = 980706628540170282
poll_friends_channel_id = 980706628540170282

# Bot Path Info
base_path = '/home/guam/GuamsServerBot/'
ticket_logs_folder = '/home/guam/GuamsServerBot/Ticket Logs/'
message_folder = 'Bot Messages/'
ticket_messages = load_random_messages(os.path.join(base_path, message_folder, 'ticket_messages.txt'))
timer_messages = load_random_messages(os.path.join(base_path, message_folder, 'timer_messages.txt'))
welcome_messages = load_random_messages(os.path.join(base_path, message_folder, 'welcome_messages.txt'))
goodbye_messages = load_random_messages(os.path.join(base_path, message_folder, 'goodbye_messages.txt'))
D4_messages = load_random_messages(os.path.join(base_path, message_folder, 'D4_messages.txt'))
D6_messages = load_random_messages(os.path.join(base_path, message_folder, 'D6_messages.txt'))
D8_messages = load_random_messages(os.path.join(base_path, message_folder, 'D8_messages.txt'))
D10_messages = load_random_messages(os.path.join(base_path, message_folder, 'D10_messages.txt'))
D12_messages = load_random_messages(os.path.join(base_path, message_folder, 'D12_messages.txt'))
D20_messages = load_random_messages(os.path.join(base_path, message_folder, 'D20_messages.txt'))
coinflip_messages = load_random_messages(os.path.join(base_path, message_folder, 'coinflip.txt'))

### FUNCTIONS ###

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

# Complex Embed Creator
async def send_complex_embed(ctx_or_channel, title, description, color=discord.Color.red(), thumbnail=None, fields=None):
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
        for value, inline in fields:
            embed.add_field(name='\u200b', value=value, inline=inline)
    if isinstance(ctx_or_channel, discord.TextChannel):
        # If ctx_or_channel is a TextChannel, send the embed directly
        return await ctx_or_channel.send(embed=embed)
    else:
        # Otherwise, send the embed to the author's channel
        return await ctx_or_channel.send(embed=embed)

# Read voice channel IDs from the file
with open('silenced_servers.txt', 'r') as f:
    target_voice_channel_ids = [line.strip() for line in f]

### AUTO COMMANDS ###

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
        elif before.channel and before.channel.id == int(channel_id):
            await member.remove_roles(silenced_role)

### WELCOME AND GOODBYE MESSAGES ###

# Welcome Messages
@client.event
async def on_member_join(member):
    welcome_message = random.choice(welcome_messages).format(member_mention=member.mention)
    welcome_channel = client.get_channel(welcome_channel_id)
    if welcome_channel:
        embed = discord.Embed(title=":wave: Welcome to the Server!", description=welcome_message, color=discord.Color.red())
        await welcome_channel.send(embed=embed)

# Goodbye Messages
@client.event
async def on_member_remove(member):
    goodbye_message = random.choice(goodbye_messages).format(member_mention=member.mention)
    goodbye_channel = client.get_channel(goodbye_channel_id)
    if goodbye_channel:
        embed = discord.Embed(title=":wave: Goodbye!", description=goodbye_message, color=discord.Color.red())
        await goodbye_channel.send(embed=embed)

### COMMAND LISTS - FRIEND AND MOD LISTS ###

# !commands
@client.command()
async def commands(ctx):
    embed = discord.Embed(title="Server Commands", color=discord.Color.red())
    embed.add_field(name=":ballot_box: !suggest <your suggestion>", value="Creates a Server Suggestion", inline=False)
    embed.add_field(name=":bar_chart: !poll <poll question>", value="Creates a Server Poll", inline=False)
    embed.add_field(name=":tickets: !ticket", value="Creates a New Private Ticket with the Server Mods", inline=False)
    embed.add_field(name=":envelope: !invite", value="Sends an invite to the General chat for the game you're playing", inline=False)
    embed.add_field(name=":alarm_clock: !timer <HH:MM>", value="Set a timer. Make sure your time amount matches the code format!", inline=False)
    embed.add_field(name=":coin: !coinflip", value="Flips a coin", inline=False)
    embed.add_field(name=":game_die: !dice_commands", value="Lists all the dice commands", inline=False)
    embed.add_field(name=":loud_sound: !voice_commands", value="Lists all the Voice Chat Commands", inline=False)
    embed.add_field(name=":crown: !roll_commands", value="A list of Roll Specific Commands", inline=False)
    embed.add_field(name=":video_game: !game_commands", value="Lists all the Channel Game Commands", inline=False)
    embed.add_field(name=":sos: !help_commands", value="Opens the Command Help Menu", inline=False)
    embed.set_footer(text=f"Bot Version: {bot_version}")
    await ctx.send(embed=embed)
    await ctx.message.delete()

# !voice_commands
@client.command()
async def voice_commands(ctx):
    embed = discord.Embed(title="Voice Chat Commands", color=discord.Color.red())
    embed.add_field(name=":mute: !mute", value="Mutes you and all members in the voice chat with you", inline=False)
    embed.add_field(name=":sound: !unmute", value="Unmutes you and all members in the voice chat with you", inline=False)
    await ctx.send(embed=embed)
    await ctx.message.delete()

# !dice_commands
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

# Sepcial Roll Commands
@client.command()
async def roll_commands(ctx):
    embed = discord.Embed(title="Roll Specific Commands", color=discord.Color.red())
    embed.add_field(name=":crown: !friend_commands", value="Lists the Special @Friend Commands", inline=False)
    embed.add_field(name=":flag_gu: !mod_commands", value="Lists the Special @Moderator Commands", inline=False)
    await ctx.send(embed=embed)
    await ctx.message.delete()
    
# !game_commands
@client.command()
async def game_commands(ctx):
    embed = discord.Embed(title="Server Game Commands", color=discord.Color.red())
    embed.add_field(name=":abcd: !wordle", value="Starts Your own Wordle Game", inline=False)
    embed.add_field(name=":grey_question: !guess <word>", value="Makes a Guess to YOUR wordle Game", inline=False)
    embed.add_field(name=":fire: !wordle_streaks", value="Shows all Current Player Streaks.", inline=False)
    embed.add_field(name=":red_circle: !connect4 <@opponents_username>", value="Starts a Connect4 Game Between You and the Tagged User", inline=False)
    await ctx.send(embed=embed)
    await ctx.message.delete()

### HELP COMMANDS ###
@client.command()
async def help_commands(ctx):
    embed = discord.Embed(title="Help Commands", color=discord.Color.red())
    embed.add_field(name=":speech_balloon: !command_help", value="Opens a Private chat between you and the Server Bot. There he can answer all of your questions by using the following commands", inline=False)
    embed.add_field(name=":speaking_head: !explain <!command_you_need_help_with>", value="Explains in depth how to use commands.", inline=False)
    embed.add_field(name=":octagonal_sign: !end", value="Ends your conversation with the Server Bot", inline=False)
    embed.set_footer(text=f"Chat Bot Version: {chat_bot_version}")
    await ctx.send(embed=embed)
    await ctx.message.delete()

# Help Command List

@client.command()
async def command_help(ctx):
    
    # Get the command help category or return if it doesn't exist
    category = ctx.guild.get_channel(command_help_category_id)
    if not category or not isinstance(category, discord.CategoryChannel):
        await ctx.send("Command help category not found.")
        return

    # Define permissions for the command help channel
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }

    # Define the name for the command help channel
    channel_name = f"Command-Help-{ctx.author.name.replace(' ', '-')}"

    # Create the command help channel under the specified category with the defined permissions
    command_help_channel = await category.create_text_channel(channel_name, overwrites=overwrites)

    # Define the path to the help messages file
    help_messages_file = os.path.join(message_folder, 'help_messages.txt')

    # Load random help message from the file
    help_messages = load_random_messages(help_messages_file)

    if help_messages:
        # Select a random message from loaded help messages
        help_message = random.choice(help_messages)

        # Replace {user_mention} with actual user mention
        help_message = help_message.replace('{user_mention}', ctx.author.mention)

        # Creating an embed for the help message
        embed = discord.Embed(title=":flag_gu: Command Assistant", description=help_message, color=discord.Color.blue())
        embed.set_footer(text=f"Chat Bot Version: {chat_bot_version}")

        # Send the embed to the command help channel
        await command_help_channel.send(embed=embed)
    else:
        await command_help_channel.send("It seems the Command Assistant is having Technical Difficulties at the moment. Please ask for Assistance in the `#💬-general-chat`")

    await ctx.message.delete()

# Explain Command
@client.command()
async def explain(ctx, command: str):
    if command in commands_data:
        details = commands_data[command]
        embed = discord.Embed(title=details.get('title', 'Command Details'), color=discord.Color.blue())
        
        # Add fields to the embed if they exist in the details dictionary
        if 'command' in details:
            embed.add_field(name="The command:", value=details['command'], inline=False)
        if 'description' in details:
            embed.add_field(name=":scroll: Command Description:", value=details['description'], inline=False)
        if 'usage' in details:
            embed.add_field(name=":question: Who can use it?", value=details['usage'], inline=False)
        if 'channels' in details:
            embed.add_field(name=":speech_balloon: What Channels does it work in?", value=details['channels'], inline=False)
        if 'example' in details:
            embed.add_field(name="Code Example:", value=details['example'], inline=False)
        
        embed.set_footer(text=f"Chat Bot Version: {chat_bot_version}")
        
        await ctx.send(embed=embed)
    else:
        await ctx.send("Command not found.")

# End Command
@client.command()
async def end(ctx):
    # Get the name of the command help channel to delete
    channel_name = f"command-help-{ctx.author.name.replace(' ', '-')}"

    # Find the command help channel
    command_help_channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)

    # Check if the channel exists and if the user has permissions to delete it
    if command_help_channel and command_help_channel.permissions_for(ctx.author).manage_channels:
        await command_help_channel.delete()
    else:
        await ctx.send("Hmm.. I cant seem to find a command-help channel for you... If this is a mistake please notify a Moderator.")
    await ctx.message.delete()

### DICE COMMANDS ###

# D4 Command
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

### TICKET COMMANDS ###

# Create Tickets Command
@client.command()
async def ticket(ctx):
    # Get the ticket category or return if it doesn't exist
    category = ctx.guild.get_channel(ticket_category_id)
    if not category or not isinstance(category, discord.CategoryChannel):
        await ctx.send("Ticket category not found.")
        return

    # Fetch the Moderator role
    moderator_role = discord.utils.get(ctx.guild.roles, name="Moderator")
    if not moderator_role:
        await ctx.send("Moderator role not found.")
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
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        moderator_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)  # Add Moderator role permissions
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

### VOICE CHANNEL COMMANDS ###

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
            embed = discord.Embed(title=":loud_sound: Unmute", description=message, color=discord.Color.green())
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

                    await send_embed(invite_channel, ":video_game: Game Invitation", formatted_message, color=discord.Color.green())
                else:
                    await ctx.send("Invite channel not found.")
            else:
                await ctx.send(f"No role found for {game}.")
        else:
            await ctx.send("You need to be playing a game to use this command.")
    else:
        await ctx.send("You need to be in a voice channel to use this command.")
    await ctx.message.delete()
    
### FRIEND COMMANDS ###

# Define a class for Friend commands

from discord.ext import commands

class FriendCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Friend Command List
    @commands.command()
    @commands.has_role(friend_role_name)
    async def friend_commands(self, ctx):
        embed = discord.Embed(title="Special Friend Commands", color=discord.Color.red())
        embed.add_field(name=":incoming_envelope: !invite_friends", value="Invites users to play the game your playing in the #friend-chat", inline=False)
        embed.set_footer(text=f"Bot Version: {bot_version}")
        await ctx.send(embed=embed)
        await ctx.message.delete()

    # Game Invite Command
    @commands.command()
    @commands.has_role(friend_role_name)  # Restrict the command to members with the 'Friends' role
    async def invite_friends(self, ctx):
        if ctx.author.voice is not None:
            voice_channel = ctx.author.voice.channel
            game = ctx.author.activity.name if ctx.author.activity else None
            if game:
                role = discord.utils.get(ctx.guild.roles, name=game)
                if role:
                    invite_channel = ctx.guild.get_channel(invite_friend_channel_id)
                    if invite_channel:
                        message_filepath = os.path.join(base_path, message_folder, 'game_messages.txt')
                        random_message = random.choice(load_random_messages(message_filepath))

                        formatted_message = random_message.format(
                            user_mention=ctx.author.mention,
                            game_name=game,
                            voice_channel_mention=voice_channel.mention,
                            role_mention=role.mention
                        )

                        await send_embed(invite_channel, ":joystick: Game Invitation", formatted_message, color=discord.Color.green())
                    else:
                        await ctx.send("Invite channel not found.")
                else:
                    await ctx.send(f"No role found for {game}.")
            else:
                await ctx.send("You need to be playing a game to use this command.")
        else:
            await ctx.send("You need to be in a voice channel to use this command.")
        await ctx.message.delete()

### MODERATOR COMMANDS ###

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def send_embed_message(self, ctx, title, description, color):
        embed = discord.Embed(title=title, description=description, color=color)
        await ctx.send(embed=embed)

    async def send_error_message(self, ctx, error_message):
        await self.send_embed_message(ctx, ":x: Error", error_message, discord.Color.red())
        await ctx.message.delete()

    async def check_permissions(self, ctx):
        moderator_role_name = "Moderator"  # Replace with the actual name of your moderator role
        moderator_role = discord.utils.get(ctx.guild.roles, name=moderator_role_name)
        if moderator_role in ctx.author.roles:
            return True
        else:
            await self.send_error_message(ctx, "You don't have permission to use this command. If you think this is an error, please message one of the Moderators.")
            return False
        await ctx.message.delete()

    # Mod Command List
    @commands.command()
    async def mod_commands(self, ctx):
        if await self.check_permissions(ctx):
            embed = discord.Embed(title="Special Moderator Commands", color=discord.Color.red())
            embed.add_field(name=":wastebasket: !delete_ticket", value="Deletes the ticket you are responding to.", inline=False)
            embed.add_field(name=":scroll: !log_ticket", value="Logs the ticket you are responding to.", inline=False)
            embed.add_field(name=":broom: !clear", value="Clears the entire chat the command was used in.", inline=False)
            embed.add_field(name=":hourglass: !timeout <username> <time in seconds> <reason>", value="Puts a user in 'timeout' for a set duration of time.", inline=False)
            embed.add_field(name="!:boot: kick <username> <reason>", value="Kicks a user from the server", inline=False)
            embed.add_field(name=":no_entry_sign: !ban <username> <reason>", value="Bans a user from the server", inline=False)
            embed.set_footer(text=f"Bot Version: {bot_version}")  # Make sure bot_version is defined
            await ctx.send(embed=embed)
        await ctx.message.delete()

    # Clear Command
    @commands.command()
    async def clear(self, ctx):
        if await self.check_permissions(ctx):
            # Check if the command was used in a guild (server)
            if ctx.guild:
                # Create an embed for the confirmation message
                embed = discord.Embed(
                    title="Clear Messages Confirmation",
                    description="Are you sure you want to clear all messages in this channel?",
                    color=discord.Color.blue()
                )
                embed.set_footer(text=f"Requested by {ctx.author.display_name}")

                # Send the embed as the confirmation message
                confirmation_message = await ctx.send(embed=embed)

                # Add reaction options
                await confirmation_message.add_reaction('✅')  # Check mark
                await confirmation_message.add_reaction('❌')  # Cross mark

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ['✅', '❌']

                try:
                    reaction, _ = await self.client.wait_for('reaction_add', timeout=30.0, check=check)

                    if str(reaction.emoji) == '✅':
                        # Clear all messages in the channel
                        await ctx.channel.purge()
                    else:
                        # Cancel the action
                        embed = discord.Embed(
                            description="Clear operation canceled.",
                            color=discord.Color.red()
                        )
                        await ctx.send(embed=embed)
                except asyncio.TimeoutError:
                    # Timeout if the user doesn't react within 30 seconds
                    embed = discord.Embed(
                        description="Clear operation timed out. No messages were cleared.",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=embed)

                # Delete the confirmation message (if it still exists)
                try:
                    await confirmation_message.delete()
                except discord.errors.NotFound:
                    pass  # Confirmation message was already deleted
                except Exception as e:
                    print(f"An error occurred while deleting the confirmation message: {e}")
            else:
                # If the command was used in a private message (DM), send an error message
                embed = discord.Embed(
                    description="This command can only be used in a server channel.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)

    # Log Ticket Command
    @commands.command()
    async def log_ticket(self, ctx):
        if await self.check_permissions(ctx):
            if isinstance(ctx.channel, discord.TextChannel) and ctx.channel.category_id == ticket_category_id:  # Make sure ticket_category_id is defined
                if not os.path.exists(ticket_logs_folder):  # Make sure ticket_logs_folder is defined
                    os.makedirs(ticket_logs_folder)

                filename = f"{ctx.channel.name}.txt"
                filepath = os.path.join(ticket_logs_folder, filename)

                messages = []
                async for message in ctx.channel.history(limit=None):
                    messages.append(f"{message.created_at} - {message.author.display_name}: {message.content}")

                messages.reverse()

                with open(filepath, 'w') as file:
                    file.write("\n".join(messages))

                embed = discord.Embed(title=":scroll: Conversation Logged", description="This conversation has been logged by a mod.", color=discord.Color.green())
                await ctx.send(embed=embed)
            else:
                await self.send_error_message(ctx, "This command can only be used in a ticket channel.")
            await ctx.message.delete()

    # Delete Ticket Command
    @commands.command()
    async def delete_ticket(self, ctx):
        if await self.check_permissions(ctx):
            if isinstance(ctx.channel, discord.TextChannel) and ctx.channel.category_id == ticket_category_id:  # Make sure ticket_category_id is defined
                try:
                    await ctx.channel.delete()
                except discord.NotFound:
                    pass  # Channel already deleted, no need to delete it again
            else:
                await self.send_error_message(ctx, "This command can only be used in a ticket channel.")
    
    # Timeout Command
    @commands.command()
    async def timeout(self, ctx, member: discord.Member, duration: int, *, reason="No reason provided."):
        if await self.check_permissions(ctx):
            try:
                await member.edit(mute=True)
                embed = discord.Embed(title=":hourglass: Member Timeout", description=f"{member.mention} has been timed out for {duration} seconds.", color=discord.Color.red())
                embed.add_field(name="Reason", value=reason)
                await ctx.send(embed=embed)
                await asyncio.sleep(duration)
                await member.edit(mute=False)
            except discord.Forbidden:
                await self.send_error_message(ctx, "I don't have the necessary permissions to timeout members.")
            except Exception as e:
                await self.send_error_message(ctx, f"An error occurred: {e}")
            await ctx.message.delete()

    # Kick Command
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided."):
        if await self.check_permissions(ctx):
            try:
                await member.kick(reason=reason)
                embed = discord.Embed(title=":boot: Member Kicked", description=f"{member.mention} has been kicked.", color=discord.Color.red())
                embed.add_field(name="Reason", value=reason)
                await ctx.send(embed=embed)
            except discord.Forbidden:
                await self.send_error_message(ctx, "I don't have the necessary permissions to kick members.")
            except Exception as e:
                await self.send_error_message(ctx, f"An error occurred: {e}")
            await ctx.message.delete()

    # Ban Command
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided."):
        if await self.check_permissions(ctx):
            try:
                await member.ban(reason=reason)
                embed = discord.Embed(title=":no_entry_sign: Member Banned", description=f"{member.mention} has been banned.", color=discord.Color.red())
                embed.add_field(name="Reason", value=reason)
                await ctx.send(embed=embed)
            except discord.Forbidden:
                await self.send_error_message(ctx, "I don't have the necessary permissions to ban members.")
            except Exception as e:
                await self.send_error_message(ctx, f"An error occurred: {e}")
            await ctx.message.delete()

### SERVER CUSTOMIZATION COMMANDS ###

role_options = {
    "color": {
        "message": "Server Color Selection",
        "description": "Color Key:",
        "note": "Pick 1 color at a time.",
        "options": {
            "🔴": {"name": "`Red`", "role_id": 1036871222987857930},
            "🟡": {"name": "`Yellow`", "role_id": 1036871950464729128},
            "🟢": {"name": "`Green`", "role_id": 1036872280103452782},
            "🔵": {"name": "`Blue`", "role_id": 1036872513654894602},
            "🟣": {"name": "`Purple`", "role_id": 1036872927469117450}
        }
    },

    "game": {
        "message": "Game Selection",
        "description": "Server Game Options:",
        "note": "Select all the games you want to be apart of!",
        "options": {
            "🚀": {"name": "`Lethal Company`", "role_id": 1193313172376015058},
            "🧙‍♀️": {"name": "`Baldur's Gate 3`", "role_id": 1193312758721159208},
            "🕰️": {"name": "`Blood on The Clocktower`", "role_id": 1154988413871730688},
            "🐔": {"name": "`Clash of Clans (COC)`", "role_id": 1184233316195516466},
            "🌀": {"name": "`Splitgate`", "role_id": 1193340302782648510},
            "💀": {"name": "`Dead By Daylight`", "role_id": 1202837366474149898}
        }
    },

    "free_game": {
        "message": "Free Game and Update Channels",
        "description": "Channel Options:",
        "note": "Game updates only support 🚀 and 🧙‍♀️.",
        "options": {
            "🆓": {"name": "`Free Games`", "role_id": 1197633716256776243},
            "🔔": {"name": "`Game Updates`", "role_id": 1197621406175866981}
        }
    }
}

message_ids = {
    "color_message_id": 1208782052317470791,
    "game_message_id": 1208782064208449647,
    "free_game_message_id": 1208782075633868900
}

# Define the customize_server command
@client.command()
async def customize_server(ctx):
    for role_type, data in role_options.items():
        await send_role_selection_message(ctx, role_type, data)

# Define the function to send role selection messages
async def send_role_selection_message(ctx, role_type, data, footer_text="React with the emojis to make your selection!"):
    color = get_embed_color(role_type)
    embed = discord.Embed(title=data["message"], color=color)
    embed.add_field(name="Note:", value=data['note'], inline=False)
    embed.add_field(name=data["description"], value="\n".join([f"{emoji} - {option['name']}" for emoji, option in data["options"].items()]), inline=False)
    embed.set_footer(text=footer_text)
    message = await ctx.send(embed=embed)

    # Store the message ID
    message_ids[f"{role_type}_message_id"] = message.id
    
    # Add reaction emojis
    for emoji in data["options"].keys():
        await message.add_reaction(emoji)

# Function to get embed color based on role type
def get_embed_color(role_type):
    if role_type == "color":
        return discord.Color.red()
    elif role_type == "game":
        return discord.Color.blue()
    elif role_type == "free_game":
        return discord.Color.yellow()
        
# Define the event handler for raw reaction adds
@client.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return
    
    await handle_raw_reaction(payload)

# Define the event handler for raw reaction removals
@client.event
async def on_raw_reaction_remove(payload):
    await handle_raw_reaction(payload)

async def handle_raw_reaction(payload):
    guild = client.get_guild(payload.guild_id)
    if guild is None:
        return
    if payload.member is None:
        member = await guild.fetch_member(payload.user_id)
    else:
        member = payload.member
    if member.bot:
        return
    for role_type, data in role_options.items():
        if payload.message_id == message_ids.get(f"{role_type}_message_id"):

            emoji_name = payload.emoji.name if payload.emoji.name else str(payload.emoji)

            role_id = data["options"].get(emoji_name, {}).get("role_id")

            if role_id:
                role = discord.utils.get(guild.roles, id=role_id)
                if role:
                    if payload.event_type == 'REACTION_ADD':
                        await member.add_roles(role)
                        
                    elif payload.event_type == 'REACTION_REMOVE':
                        await member.remove_roles(role)
                        
### ECONOMY AND GAMES ###

# Economy variables
game_states = {}
user_scores = {}
user_streaks = {}
players = {}

# Function to save economy values to a file
def save_economy_values():
    with open("economy_values.txt", "w") as file:
        for player_id, player in players.items():
            file.write(f"{player_id},{player.collection_points},{player.emeralds},{player.rubies}\n")

# Function to load economy values from a file
def load_economy_values():
    try:
        with open("economy_values.txt", "r") as file:
            for line in file:
                player_id, cp, emeralds, rubies = line.strip().split(",")
                player = players.get(int(player_id))
                if player:
                    player.collection_points = int(cp)
                    player.emeralds = int(emeralds)
                    player.rubies = int(rubies)
    except FileNotFoundError:
        # If the file doesn't exist, no data needs to be loaded
        pass
        
# Function to award 1 Collection Point to the winner
def award_collection_point(player_id):
    player = players.get(player_id)
    if player:
        player.collection_points += 1  # Award 1 Collection Point
        user_streaks[player_id] = user_streaks.get(player_id, 0) + 1  # Increment player's streak
        save_economy_values()  # Save updated economy values
        
# Inventory command
@client.command()
async def inventory(ctx):
    player = players.get(ctx.author.id)
    if player:
        embed = discord.Embed(title=f"{ctx.author.display_name}'s Inventory", color=discord.Color.blue())
        embed.add_field(name="Collection Points", value=player.collection_points, inline=False)
        embed.add_field(name="Emeralds", value=player.emeralds, inline=False)
        embed.add_field(name="Rubies", value=player.rubies, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("You don't have an inventory yet. Play some games to earn items!")

# Additional commands for buying emeralds and rubies
@client.command()
async def buy_emerald(ctx):
    player = players.get(ctx.author.id)
    if player and player.collection_points >= 2:
        player.collection_points -= 2
        player.emeralds += 2  # Add 2 emeralds to the player's inventory
        await ctx.send("You have successfully purchased 2 emeralds!")
        save_economy_values()  # Save updated economy values
    else:
        await ctx.send("You don't have enough collection points to buy emeralds.")

@client.command()
async def buy_ruby(ctx):
    player = players.get(ctx.author.id)
    if player and player.emeralds >= 2:
        player.emeralds -= 2  # Remove 2 emeralds from the player's inventory
        player.rubies += 1  # Add 1 ruby to the player's inventory
        await ctx.send("You have successfully purchased 1 ruby!")
        save_economy_values()  # Save updated economy values
    else:
        await ctx.send("You don't have enough emeralds to buy a ruby.")

## WORDLE CODE ##

# Wordle variables
WordleEmpty = "<:WordleEmpty:1209440570376855572>"
WordleGray = "<:WordleGray:1209457732831281153>"
WordleGreen = "<:WordleGreen:1209457589881012284>"
WordleYellow = "<:WordleYellow:1209457878746923029>"

# Read word list
def read_word_list():
    with open("wordle_words.txt", "r") as file:
        words = file.read().splitlines()
    return words

# Generate secret word
def generate_secret_word():
    words = read_word_list()
    return random.choice(words)

# Calculates guess feedback
def get_feedback(guess, secret_word):
    feedback = []
    guess = guess.lower()  # Convert guess to lowercase
    secret_word = secret_word.lower()  # Convert secret word to lowercase
    
    # Count the occurrences of each letter in the guess and the secret word
    guess_counts = collections.Counter(guess)
    secret_counts = collections.Counter(secret_word)
    
    # Iterate through each letter in the guess
    for i in range(len(guess)):
        if guess[i] == secret_word[i]:
            # If the guessed letter matches the corresponding letter in the secret word
            feedback.append("correct")
            # Decrement the count of the guessed letter in both guess and secret word
            guess_counts[guess[i]] -= 1
            secret_counts[guess[i]] -= 1
        else:
            # If the guessed letter does not match the corresponding letter in the secret word
            feedback.append("incorrect")

    # Check for correct letters in the wrong positions
    for i in range(len(guess)):
        if guess[i] != secret_word[i] and guess[i] in secret_word:
            # If the guessed letter exists in the secret word but is not in the correct position
            if secret_counts[guess[i]] > 0:
                feedback[i] = "misplaced"
                secret_counts[guess[i]] -= 1

    return feedback

# Wordle command
@client.command()
async def wordle(ctx):
    global game_states

    if ctx.author.id in game_states:
        embed = discord.Embed(title="Error", description="You already have an active game. Finish it before starting a new one.")
        error_message = await ctx.send(embed=embed)
        await asyncio.sleep(15)
        await error_message.delete()
        return

    secret_word = generate_secret_word()
    game_states[ctx.author.id] = {'secret_word': secret_word, 'attempts': 6, 'guesses': []}
    game_embed = discord.Embed(title="Wordle", description=f"Guess the 5-letter word by typing `!guess <word>`.")
    game_message = await ctx.send(embed=game_embed)
    game_states[ctx.author.id]['game_message'] = game_message

# Guess command
@client.command()
async def guess(ctx, guess_word: str):
    global game_states
    global user_scores
    global user_streaks

    if ctx.author.id not in game_states:
        embed = discord.Embed(title="Error", description="Please start a game using !wordle command first.")
        error_message = await ctx.send(embed=embed)
        await asyncio.sleep(15)
        await delete_message_safely(ctx, error_message)
        return

    game_state = game_states[ctx.author.id]

    guess = guess_word.lower().strip()  # Strip leading/trailing whitespace
    if len(guess) != 5 or not guess.isalpha():
        embed = discord.Embed(title="Error", description="Invalid guess. Please enter a 5-letter word.")
        error_message = await ctx.send(embed=embed)
        await asyncio.sleep(15)
        await delete_message_safely(ctx, error_message)
        return

    game_state['guesses'].append(guess)
    game_state['attempts'] -= 1
    feedback = get_feedback(guess, game_state['secret_word'])
    feedback_message = ""
    for char in feedback:
        if char == "correct":
            feedback_message += WordleGreen
        elif char == "misplaced":
            feedback_message += WordleYellow
        else:
            feedback_message += WordleGray
    feedback_embed = discord.Embed(title="Feedback", description=feedback_message)

    game_embed = game_state['game_message'].embeds[0]
    game_embed.description += f"\n{feedback_message} - {guess}"
    game_embed.set_footer(text=f"You have {game_state['attempts']} attempts left.")
    await game_state['game_message'].edit(embed=game_embed)

    if guess == game_state['secret_word'].strip():
        embed = discord.Embed(title="Congratulations!", description="You guessed the word correctly... :rolling_eyes:")
        embed.add_field(name="The secret word was:", value=game_state['secret_word'], inline=False)
        await ctx.send(embed=embed)
        user_scores[ctx.author.id] = user_scores.get(ctx.author.id, 0) + 1
        user_streaks[ctx.author.id] = user_streaks.get(ctx.author.id, 0) + 1
        award_collection_point(ctx.author.id)  # Award Collection Point to the winner
        del game_states[ctx.author.id]

    else:
        if game_state['attempts'] == 0:
            embed = discord.Embed(title="Game Over", description="Womp Womp you suck!!! Start a new game using `!wordle`.")
            embed.add_field(name="The secret word was:", value=game_state['secret_word'], inline=False)
            await ctx.send(embed=embed)
            # Reset streak on loss
            user_streaks[ctx.author.id] = 0
            del game_states[ctx.author.id]

    # Delete the guess command message if it's not None
    if ctx.message:
        await delete_message_safely(ctx, ctx.message)

async def delete_message_safely(ctx, message):
    try:
        await message.delete()
    except discord.errors.NotFound:
        print("Error: Message not found. Cannot delete.")

# Wordle Streaks command
@client.command()
async def wordle_streaks(ctx):
    global user_streaks

    # Filter users with streaks greater than 0
    users_with_streaks = {k: v for k, v in user_streaks.items() if v > 0}

    # Sort users by streaks (highest to lowest)
    sorted_users = sorted(users_with_streaks.items(), key=lambda x: x[1], reverse=True)

    embed = discord.Embed(title=":fire: Wordle Streaks", color=discord.Color.gold())
    placement_emojis = ["🥇", "🥈", "🥉"]  # Discord emojis for 1st, 2nd, and 3rd place

    for idx, (user_id, streak) in enumerate(sorted_users):
        user = ctx.guild.get_member(user_id)
        placement = f"{idx + 1}."  # Default placement number
        if idx < len(placement_emojis):
            placement = placement_emojis[idx]  # Use emoji for 1st, 2nd, and 3rd place
        if user:
            embed.add_field(name=f"{placement} {user.display_name}", value=f"Streak: {streak}", inline=False)

    await ctx.send(embed=embed)
    await ctx.message.delete()

## Connect4 Code ##

# Player class to track players in the game
class Connect4Player:
    def __init__(self, member, token_emoji):
        self.member = member
        self.token_emoji = token_emoji
        self.score = 0
        self.collection_points = 0  # Track collection points for each player
        self.emeralds = 0  # Track emeralds for each player
        self.rubies = 0  # Track rubies for each player

# Connect4 game class
class Connect4Game:
    def __init__(self, player1, player2):
        self.board = [[ConnectBoard for _ in range(7)] for _ in range(6)]
        self.column_heights = [0] * 7  # Tracks the height of each column
        self.players = [player1, player2]
        self.turn = 0  # Index of the current player in self.players
        self.active = True
        self.winner = None

    async def make_move(self, column, ctx):
        if not self.active:
            return "Game is already over."
        if not 0 <= column < 7:
            return "Invalid column. Please choose a column between 0 and 6."
        row = self.column_heights[column]  # Get the next available row in the chosen column
        if row >= 6:
            return "Column is full. Please choose another column."
        self.board[row][column] = self.players[self.turn].token_emoji
        self.column_heights[column] += 1  # Increase the column height
        if self.check_winner(row, column):
            self.active = False
            self.winner = self.players[self.turn]
            return None
        self.turn = 1 - self.turn  # Switch turns
        return None  # Move successful

    def check_winner(self, row, col):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for i in range(1, 4):
                r, c = row + i * dr, col + i * dc
                if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == self.board[row][col]:
                    count += 1
                else:
                    break
            for i in range(1, 4):
                r, c = row - i * dr, col - i * dc
                if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == self.board[row][col]:
                    count += 1
                else:
                    break
            if count >= 4:
                return True
        return False

# Emoji definitions
ConnectBoard = "<:ConnectBoard:1213906784821977118>"
ConnectRed = "<:ConnectRed:1213906783437848616>"
ConnectYellow = "<:ConnectYellow:1213906785941987399>"
number_emojis = ["\u0031\u20E3", "\u0032\u20E3", "\u0033\u20E3", "\u0034\u20E3", "\u0035\u20E3", "\u0036\u20E3", "\u0037\u20E3"]

@client.command()
async def connect4(ctx, opponent: discord.Member):
    if opponent == ctx.author:
        await ctx.send("You cannot play against yourself, nerd!")
        return

    # Initialize player1 and player2 instances, and load their existing economy values if available
    player1 = players.get(ctx.author.id, Connect4Player(ctx.author, ConnectRed))
    player2 = players.get(opponent.id, Connect4Player(opponent, ConnectYellow))
    
    # Create a new Connect4Game instance with the initialized players
    game = Connect4Game(player1, player2)
    
    # Send initial game message and add number emojis as reactions
    message = await ctx.send(f"{game.players[game.turn].member.mention}, it's your turn!", embed=create_embed(game))
    for emoji in number_emojis:
        await message.add_reaction(emoji)

    # Main game loop
    while game.active:
        reaction, user = await client.wait_for('reaction_add', check=lambda r, u: u == game.players[game.turn].member and r.message.id == message.id and str(r.emoji) in number_emojis)
        column = number_emojis.index(str(reaction.emoji))
        error = await game.make_move(column, ctx)
        if error:
            await ctx.send(error)
        else:
            await update_message(message, game)
            if not game.active:
                if game.winner:
                    await add_winning_chip(message, game)
                    await send_winning_embed(ctx, game)
                    if game.winner == player1:
                        player1.score += 1
                        player1.collection_points += 1  # Award 1 CP for winning Connect 4
                        save_economy_values()  # Save updated economy values
                    else:
                        player2.score += 1
                        player2.collection_points += 1  # Award 1 CP for winning Connect 4
                        save_economy_values()  # Save updated economy values
                else:
                    await ctx.send("It's a draw!")

async def update_message(message, game):
    await message.edit(content=f"{game.players[game.turn].member.mention}, it's your turn!", embed=create_embed(game))

async def add_winning_chip(message, game):
    embed = message.embeds[0]
    winning_emoji = game.players[game.turn].token_emoji
    embed.set_field_at(0, name='\u200b', value=embed.fields[0].value.replace(ConnectBoard, winning_emoji))

# Connect4 code
async def send_winning_embed(ctx, game):
    winner = game.winner.member.display_name
    embed = discord.Embed(title="Game Over:", description=f"`{winner}` wins!", color=discord.Color.green())
    await ctx.send(embed=embed)
    award_collection_point(game.winner.member.id)  # Award Collection Point to the winner

def create_embed(game):
    color = discord.Color.red() if game.players[game.turn].token_emoji == ConnectRed else discord.Color.gold()
    embed = discord.Embed(title="Connect 4", color=color)

    # Generate the game board dynamically based on current state
    for row in range(5, -1, -1):  # Loop from bottom row to top row
        row_str = ""
        for col in range(7):
            row_str += game.board[row][col]
        embed.add_field(name="\u200b", value=row_str, inline=False)

    return embed

## CHAT BOT CODE ##

# Define a function to load responses from a text file
def load_responses(filename):
    responses = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if '|' not in line:
                    continue  # Skip lines without the delimiter
                input_text, *output_texts = line.split('|')
                responses[input_text.lower()] = [output_text.strip() for output_text in output_texts]
    except FileNotFoundError:
        pass
    return responses

# Define a function to save responses to a text file
def save_responses(responses, filename):
    with open(filename, 'w') as file:
        for input_text, output_texts in responses.items():
            for output_text in output_texts:
                file.write(f"{input_text}|{output_text}\n")

# Command to chat with the bot
@client.command()
async def chat(ctx, *input_text):
    input_text = ' '.join(input_text)
    responses = load_responses("user_responses.txt")
    if input_text.lower() in responses:
        # If the input text exists in responses, get a random response
        response = random.choice(responses[input_text.lower()])
        await ctx.send(response)
    else:
        # Ask user for a response
        await ctx.send("I'm not sure how to respond to that. You have 60 seconds to help me reply with a response.")

        try:
            # Wait for a response from the user
            response_message = await client.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            # Add the user-provided response to the dictionary
            if input_text.lower() in responses:
                responses[input_text.lower()].append(response_message.content)
            else:
                responses[input_text.lower()] = [response_message.content]
            # Save responses to file
            save_responses(responses, "user_responses.txt")
            await ctx.send("Response added successfully!")
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you took too long to respond. Please try again later.")

# Command to add a response
@client.command()
async def add_response(ctx, input_text, *output_text):
    input_text = input_text.lower()
    output_text = ' '.join(output_text)
    
    if input_text in user_responses:
        # Check if the new response already exists for the given input text
        if output_text in user_responses[input_text]:
            await ctx.send("This response already exists for the given input.")
        else:
            # If the input text already exists, append the new response
            user_responses[input_text].append(output_text)
            await ctx.send("Response added successfully!")
    else:
        # If the input text doesn't exist, create a new list with the response
        user_responses[input_text] = [output_text]
        await ctx.send("Response added successfully!")

@client.event
async def on_reaction_add(reaction, user):
    # Check if the reaction is from the bot or the user is the bot
    if user.bot or reaction.message.author.bot:
        return
    if str(reaction.emoji) == '✅':
        await reaction.message.delete()
    elif str(reaction.emoji) == '❌':
        await reaction.message.delete()
        await user.send("You can help improve my responses by using the command `!add_response <your original input> <new output>`.")

# Command to solve math problems
@client.command()
async def calculate(ctx, *, expression):
    try:
        result = eval(expression)
        await ctx.send(f"{expression} = `{result}`")
    except Exception as e:
        await ctx.send(f"Error: {e}")

# Run the Discord bot with your token
load_economy_values()
client.run('MTIwNTcyODE4MzI5MTQ3ODA1Ng.GnDsAJ.UyTvS0jOyj99c88i5E-uXuu13xepuFfXBC1N8A')
