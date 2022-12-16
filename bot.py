import discord
from discord.ext import commands, tasks
from datetime import date
import datetime
import os
import currentimagedata as cid
from dotenv import load_dotenv
import scheduledtasks as st

tz = datetime.timezone(datetime.timedelta(hours=-5))
CURRENT_DATE = date.today()
update_time = datetime.time(hour=00, minute=1, tzinfo=tz)
target_channel_id = 1040730331264856207
load_dotenv()
TOKEN = os.getenv('TOKEN')


def run_bot():
    class MyBot(commands.Bot):
        async def setup_hook(self):
            print("Bot starting")
            self.update_and_send_potd.start()

        @tasks.loop(time=update_time)
        async def update_and_send_potd(self):
            print("Running scheduled bot task: updating and sending the POTD")
            st.store_new_potd()
            page_url = cid.page_url
            image_url_comp = cid.image_url_comp
            blurb = cid.blurb
            embed = discord.Embed(title="Wikipedia Picture of the Day",
                                  url=page_url,
                                  description=blurb,
                                  color=0xff8585, )
            embed.set_image(url=image_url_comp)
            message_channel = bot.get_channel(target_channel_id)
            await message_channel.send(embed=embed)

        @update_and_send_potd.before_loop
        async def before(self):
            await bot.wait_until_ready()
            print("Finished waiting")

    bot = MyBot(command_prefix="^", intents=discord.Intents.all())
    # client = discord.Client(command_prefix="^", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print("Bot is now running")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
            st.store_new_potd()
        except Exception as e:
            print(e)

    @bot.tree.command(name="daily")
    async def daily(interaction: discord.Interaction):
        page_url = cid.page_url
        image_url_comp = cid.image_url_comp
        blurb = cid.blurb
        print("Daily command called, stored image being displayed: " + image_url_comp)

        embed = discord.Embed(title="Wikipedia Picture of the Day",
                              url=page_url,
                              description=blurb,
                              color=0xff8585, )
        embed.set_image(url=image_url_comp)
        await interaction.response.send_message(embed=embed)

    bot.run(TOKEN)
