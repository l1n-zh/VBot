from discord.ext import commands
from discord.ext.commands.context import Context
from assets.Assets import Assets
from utils import *
import requests
from io import BytesIO
from PIL import Image
from discord import Embed, File
from random import choice
from asyncio import sleep
from asyncio import TimeoutError as Timeout

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
        for fn in ('easy','medium'):
            with open(f'assets/words/{fn}.txt') as f:
                self.words.append([l[:-1] for l in f.readlines()])

    @commands.command(aliases=['bt'])
    async def bigtext(self, ctx: Context, text:str):
        r = requests.get(f'https://www.moedict.tw/{text}.png')
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content))
            img = img.crop(img.getbbox())
            
            fp = BytesIO()
            img.save(fp,format="PNG")
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

        timeout =  min((5,10,20,30),key = lambda i:abs(i-timeout))
        words = self.words[difficulty == 'hard']
        answer = choice(words)

        print(answer)
        W = emojis['Wa']
        embed = Embed(title = "點擊符號開始遊戲")
        game_area = await ctx.message.create_thread(name=f'{ctx.author.display_name} 的 WordleGame')
        row = emojis['empty'] * 5
        game = await game_area.send(f'{row}\n'*5, embed=embed)
        await game.add_reaction(W)

        try:
            await self.bot.wait_for(
                'reaction_add',
                check = lambda r, u:all([
                    u.id == ctx.author.id,
                    str(r) == W
                ]),
                timeout=20)
        except Timeout:
            await game_area.delete()
            return
        else:
            await game.clear_reactions()
        record = ''
        def get_result(guess):
            nonlocal record
            guess = str(guess).upper()
            result = []
            for i in range(5):
                char = guess[i]
                status = (char == answer[i]) + (char in answer)
                record += '⬛🟨🟩'[status]
                result.append(emojis[ char + 'cba'[status] ])
            record += '\n'
            return ''.join(result)

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
                            m.content.upper() in words,
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
                print('awa')
                e = Embed(title = f'正確答案: {answer}')
                break
        
        set_author(e)
        await game.edit(embed = e)

        await sleep(10)
        await game_area.delete()
def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))