## Adding New Reaction Roles to Your Discord Bot

### Step 1: Define the Role

Decide on the emoji you want to use and the role you want to assign users when they react with that emoji. Write down both the emoji name and the role names somewher so they are easy to refrence later!
- NOTE: Its supper important to write down the emoji and roll name EXACTLY as they are spelled in your server. These need to match whats in your code perfectly.  

### Step 2: Update the Bot's Code to fit your Server

Once you have the emoji and role information, you need to update your bot's code to handle the new reactions. This will involves modifying the `on_raw_reaction_add` and `on_raw_reaction_remove` event listeners.

### Step 3.1: Update `on_raw_reaction_add` Event Listener

In the `on_raw_reaction_add` event listener, add a new `elif` block to check if the reaction emoji matches the one you want to assign a role for. If it does, fetch the corresponding role and assign it to the reacting member.

```
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
```

### Step 3.2: Update `on_raw_reaction_remove` Event Listener (Optional but Recomended)
If you want the bot to remove the role when the user removes their reaction, update the `on_raw_reaction_remove` event listener similarly.

```
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

```

### Step 4: Sending Messages as your discord bot
You will want to create a command that allows you to send messages as your discord bot to attach your reaction rolls too. This is because the code will only add the roll to the emoji if it was sent by the bot. Its set this way so users can still use your server emojis without messing up the rolls they selected. Below is the code to send an embeded message to the server as the bot.

```
# Send a message as the Bot
@client.command()
async def send_bot_message(ctx, *, args): # the command to send messages as the bot is set to !send_bot_message. You can change this if you'd like.
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
```

### Additional Notes:
- Make sure that the bot has the necessary permissions to assign and remove roles in your Discord server.
- Double-check the spelling and capitalization of the emoji name and role name to avoid errors.
- Always test your bot thoroughly after making changes to ensure it functions as intended.
