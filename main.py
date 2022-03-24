from discord.ext import commands
import glob
from asyncio import sleep

bot = commands.Bot(command_prefix='-')

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

if __name__ == '__main__':
    for fn in glob.glob('cogs/*.py'):
        bot.load_extension('cogs.'+fn[5:-3])

bot.run("OTMzNzc5NjM5MzgwMzYxMjI2.YemgDg.6wloTk3yfMxH7mb74033kDTfbtw")
# OTUwMzgxODc0ODI2NjAwNDQ4.YiYGGA.-Sp8s63fDcmK5xI9bABYUUvBviY