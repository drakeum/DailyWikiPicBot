import discord
from discord.ext import commands, tasks
from datetime import date, datetime
import datetime as dt
import os
import currentimagedata as cid
from dotenv import load_dotenv
import scheduledtasks as st

# Create an EST timezone
tz = dt.timezone(dt.timedelta(hours=-5))
# Store the current date
CURRENT_DATE = date.today()
# Set the time the bot will update the POTD
update_time = dt.time(hour=10, minute=7)
# Load environment variables
load_dotenv()
# Get authorization token from env variables
TOKEN = os.getenv('TOKEN')


# Function to start the bot
def run_bot():
    # Set up timed loop functions
    class MyBot(commands.Bot):
        async def setup_hook(self):
            print("Bot starting")
            self.update_and_send_potd.start()

        # Update the POTD and send it. Updates at the time specified in "time="
        # Sends the message in the first text channel in a server that the bot has permissions to
        # send messages in
        @tasks.loop(time=update_time)
        async def update_and_send_potd(self):
            print("Running scheduled bot task: updating and sending the POTD")
            st.store_new_potd()
            page_url = cid.page_url
            image_url_comp = cid.image_url_comp
            blurb = cid.blurb
            image_date = cid.image_date
            embed = discord.Embed(title="New Wikipedia Picture of the Day!",
                                  url=page_url,
                                  color=0xff8585, )
            embed.set_image(url=image_url_comp)
            embed.add_field(name="Description", value=blurb)
            embed.set_footer(text="Image date: " + image_date)
            for guild in bot.guilds:
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:
                        message_channel = channel
                        print("First channel found in guild " + guild.name)
                        await message_channel.send(embed=embed)
                        break

        # Makes it so the timer loop starts after the bot is ready
        @update_and_send_potd.before_loop
        async def before(self):
            await bot.wait_until_ready()
            print("Finished waiting")

    # Creates instance of the bot that uses the prefix "^" for commands
    bot = MyBot(command_prefix="^", intents=discord.Intents.all())

    # Updates POTD at launch and establishes slash command sync
    @bot.event
    async def on_ready():
        print("Bot is now running")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
            st.store_new_potd()
        except Exception as e:
            print(e)

    # Creates the "daily" command. WHen a user executes this command, the bot will reply with
    # the current POTD
    @bot.hybrid_command(name="daily", description="Shows today's Wikipedia daily picture.")
    async def daily(ctx: commands.Context):
        page_url = cid.page_url
        image_url_comp = cid.image_url_comp
        blurb = cid.blurb
        image_date = cid.image_date
        print("Daily command called, stored image being displayed: " + image_url_comp)
        print("Current time: " + CURRENT_DATE.isoformat() + " " + datetime.now().strftime(
            "%H:%M:%S"))

        embed = discord.Embed(title="Wikipedia Picture of the Day!",
                              url=page_url,
                              color=0xff8585, )
        embed.set_image(url=image_url_comp)
        embed.add_field(name="Description", value=blurb)
        embed.set_footer(text="Image date: " + image_date)
        await ctx.reply(embed=embed)

    # Starts the bot (for real)
    bot.run(TOKEN)
