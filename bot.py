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
update_time = datetime.time(hour=00, minute=37, tzinfo=tz)
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
            for guild in bot.guilds:
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:
                        message_channel = channel
                        print("First channel found in guild " + guild.name)
                        await message_channel.send(embed=embed)
                        break

        @update_and_send_potd.before_loop
        async def before(self):
            await bot.wait_until_ready()
            print("Finished waiting")

    bot = MyBot(command_prefix="^", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print("Bot is now running")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
            st.store_new_potd()
        except Exception as e:
            print(e)

    @bot.hybrid_command(name="daily", description="Shows today's Wikipedia daily picture.")
    async def daily(ctx: commands.Context):
        page_url = cid.page_url
        image_url_comp = cid.image_url_comp
        blurb = cid.blurb
        print("Daily command called, stored image being displayed: " + image_url_comp)

        embed = discord.Embed(title="Wikipedia Picture of the Day",
                              url=page_url,
                              description=blurb,
                              color=0xff8585, )
        embed.set_image(url=image_url_comp)
        await ctx.reply(embed=embed)

    bot.run(TOKEN)
