from discord import Activity, Intents
from discord.ext import commands
import glob
from asyncio import sleep
from random import choices
from os import getenv
from dotenv import load_dotenv

load_dotenv()


intents = Intents.all()
bot = commands.Bot(command_prefix='-', intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    activities = (('你', 3), ('化學講義', 3), ('英文雜誌', 3), ('Spotify', 2),
                  ('Golf Battle', 0), ('象棋', 0), ('五子棋', 0))
    while not bot.is_closed():
        name, type = choices(activities)[0]
        await bot.change_presence(activity=Activity(name=name, type=type))
        await sleep(120)
    

if __name__ == '__main__':
    filename = slice(5, -3)
    for path in glob.glob('cogs/*.py'):
        bot.load_extension('cogs.' + path[filename])


token = getenv("TOKEN") 
bot.run(token)  # Starts the bot