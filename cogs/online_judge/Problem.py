from urllib.error import URLError
import requests
from bs4 import BeautifulSoup
from .formatter.Formatter import Formatter
from typing import Type
import re


class Problem:
    def __init__(self, arg: str, F: Type[Formatter]):
        url_pattern = F.url.replace('?', '\?')
        pattern = rf'((http|https)://)?(www.)?({url_pattern})?({F.index_pattern})$'
        
        if re.match(pattern, arg):
            index = re.match(pattern, arg).group(5)
        else:
            raise(URLError('Invalid URL'))

        self.url = f'http://{F.url}{index}'
        r = requests.get(self.url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            formatter = F(soup)

            self.title = formatter.get_title()
            self.statistics = formatter.get_statistics()
            self.content = formatter.get_content()
            self.theinput = formatter.get_theinput()
            self.theoutput = formatter.get_theoutput()
            self.tags = formatter.get_tags() or '\u200b'
            self.examples = formatter.get_examples()
            self.note = formatter.get_note() or '\u200b'

        else: print(r.status_code)
    
    
    def to_embed_dict(self) -> None:
        embed_dict = {}
        embed_dict['title'] = self.title
        embed_dict['description'] = self.statistics
        embed_dict['url'] = self.url
        fields = []
        add_field = lambda n, v, b = False: fields.append({ 'name':n, 'value':v,'inline':b })

        add_field('[內容]', self.content)
        add_field('[輸入]', self.theinput)
        add_field('[輸出]', self.theoutput)

        for i, example in enumerate(self.examples, 1):
            input, output = example
            add_field( f'範例輸入 {i:02d}', f'```{input}```', True)
            add_field( f'範例輸出 {i:02d}', f'```{output}```', True)
            add_field( '\u200b', '\u200b', False)

        add_field('[提示]', self.note)
        add_field('[標籤]', self.tags)
        embed_dict['fields'] = fields
        return embed_dict