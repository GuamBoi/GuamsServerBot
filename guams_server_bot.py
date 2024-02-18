#Import List
import discord
from discord.ext import commands

# Other Imports
from command_explanations import commands_data
from discord.ext.commands import Command
from discord.ext.commands import Cog
import random
import logging
import os
import asyncio

# Initialize the bot with intents
intents = discord.Intents.all()
intents.voice_states = True

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
base_path = '/home/kali/GuamsServerBot/'
ticket_logs_folder = '/home/kali/GuamsServerBot/Ticket Logs/'
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

#Command List
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
    embed.add_field(name=":sos: !help_commands", value="Opens the Command Help Menu", inline=False)
    embed.set_footer(text=f"Bot Version: {bot_version}")
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

# Sepcial Roll Commands
@client.command()
async def roll_commands(ctx):
    embed = discord.Embed(title="Roll Specific Commands", color=discord.Color.red())
    embed.add_field(name=":crown: !friend_commands", value="Lists the Special @Friend Commands", inline=False)
    embed.add_field(name=":flag_gu: !mod_commands", value="Lists the Special @Moderator Commands", inline=False)
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

### SUGGESTION AND POLL COMMANDS ###

@client.command()
async def suggest(ctx, *, question):
    print(f'INFO:__main__:Suggestion created by {ctx.author.name}: {question}')
    suggestion_channel = client.get_channel(suggestion_channel_id)

    if not suggestion_channel:
        await ctx.send("Suggestion channel not found.")
        return

    try:
        default_avatar_url = "https://example.com/default_avatar.png"  # Define your default avatar URL here

        embed = discord.Embed(title="Server Suggestion", description=question, color=discord.Color.blue())
        embed.add_field(name="Reaction Key", value="Voting Reactions: `👍 = Yes` / `👎 = No` \n Mod Reactions: `✅ = Approve` / `❌ = Decline`", inline=False)

        avatar_url = ctx.author.avatar.url if ctx.author.avatar else default_avatar_url
        embed.set_footer(text=f"Suggested by {ctx.author.name}", icon_url=avatar_url)  # Using the username in the footer

        message = await suggestion_channel.send(embed=embed)
        await message.add_reaction('👍')
        await message.add_reaction('👎')
        await message.add_reaction('✅')  # Approval
        await message.add_reaction('❌')  # Decline

        success_embed = discord.Embed(title="New Server Suggestion", description=f"{ctx.author.mention} created a new server suggestion! Go vote on it [HERE]({message.jump_url})!", color=discord.Color.green())
        await ctx.send(embed=success_embed)
    except Exception as e:
        error_embed = discord.Embed(title="Error", description=f"An error occurred: {e}", color=discord.Color.red())
        await ctx.send(embed=error_embed)

