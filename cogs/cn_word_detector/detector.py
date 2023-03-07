from discord import Embed
from random import choice
from pathlib import Path

path = Path(__file__).parent / "assets/"


with (path/'tw.txt').open(encoding='utf-8') as f:
    words_tw = f.read().split('\n')

with (path/'cn.txt').open(encoding='utf-8') as f:
    words_cn = f.read().split('\n')

with (path/'image_urls.txt').open(encoding='utf-8') as f:
    image_urls = f.read().split('\n')


def detect_cn_words(content):
    detections = []
    for i, word in enumerate(words_cn):
        if word in content:
            detections.append((word, content.find(word), words_tw[i],))

    if detections:
        alert = ''
        correction = ''
        for detection in detections:
            word_cn, position, word_tw = detection
            position_end = position+len(word_cn)
            alert += f'{content[max(0, position-3):position]}**{content[position:position_end]}**{content[position_end:position_end+3]}\n'
            correction += f'~~{word_cn}~~ -> {word_tw}\n'
        embed = Embed(title='⚠️⚠️支語警告⚠️⚠️', description=alert)
        embed.add_field(name="請使用正確詞彙", value=correction)
        embed.set_image(url = choice(image_urls))
        return embed

