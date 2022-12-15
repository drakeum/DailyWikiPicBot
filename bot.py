import discord
import potdfunctions as pf
from discord.ext import commands
from datetime import date, timedelta
import os
from dotenv import load_dotenv

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
        except Exception as e:
            print(e)

    @bot.tree.command(name="daily")
    async def daily(interaction: discord.Interaction):
        data = pf.fetch_potd(CURRENT_DATE)
        image_url = data['image_src']
        image_url_comp = pf.make_picture_resolution_1920(image_url)
        print("Fetched image: " + image_url_comp)

        embed = discord.Embed(title="Wikipedia Picture of the Day",
                              url=image_url,
                              description="test",
                              color=0xFF5733, )
        embed.set_image(url=image_url_comp)
        await interaction.response.send_message(embed=embed)

    bot.run(TOKEN)
