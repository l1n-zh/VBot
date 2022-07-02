from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands.errors import *
from discord import Embed, Message
from .online_judge.Problem import Problem
from .online_judge.formatter import *
from utils import *
import re


class OnlineJudge(Cog):
    @commands.Cog.listener()
    async def on_message(self, msg:Message):
        if msg.author.id == self.bot.user.id:
            return
        
        for F in (ZeroJudgeFormatter, RyanJudgeFormatter):
            url_pattern = F.url.replace('?', '\?')
            pattern = f'(((http|https)://)?(www.)?{url_pattern}{F.index_pattern})(.*)?'
            link = re.search(pattern, msg.content)
            if link:
                problem = Problem(link.group(0), F)
                embed = Embed.from_dict(problem.to_embed_dict())
                set_footer(embed, 1)
                await msg.reply(embed = embed)


    @commands.Cog.listener()
    async def on_error(self, ctx: Context, error: CommandInvokeError):
        if(isinstance(error,CommandInvokeError)):
            print(error.original)


    @commands.command(aliases=['zj'])
    async def zerojudge(self, ctx: Context, arg: str):
        problem = Problem(arg, ZeroJudgeFormatter)
        embed = Embed.from_dict(problem.to_embed_dict())
        set_footer(embed, 1)
        await ctx.send(embed = embed)
    

    @commands.command(aliases=['rj'])
    async def ryanjudge(self, ctx: Context, arg:str):
        problem = Problem(arg, RyanJudgeFormatter)
        embed = Embed.from_dict(problem.to_embed_dict())
        set_footer(embed, 1)
        await ctx.send(embed = embed)



def set_footer(embed: Embed, index: int = 1):
    embed.set_footer(text = ': ' + Saying.random_get(index), icon_url='https://media.discordapp.net/attachments/933779977638400101/949148193076183100/IMG_4208.png')
    return embed


def setup(bot: commands.Bot):
    bot.add_cog(OnlineJudge(bot))