@client.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == suggestion_channel_id:
        suggestion_channel = client.get_channel(suggestion_channel_id)
        message = await suggestion_channel.fetch_message(payload.message_id)
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        # Check if the reacting member has the Moderator role
        moderator_role = discord.utils.get(guild.roles, name="Moderator")
        is_moderator = moderator_role in member.roles if moderator_role else False

        if is_moderator and str(payload.emoji) in ['✅', '❌']:
            # Only moderators can approve or decline suggestions
            if str(payload.emoji) == '✅':
                # Handle Approval
                approved_messages_file = os.path.join('Bot Messages/', 'approved_messages.txt')
                with open(approved_messages_file, 'r') as file:
                    approved_messages = file.readlines()
                    random_approved_message = random.choice(approved_messages).strip()
                approved_channel = client.get_channel(approved_channel_id)

                suggestion_content = message.embeds[0].description
                embed = discord.Embed(title=":white_check_mark: Approved Suggestion", color=discord.Color.green())
                embed.add_field(name="Original Suggestion", value=suggestion_content, inline=False)
                embed.add_field(name="Server Note", value=random_approved_message, inline=False)
                embed.add_field(name="Original Suggestion", value=f"To view the original suggestion click [HERE]({message.jump_url}).")
                embed.set_footer(text=f"Approved by: {member.display_name}")
                await approved_channel.send(embed=embed)

            elif str(payload.emoji) == '❌':
                # Handle Decline
                member = guild.get_member(payload.user_id)
                moderator_role = discord.utils.get(guild.roles, name="Moderator")

                if moderator_role in member.roles:
                    # Prompt the moderator to provide a reason via DM
                    try:
                        reason_prompt_embed = discord.Embed(
                            title="Decline Reason Prompt",
                            description="Please provide a reason for declining the suggestion:",
                            color=discord.Color.red()
                        )
                        dm_prompt = await member.send(embed=reason_prompt_embed)

                        reason_message = await client.wait_for(
                            'message',
                            timeout=120.0,
                            check=lambda m: m.author == member and m.guild is None
                        )

                        declined_reason = reason_message.content
                    except asyncio.TimeoutError:
                        timeout_embed = discord.Embed(
                            title="Decline Reason Prompt Timeout",
                            description="No reason provided. Cancelling the decline process.",
                            color=discord.Color.red()
                        )
                        await member.send(embed=timeout_embed)
                        return
                else:
                    # Handle Decline without reason from a non-moderator
                    declined_messages_file = os.path.join('Bot Messages/', 'declined_messages.txt')
                    with open(declined_messages_file, 'r') as file:
                        declined_messages = file.readlines()
                        random_declined_message = random.choice(declined_messages).strip()

                    declined_reason = random_declined_message

                declined_channel = client.get_channel(declined_channel_id)

                suggestion_content = message.embeds[0].description
                embed = discord.Embed(title="Declined Suggestion", color=discord.Color.red())
                embed.add_field(name="Original Suggestion", value=suggestion_content, inline=False)
                embed.add_field(name="Declined Reason", value=declined_reason, inline=False)
                embed.add_field(name="Original Suggestion", value=f"To view the original suggestion click [HERE]({message.jump_url}).")
                embed.set_footer(text=f"Declined by: {member.display_name}")
                await declined_channel.send(embed=embed)

# Create Polls Command
@client.command()
async def poll(ctx, *, question_and_options):
    # Define the poll duration (24 hours)
    poll_duration = 24 * 60 * 60  # 24 hours in seconds

    # Create a list of number emojis
    number_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
    # Split the question and options
    question, *options = question_and_options.split('/')

    # Create the poll message with number emojis
    poll_message = f"**{question.strip()}**\n\n"
    for i, option in enumerate(options[:9]):
        emoji = number_emojis[i]
        poll_message += f"{emoji} - {option.strip()}\n"

    # Send the poll message to the specified channel
    poll_channel = client.get_channel(poll_channel_id)
    if poll_channel:
        poll_embed = discord.Embed(title=":bar_chart: Server Poll", description=poll_message, color=discord.Color.blue())
        poll_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        poll_embed.set_footer(text="React with the corresponding emoji to vote")

        # Send the poll message and store the message object
        poll_embed_message = await poll_channel.send(embed=poll_embed)

        # Add number reactions to the poll message
        for i, emoji in enumerate(number_emojis[:len(options)]):
            await poll_embed_message.add_reaction(emoji)

        # Dictionary to store votes for each option
        votes = {emoji: 0 for emoji in number_emojis[:len(options)]}

        # Event listener for reaction adds
        @client.event
        async def on_reaction_add(reaction, user):
            nonlocal votes
            if reaction.message.id == poll_embed_message.id and user != client.user and str(reaction.emoji) in votes:
                votes[str(reaction.emoji)] += 1

        # Wait for the poll duration
        await asyncio.sleep(poll_duration)

        # Get the total votes
        total_votes = sum(votes.values())

        # Sort options by number of votes
        sorted_options = sorted(votes.items(), key=lambda x: x[1], reverse=True)

        # Create the poll result message
        result_message = f"**Poll Results for \"{question.strip()}\"**\n\n"
        for i, (emoji, votes_count) in enumerate(sorted_options):
            option_index = int(emoji.split('')[0]) - 1
            result_message += f"{i+1}. {options[option_index].strip()} - {votes_count} votes\n"

        # Send the poll result message to the specified channel
        result_channel = client.get_channel(result_channel_id)
        if result_channel:
            result_embed = discord.Embed(title=":bar_chart: Poll Results", description=result_message, color=discord.Color.green())
            result_embed.add_field(name="Original Poll", value=f"To view the original poll click [HERE]({poll_embed_message.jump_url}).")
            await result_channel.send(embed=result_embed)

