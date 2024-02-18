commands_data = {
        '!explain': {
        'title': 'The Explain Command',
        'command': '`!explain <!command_you_need_help_with>`',
        'description': 'This command explains all the commands on the server. When using this command replace `<!command_you_need_help_with>` with the command you need help with. \nPlease Note: You only need the base of the commands so dont include any fields after the command.',
        'usage': 'Everyone can use this command!',
        'channels': 'This command works in any channel',
        'example' : '`!explain !suggest`'
    },
    '!command_help': {
        'title': 'The Command Help Command',
        'command': '`!command_help`',
        'description': 'This command allows you to chat with me, the Server Bot! I\'m hoping to grow and be able to answer more advance questions in the future, but for now server commands are all I know...',
        'usage': 'Everyone can use this command!',
        'channels': 'This command works in any channel, but will create a new private chat between you and I under the `🎫 Tickets / Support` catagory.'
    },
        '!commands': {
        'title': 'The Commands Command',
        'command': '!commands',
        'description': 'This command shows all available commands you can use to react with me!',
        'usage': 'Everyone can use this command!',
        'channels': 'This command works in any channel'
    },
    '!suggest': {
        'title': 'The Suggestion Command',
        'command': '`!suggest <your suggestion>`',
        'description': 'This command creates a suggestion for users to vote on. Moderators can also Approve or Decline suggestions and they will be sent to their respective channels. \nTo use this command make sure to replace `<your suggestion>` with the suggetion you want to see added to the server. This command will allow other users to vote on your suggestions, and allows moderators to approve or decline your suggestions.',
        'usage': 'Everyone can use this command!',
        'channels': 'This command works in any channel, but will send the reult to the `:grey_question: server-suggetions` channel',
        'example': '`!suggest Create a new custom server emoji`'
    },
    '!poll': {
        'title': 'The Poll Command',
        'command': '`!poll [Your Question] / <option 1> / <option 2> / <option 3> / etc...`',
        'description': 'Starts a poll in the  channel for members to vote on The poll lasts for 24 hours and then will display the poll results in the `🌟-poll-results` channel. \nMake sure to do the following when using this command: \n1. Change `[Your Question] to the question you want to ask in your poll. \n2. change `<option 1> / <option 2> / <option 3> / etc...` with the options members can pick from. You are allowed up to 9 options \n3. Make sure to place all of the `/` as you see them in the command. See the example.',
        'usage': 'Everyone can use this command!',
        'channels': 'This command works in all channels but will post the polls to the `📊-server-polls` channel',
        'example': '`!poll Replace with your poll question? / Option 1 / Option 2 / Option 3 / Option 4 / Option 5 / Option 6 / Option 7 / Option 8 / Option 9`'
    },
    '!ticket': {
        'title': 'The Ticket Command',
        'command': '`!ticket`',
        'description': 'This command creates a private ticket between you and the server Moderators in the `🎫 Tickets / Support` channel catagory. Here you can report issues you are having with specific server features, or users on the server. Moderators also have the ability to log anything said in these channels to be reviewed latter. Once your issue has been resolved a Moderator can then close your ticket which will delete the channel and everything said inside.',
        'usage': 'Everyone can use this command!',
        'channels': 'This command can be used in any channel and will delete the !ticket line from any channel'
    },
    '!invite': {
        'title': 'The Invite Command',
        'command': '`!invite`',
        'description': 'This command will invite the roll corresponding to the game you are playing to play with you in your voice channel. It will ping all the users that follow the game you\'re playing and ask them to join you in the voice channel you\'re in. \n Please Note: You must allow discord to see what game your playing, have the game launched, and be in a voice channel for this command to work! It also only works for games in the server.',
        'usage': 'Everyone can use this command!',
        'channels': 'This command works in all channels, but will only send invites to the `💬-general-chat`',
        'example': 'If you\'re playing Dead By Daylight and want a full party type `!invite` to invite other Dead By Daylight Players to join!'
    },
    '!timer': {
        'title': 'The Timer Command',
        'command': '`!timer <HH:MM>`',
        'description': 'This command sets a timer for a specific amout of time. In this command makesure to replace `<HH:MM>` with the amount of time you want to set the timer for in `Hours` and `Minutes`.',
        'usage': 'Everyone can use this command!',
        'channels': 'This command works in any channel!',
        'example': 'To set a timer for an Hour and a half type `!timer 01:30`'
    },
    '!coinflip': {
        'title': 'The Coinflip Command',
        'command': '`!coinflip`',
        'description': 'This command flips a coin and lets you know if it landed on `Heads` or `Tails`',
        'usage': 'Everyone can use this command!',
        'channels': 'This command works in any channel!'
    },
    '!dice_commands': {
        'title': 'The Dice Commands Command',
        'command': '`!dice_commands`',
        'description': 'This command lists all the dice commands available in the server. ',
        'usage': 'Everyone can use this command!',
        'channels': 'This command works in any channel!'
    },
    '!d4': {
        'title': 'The D4 Command',
        'command': '`!d4`',
        'description': 'This command rolls a D4 dice and lets you know what number it rolled.',
        'usage': 'Everyone can use this command!',
        'channels': 'This command works in any channel!'
    },
    '!roll': {
        'title': 'The Roll Command',
        'command': '`!roll`',
        'description': 'This command rolls a normal 6 sided dice and lets you know what number it rolled.',
        'usage': 'Everyone can use this command!',
        'channels': 'This command works in any channel!'
    },
    '!d8': {
        'title': 'The D8 Command',
        'command': '`!d8`',
        'description': 'This command rolls a D8 dice and lets you know what number it rolled.',
        'usage': 'Everyone can use this command!',
        'channels': 'This command works in any channel!'
    },
    '!d10': {
        'title': 'The D10 Command',
        'command': '`!d10`',
        'description': 'This command rolls a D10 dice and lets you know what number it rolled.',
        'usage': 'Everyone can use this command!',
        'channels': 'This command works in any channel!'
    },
    '!d12': {
        'title': 'The D12 Command',
        'command': '`!d12`',
        'description': 'This command rolls a D12 dice and lets you know what number it rolled.',
        'usage': 'Everyone can use this command!',
        'channels': 'This command works in any channel!'
    },
    '!d20': {
        'title': 'The D20 Command',
        'command': '`!d20`',
        'description': 'This command rolls a D20 dice and lets you know what number it rolled.',
        'usage': 'Everyone can use this command!',
        'channels': 'This command works in any channel!'
    },
    '!voice_commands': {
        'title': 'The Voice Commands Command',
        'command': '`!voice_commands`',
        'description': 'This command list all the commands that work in voice channels',
        'usage': 'Everyone can use this command!',
        'channels': 'This command works in any channel!'
    },
    '!mute': {
        'title': 'The Mute Command',
        'command': '`!mute`',
        'description': 'This command mutes everyone in the same voice channel as you',
        'usage': 'Everyone can use this command!',
        'channels': 'This command only works in the `Company VC` and the `😎 Hanging with Friends` voice channels \n Please Note: You must be in a voice channel for this command to work!',
        'example': 'This command is was created to be able to easily mute all members playing Lethal Company. Just type `!mute` and I will do the rest!'
    },
    '!unmute': {
        'title': 'The Unmute Command',
        'command': '`!unmute`',
        'description': 'This command unmutes everyone in the same voice channel as you and only works when followed by the `!mute` command.',
        'usage': 'Everyone can use this command!',
        'channels': 'This command only works in the `Company VC` and the `😎 Hanging with Friends` voice channels \n Please Note: You must be in a voice channel for this command to work!',
        'example': 'This command is was created to be able to easily unmute all members playing Lethal Company. Just type `!unmute` and I will do the rest!'
    },
    '!roll_commands': {
        'title': 'The Roll Commands Command',
        'command': '`!roll_commands`',
        'description': 'This command lists all the Specialty Roll command lists!',
        'usage': 'All users can use this command to see what rolls have special commands, however to see the list of special commands you must have the roll listed at the beginning of the listed commands.',
        'channels': 'This command works in any channel!'
    },
    '!friend_commands': {
        'title': 'The Friend Commands Command',
        'command': '`!friend_commands`',
        'description': 'This command lists all the special commands members with the @friends roll can use',
        'usage': 'Only members with the @friend roll can use this command.',
        'channels': 'This command works in any channel!'
    },
    '!invite_friends': {
        'title': 'The Invite Friends Command',
        'command': '`!invite_friends`',
        'description': 'This command will invite the roll corresponding to the game you are playing to play with you in your voice channel. It will ping all the users that follow the game you\'re playing and ask them to join you in the voice channel you\'re in. \n Please Note: You must allow discord to see what game your playing, have the game launched, and be in a voice channel for this command to work! It also only works for games in the server.',
        'usage': 'Only members with the @friend roll can use this command.',
        'channels': 'This command works in any channel but will only send invites to the `💬-friend-chat`',
        'example': 'If you\'re playing Dead By Daylight and only want to invite other friends type `!invite_friends` to invite other Dead By Daylight Players with the @friend roll to join!'
    },
    '!poll_friends': {
        'title': 'The Poll Friends Command',
        'command': '`poll_friends [Your Question] / <option 1> / <option 2> / <option 3> / etc...`',
        'description': 'This command creates a 24 hour poll for members with the `friends` roll to vote on. The poll expires in 24 hours and will display the final results when the time expires.',        
        'usage': 'Only members with the @friend roll can use this command.',
        'channels': 'This command works in any channel but will send the poll and the results to the `😎 Hanging with Friends` chat',
        'example': '!poll_friends Replace with your poll question? / Option 1 / Option 2 / Option 3 / Option 4 / Option 5 / Option 6 / Option 7 / Option 8 / Option 9'
    },
    '!mod_commands': {
        'title': 'The Mod Commands Command',
        'command': '`!mod_commands`',
        'description': 'This command lists all the special commands members with the @Moderator roll can use',
        'usage': 'Only members with the @Moderator roll can use this command',
        'channels': 'This command works in any channel!'
    },
    '!delete_ticket': {
        'title': 'The Delete Ticket Command',
        'command': '`!delete_ticket`',
        'description': 'This command deletes a ticket from the server. \n Please Note: Tickets should only be deleted after a members issue has been resolved.',
        'usage': 'Only members with the @Moderator roll can use this command',
        'channels': 'This command only works in ticket channels. \n Note: Ticket channels start with `ticket` and end with the members\' username that created the ticket.'
    },
    '!log_ticket': {
        'title': 'The Log Ticket Command',
        'command': '`!log_ticket`',
        'description': 'This command logs a ticket from the server and saves the entire conversation to a file in the bots database. These files can be reviewed latter by Moderators.',
        'usage': 'Only members with the @Moderator roll can use this command',
        'channels': 'This command only works in ticket channels. \n Note: Ticket channels start with `ticket` and end with the members\' username that created the ticket.'
    },
    '!timeout': {
        'title': 'The Timeout Command',
        'command': '`!timeout <username> <time in seconds> <reason>`',
        'description': 'This command puts a member in timeout preventing them from being able to talk in any voice channel for the specified duration of time. To use the command replace `<username> with the username of the member you want to put in timeout / replace `<time in seconds>` with the time duration you want to put them in timeout for / and replace <reason> with the reason for putting them in timeout. \n Please Note: The `<reason>` field is optional, but is nice to add.',
        'usage': 'Only members with the @Moderator roll can use this command',
        'channels': 'This command works in any channel!',
        'example': '`!timeout @mamaslofunk Too much background noise`'
    },
    '!kick': {
        'title': 'The Kick Command',
        'command': '`!kick <username> <reason>`',
        'description': 'This command kicks a member from the server. To use the command replace `<username> with the username of the member you want to kick and replace <reason> with the reason for kicking them. \n Please Note: The `<reason>` field is optional, but is nice to add.',
        'usage': 'Only members with the @Moderator roll can use this command',
        'channels': 'This command works in any channel',
        'example': '`!kick @Raylan He kind of smells`'
    },
    '!ban': {
        'title': 'The Ban Command',
        'command': '`!ban <username> <reason>`',
        'description': 'This command bans a member from the server. To use the command replace `<username> with the username of the member you want to ban and replace <reason> with the reason for kicking them. \n Please Note: The `<reason>` field is optional, but is nice to add.',
        'usage': 'Only members with the @Moderator roll can use this command',
        'channels': 'This command works in any channel',
        'example': '`!ban @Guamboi This is my server now!`'
    }
}
