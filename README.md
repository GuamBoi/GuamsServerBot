# Guam's Server Bot

Welcome to Guam's Server Bot! This bot is designed to enhance your Discord server experience with various functionalities. Below you'll find an in-depth guide on how to set up and use this bot effectively.

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Setup](#setup)
4. [Commands](#commands)
5. [Thank You!](#thanks)

## Introduction <a name="introduction"></a>
Guam's Server Bot is a Discord bot built using the Discord.py library. This bot will require you to change a few things within the code to get it working within your server! Feel free to download it and make whatever changes you would like! I post frequent updates for it too so make sure to come back and check here as Updates are created to see if they are something you want to add to your server! Hope you enjoy it!

## Features <a name="features"></a>
- Automated welcome and goodbye messages.
- Server suggestions and polls.
- Ticketing system for private communication with server moderators.
- Voice chat commands for muting and unmuting all users in your voice channel.
- Dice rolling commands for various types of dice.
- Timer functionality for setting reminders.

## Setup <a name="setup"></a>
To set up Guam's Server Bot for your Discord server, follow these steps:
1. Clone the repository to your local machine.
  $ git clone https://github.com/your_username/guams-server-bot.git

2. Install the required dependencies using pip.
- Python 3.x
- discord.py
- asyncio
  
3. Obtain your Discord bot token from the [Discord Developer Portal](https://discord.com/developers/applications).
4. Replace `'YOUR_DISCORD_BOT_TOKEN' and 'YOUR_CHANNEL_ID` in the code with your actual Discord Dot Token and Channel IDs.
5. Customize the bot's behavior and messages according to your preferences.
6. Delete the `'DELETE_ME.txt'` file from the `Ticket Logs` *Not Required but I would lol
7. Deploy the bot to your server. 

## Commands <a name="commands"></a>
- **Server Commands**: 
- `!suggest <your suggestion>`: Creates a server suggestion.
- `!poll <poll question>`: Creates a server poll.
- `!ticket`: Creates a new private ticket with the server mods.
- `!dice_commands`: Lists all the dice commands.
- `!invite`: Sends an invite to the general chat for the game you're playing.
- `!coinflip`: Flips a coin.
- `!timer <HH:MM>`: Set a timer. Make sure your time amount matches the code format!
- **Voice Chat Commands**:
- `!voice_commands`: Lists all the voice chat commands.
- `!mute`: Mutes you and all members in the voice chat with you.
- `!unmute`: Unmutes you and all members in the voice chat with you.
- **Dice Commands**:
- `!d4`: Rolls a D4 dice.
- `!roll`: Rolls a normal D6 dice.
- `!d8`: Rolls a D8 dice.
- `!d10`: Rolls a D10 dice.
- `!d12`: Rolls a D12 dice.
- `!d20`: Rolls a D20 dice.
  
## Thank You! <a name="thanks"></a>
Thank you for choosing Guam's Server Bot! If you have any questions or need further assistance consider joining my [Discord](https://discord.gg/sKhasKfd)
