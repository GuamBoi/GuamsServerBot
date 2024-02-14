# Guam's Server Bot

Welcome to Guam's Server Bot! This bot is designed to enhance your Discord server experience with various functionalities. Below you'll find an in-depth guide on how to set up and use this bot effectively.

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Setup](#setup)
4. [Commands](#commands)
5. [Thank You!](#thanks)
6. [Important Notes](#notes)

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
4. Replace `'YOUR_DISCORD_BOT_TOKEN'` and `'YOUR_CHANNEL_ID'` in the code with your actual Discord Dot Token and Channel IDs.
5. Customize the bot's behavior and messages according to your preferences.
6. Delete the `'DELETE_ME.txt'` file from the `'Ticket Logs'` *Not Required but I would lol
7. Deploy the bot to your server however you'd like! Options too keep your bot up and running all the time are in the `Important Notes` section. 

## Commands <a name="commands"></a>
**Server Commands**: 
- `!suggest <your suggestion>`: Creates a server suggestion in the Specified Channel.
- `!poll <poll question>`: Creates a server poll in the Specified Channel.
- `!ticket`: Creates a new private ticket with the server Mods in the Specified Channel Category must have an @moderator tag or change this in the code.
- `!delete_ticket` : Deletes a specified Ticket. *Must be used in a created Ticket Channel
- `!log_ticket` : Logs a specified Ticket in the `'Ticket Logs'` Folder. *Must be used in a created Ticket Channel
- `!dice_commands`: Lists all the dice commands.
- `!invite`: Sends an invite for the game you're playing in the Specified Channel. *Users must allow discord to see what game they are playing to use this command.
- `!coinflip`: Flips a coin.
- `!timer <HH:MM>`: Set a timer. Make sure users time amount matches the code format!

**Voice Chat Commands**:
- `!voice_commands`: Lists all the voice chat commands.
- `!mute`: Mutes you and all members in the same voice chat with as the user. * We use this for Lethal Company
- `!unmute`: Unmutes you and all members in the voice chat as the user. * We use this for Lethal Company

**Dice Commands**:
- `!d4`: Rolls a D4 dice.
- `!roll`: Rolls a normal D6 dice.
- `!d8`: Rolls a D8 dice.
- `!d10`: Rolls a D10 dice.
- `!d12`: Rolls a D12 dice.
- `!d20`: Rolls a D20 dice.

## Important Command Notes <a name="notes"></a>
1. All commands will automaticly delete their trigger message to keep your server looking clean.

2. All Bot messages should send as an embed and pull their messages from the `Bot Messages` folder. The messages in these files can be edited however you would like the bot to respond! Just make sure the to keep ALL the numbers for each dice thier coresponding `dice_messages.txt` files.

3. All Commands will run in the channel users used them in. Some Commands will send the responces to specific commands to the Channel you specify in the `YOUR_CHANNEL_ID` Sections of the code. 
  These Commands include:
    - `!suggest`, `!poll`, and `!invite`.

4. The `!ticket` command will create a new ticket named `ticket-<users username>` and the `!delete_ticket` and `log_ticket` commands only work in these messages.
   - This command will also send a support message to that channel tagging the user so they know the ticket was created.
   - Only people with the @Moderator tag and the user who the ticket is named after will be able to see the newly created channel.
  
5. To deploy the bot to your server and keep it running all the time you have a few options
   - I use a [Raspberry Pi 3B+](https://www.amazon.com/ELEMENT-Element14-Raspberry-Pi-Motherboard/dp/B07P4LSDYV/ref=sr_1_3?keywords=raspberry+pi+3b%2B&qid=1707900285&sr=8-3) to run mine on, but im sure any Pi would work. 
   - You can also a Cloud Hosting Service like [Heroku](https://www.heroku.com/?utm_source=google&utm_medium=paid_search&utm_campaign=amer_heraw&utm_content=general-branded-search-rsa&utm_term=heroku&gad_source=1&gclid=Cj0KCQiA5rGuBhCnARIsAN11vgSBB_HcY1-m5s-J08hYCxfpPLxoGlskSptqZ92NvNlM8K7EtV_o89oaAgfBEALw_wcB) if you don't have a Raspberry Pi. 
 
## Thank You! <a name="thanks"></a>
Thank you for choosing Guam's Server Bot! If you have any questions or need further assistance consider joining my [Discord](https://discord.gg/sKhasKfd)
