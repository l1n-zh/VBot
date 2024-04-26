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
            detections.append((word, words_tw[i],))

    if detections:
        correction = ''
        for detection in detections:
            word_cn, word_tw = detection
            correction += f'~~{word_cn}~~ -> {word_tw}\n'
        embed = Embed(title='⚠️⚠️ 支語警告 ⚠️⚠️')
        embed.add_field(name=f'💥 偵測到 {len(detections)} 個支語', value=correction)
        embed.set_image(url=choice(image_urls))
        embed.set_footer(text='⛔ 支語禁止 ⛔')
        return embed
