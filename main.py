from discord import Activity, Intents
from discord.ext import commands
import glob
from asyncio import sleep
from random import choices
from os import environ

intents = Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    activities = (('小黃本', 3), ('文林國小的ㄌㄌ們', 3), ('你的屁股', 3), ('汪汪汪汪汪汪汪汪汪汪', 2),
                  ('cosplay梅花鹿', 0), ('生態池的鱷魚', 0), ('獨角獸', 0),  ('你', 0))
    while not bot.is_closed():
        name, type = choices(activities)[0]
        await bot.change_presence(activity=Activity(name=name, type=type))
        await sleep(120)
    

if __name__ == '__main__':
    filename = slice(5, -3)
    for path in glob.glob('cogs/*.py'):
        bot.load_extension('cogs.' + path[filename])


token = environ.get("TOKEN") 
bot.run(token)  # Starts the bot