### TICKET COMMANDS ###

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
        embed.add_field(name=":bar_chart: !poll_friends", value="Sends a Poll to the #friend-chat", inline=False)
        embed.set_footer(text=f"Bot Version: {bot_version}")
        await ctx.send(embed=embed)
        await ctx.message.delete()
    
# poll_friends command
    @commands.command()
    @commands.has_role(friend_role_name)
    async def poll_friends(self, ctx, *, question_and_options):
        # Define the poll duration (24 hours)
        poll_duration = 24 * 60 * 60  # 24 hours in seconds

        # Create a list of number emojis
        number_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
         # Split the question and options
        question, *options = question_and_options.split('/')

        # Create the poll message with number emojis
        poll_message = f"**{question.strip()}**\n\n"
        for i, option in enumerate(options[:9]):
            emoji = number_emojis[i]
            poll_message += f"{emoji} - {option.strip()}\n"

        # Send the poll message to the specified channel
        poll_channel = self.client.get_channel(poll_friends_channel_id)
        if poll_channel:
            poll_embed = discord.Embed(title=":bar_chart: Friend Poll", description=poll_message, color=discord.Color.blue())
            poll_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            poll_embed.set_footer(text="React with the corresponding emoji to vote")
            poll_embed_message = await poll_channel.send(embed=poll_embed)

            # Add number reactions to the poll message
            for i, emoji in enumerate(number_emojis[:len(options)]):
                try:
                    await poll_embed_message.add_reaction(emoji)
                except Exception as e:
                    print("Error adding reaction:", e)

            # Wait for the specified poll duration
            await asyncio.sleep(poll_duration)

            # Fetch the poll message again to get updated reactions
            poll_embed_message = await poll_channel.fetch_message(poll_embed_message.id)

            # Update the poll message with the number of votes for each option
            poll_results = {}
            for reaction in poll_embed_message.reactions:
                emoji_index = number_emojis.index(str(reaction.emoji))
                if emoji_index != -1:
                    poll_results[f"{options[emoji_index].strip()}"] = reaction.count - 1  # Exclude bot's own reaction

            # Construct the poll results message
            results_message = "**Poll Results:**\n\n"
            for option, count in poll_results.items():
                results_message += f"{option}: {count} vote(s)\n"

            # Send the poll results message
            poll_results_embed = discord.Embed(title=":first_place: Poll Results", description=results_message, color=discord.Color.green())
            await poll_channel.send(embed=poll_results_embed)

            # Delete the original poll message
            await poll_embed_message.delete()
        else:
            await ctx.send("Poll channel not found.")

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
            embed.add_field(name=":hourglass: !timeout <username> <time in seconds> <reason>", value="Puts a user in 'timeout' for a set duration of time.", inline=False)
            embed.add_field(name="!:boot: kick <username> <reason>", value="Kicks a user from the server", inline=False)
            embed.add_field(name=":no_entry_sign: !ban <username> <reason>", value="Bans a user from the server", inline=False)
            embed.set_footer(text=f"Bot Version: {bot_version}")  # Make sure bot_version is defined
            await ctx.send(embed=embed)
        await ctx.message.delete()

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
            "🌀": {"name": "`Splitgate`", "role_id": 1193340302782648510}
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

# Bot Token
client.run('YOUR_DISCORD_BOT_TOKEN')
