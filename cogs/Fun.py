from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed, File, Message

from asyncio import sleep
from asyncio import TimeoutError as Timeout

import requests
from io import BytesIO
from PIL import Image

from random import choice, randint
from re import findall, search, split, DOTALL, MULTILINE
from itertools import chain

from utils import *
from assets import Assets
from .cn_word_detector.detector import detect_cn_words

from .screenshot_generator.Generator import Generator
from time import localtime, strftime
from faker import Faker


class Fun(Cog):

    @commands.Cog.listener()
    async def on_ready(self):
        self.backstage = self.bot.get_channel(954718717974044703)
        self.emojis = {}
        for guild in self.bot.guilds:
            if guild.id in (954768006964183060, 954761016728752169):
                for emoji in guild.emojis:
                    self.emojis[emoji.name] = str(emoji)

        self.words = []
        for fn in ('easy', 'medium'):
            with open(f'assets/words/{fn}.txt') as f:
                self.words.append([l[:-1] for l in f.readlines()])

    @commands.Cog.listener()
    async def on_message(self, message:Message):
        count = len(findall("高粱|<@859231400071135262>", message.content))
        if count:
            await message.channel.send(
                embed = Embed().set_image(url = Assets.picture["dan"]),
                delete_after = 0.3*count)
        
        detection = detect_cn_words(message.content)
        if detection:
            await message.channel.send(
                embed = detection
            )


    @commands.command(aliases=['ss'])
    async def screenshot(self, ctx: Context, *, inputs):
        inputs = "\n" + inputs
        user_ids = findall(r"\n<@([0-9]+)> *:", inputs)
        messages = split(r"\n<@[0-9]+> *:", inputs)
        img_id = ctx.message.id
        generator = Generator(img_id)
        fake = Faker()
        Faker.seed()
        time = fake.date_between(start_date='-2y', end_date='today')
        time = time.strftime("%Y/%m/%d")
        if(messages[0]): user_ids.insert(0,choice(ctx.guild.members).id)
        else: del messages[0]
        for uid, message in zip(user_ids,messages):
            while message[0] in ["\n"," ","　"]: message = message[1::]
            member = await ctx.guild.fetch_member(uid)
            if(member):
                generator.add(
                    member.display_name,
                    member.color,
                    member.display_avatar.url,
                    message,
                    time)
            else:
                user = await self.bot.fetch_user(uid)
                generator.add(
                    user.name,
                    "white",
                    user.display_avatar.url,
                    message,
                    time)
        embed = Embed(title="請稍後..")
        embed.set_image(url="https://c.tenor.com/5StiWpbuWx8AAAAi/%E6%9D%B1%E6%96%B9-%E5%B0%91%E5%A5%B3%E8%AE%80%E5%8F%96%E4%B8%AD.gif")
        reply = await ctx.send(embed = embed)
        generator.generate()
        tmp = await self.backstage.send(file=File(f"buffer/screenshot{img_id}.png"))
        generator.delete_img()
        embed.set_image(url = tmp.attachments[0].url)
        embed.title = f"來自{time}的截圖"
        await reply.edit(embed = embed)
        
    @commands.command(aliases=['bt'])
    async def bigtext(self, ctx: Context, text:str):
        r = requests.get(f'https://www.moedict.tw/{text}.png')
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content))
            img = img.crop(img.getbbox())
            
            fp = BytesIO()
            img.save(fp, format="PNG")
            fp.seek(0)
            msg = await self.backstage.send(file = File(fp, filename = f"{text}.png"))
            e = Embed()
            e.set_footer(text = f'from {ctx.author.display_name}', icon_url = ctx.author.avatar.url)
            e.set_image(url = msg.attachments[0].url)

            await ctx.send(embed = e)
            
        else: print(r.status_code)


    @commands.command(aliases=['wd'])
    async def wordle(self, ctx: Context, difficulty:str = 'easy', timeout:int = 30):
        emojis = self.emojis
        
        game_area = await ctx.message.create_thread(name=f'{ctx.author.display_name} 的 WordleGame')
        row = emojis['empty'] * 5
        embed = Embed(title = "點擊符號開始遊戲")

        game = await game_area.send(f'{row}\n'*5, embed=embed)
        W = emojis['Wa']
        await game.add_reaction(W)

        try:
            await self.bot.wait_for(
                'reaction_add',
                check = lambda r, u: all([
                    u.id == ctx.author.id,
                    str(r) == W
                ]),
                timeout = 20)
        except Timeout:
            await game_area.delete()
            return
        else:
            await game.clear_reactions()

        timeout =  min((5,10,20,30), key = lambda i:abs(i-timeout))
        answer = choice(self.words[difficulty == 'hard'])
        record = ''
        def get_result(guess):
            nonlocal record
            result = ''
            answer_record = list(answer)
            guess = list(str(guess).upper())
            status_list = [0]*5

            for i in range(5):
                if(answer_record[i] == guess[i]):
                    status_list[i] = 2
                    answer_record[i] = ''

            for i in range(5):
                if not status_list[i]:
                    if(guess[i] in answer_record):
                        status_list[i] = 1
                        answer_record[i] = ''
                    
            for status, char in zip(status_list, guess):
                record += '⬛🟨🟩'[status]
                result += emojis[ char + 'cba'[status] ]
            record += '\n'
            return result

        set_author = lambda e: e.set_author(name = "Wordle Game", icon_url="https://cdn.discordapp.com/attachments/954768007597527093/954903092351098910/wordle.png")

        times = 1

        while True:
            
            if times <= 5:
                e = Embed(title = f'回合 **{times}/5**')
                e.set_image(url = Assets.gif[f'{timeout}s'])
                set_author(e)
                await game.edit(embed = e)

                try:
                    guess = await self.bot.wait_for(
                        'message',
                        check = lambda m:all([
                            m.content.upper() in chain(*self.words),
                            m.channel == game_area,
                            m.author.id == ctx.author.id
                        ]),
                        timeout = timeout )
                    
                except Timeout:
                    e = Embed(title = f'超時 **正確答案: {answer}**')
                    break
                else:
                    guess = guess.content.upper()
                    content = game.content.replace(row, get_result(guess), 1)
                    game = await game.edit(content = content)
                    times += 1
                    if guess == answer:
                        e = Embed(title = '**恭喜答對**')
                        e.add_field(name = '\u200b', value = record)
                        break
                finally:
                    set_author(e)
                    await game.edit(embed = e)
            else:
                e = Embed(title = f'正確答案: {answer}')
                break
        
        set_author(e)
        await game.edit(embed = e)

        await sleep(10)
        await game_area.delete()



def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))