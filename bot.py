import discord
import potdfunctions as pf
from discord.ext import commands
from datetime import date
import os
import currentimagedata as cid
from dotenv import load_dotenv
import scheduledtasks as st
import schedule
import time


CURRENT_DATE = date.today()

load_dotenv()
TOKEN = os.getenv('TOKEN')


def run_bot():
    bot = commands.Bot(command_prefix="^", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print("Bot is now running")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
            st.store_new_potd()
            schedule.every().day.at("12:00").do(st.store_new_potd)
            while True:
                print("Tick")
                schedule.run_pending()
                time.sleep(45)
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
                              color=0xFF5733, )
        embed.set_image(url=image_url_comp)
        await interaction.response.send_message(embed=embed)

    bot.run(TOKEN)
