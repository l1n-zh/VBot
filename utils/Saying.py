from json import load
from random import choice
import glob
from discord import Embed
import sys

class Saying:
    sayings = []
    files = glob.glob('assets/sayings/*.json')
    for fn in files:
        with open(fn, encoding='utf-8') as file:
            sayings.append(load(file))


    @classmethod
    def random_get(cls, index: int = 1):
        return choice(cls.sayings[index])
    
    
    @classmethod
    def set_footer(cls, embed: Embed, index: int = 1):
        embed.set_footer(text = ': ' + cls.random_get(index), icon_url='https://media.discordapp.net/attachments/933779977638400101/949148193076183100/IMG_4208.png')
        return embed
