# DailyWikiPicBot
A Discord bot that posts the Wikipedia picture of the day (POTD), everyday

# About
This bot will automatically update and post the Wikipedia picture of the day once a day at 12:00AM EST (this can be changed, see config section below).

The message will be posted in the first text-channel in the server that the bot has permission to send messages in.

Additionally, the current POTD can be viewed any time by using the slash command `/daily` or sending a message command `^daily` (the bot's prefix can be changed, see config section below).

# Requirements and running the bot
- Requires Python 3.9 or greater.

- pip should be installed if you used a Python installer, but if it isn't, install pip.

- In the root folder of the bot, open a command prompt and run the command `pip install -r requirements.txt`.

- In the .env file, replace "YOUR_TOKEN_HERE" with your Discord bot account's token. Don't include the parentheses.

- If you don't know what a Discord bot account is or don't have one, watch [this](https://youtu.be/Gqurhm2QxA0?t=12) video up to 0:48.

To get your bot's token, navigate to the "Bot" section of the bot's application page and click "Reset Token". Copy (and you probably want to save it somewhere) the token. This is the token you will use in the .env file.
![Image showing how to get bot token](https://user-images.githubusercontent.com/47580914/208227610-e9484423-8b84-4a2b-a6d2-856e2b99115d.png)


## Inviting to your server
- To invite the bot to your server, go to your Discord bot account and make sure these boxes are checked off like in the image below.
![Image of required intents](https://user-images.githubusercontent.com/47580914/208226855-93026a5c-a97c-4ba0-a128-4663192080c0.png)

- In the "OAUTH2/URL Generator" section, under scopes check off "bot" and it is reccomended to give it these permissions below.
![Image of bot's reccomended permissions](https://user-images.githubusercontent.com/47580914/208226842-2df7df79-91c9-4d1d-a21a-0a383e16698d.png)

Then, copy the invite link made at the bottom and go to it. That is the link to invite the bot to your sever.

## Running the bot
- In the root folder of the bot, open a command prompt and run the command `python main.py` (a more elegant solution is being worked on).

# Config
A more intuitive solution for changing these is being worked on.
## Changing the auto-update/post time
Open bot.py and edit the line `update_time = datetime.time(hour=5, minute=0)`. This time is in UTC. Change `hour=` to the hour (uses 24hr clock) and `minute` to the minute of the hour you want the bot to update and post at.
## Changing the message command prefix
Open bot.py and edit the like `bot = MyBot(command_prefix="^", intents=discord.Intents.all())`. Change `command_prefix=` to the prefix you want to use for message commands. Make sure to put in in quotation marks, like the default code line has.
