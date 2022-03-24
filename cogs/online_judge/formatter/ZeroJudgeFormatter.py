from typing import List
from .Formatter import Formatter
from .Parser import parse


class ZeroJudgeFormatter(Formatter):
    url = r'zerojudge.tw/ShowProblem?problemid='
    index_pattern = r'[a-h]\d{3}'

    def get_title(self) -> str:
        content = self.soup.find('span', id='problem_title')
        return parse(content)


    def get_statistics(self) -> str:
        content = self.soup.find('span',title='解題統計')
        accepted, _, submission, persentage = content.stripped_strings
        persentage = ''.join(persentage.split())
        return f'通過比率: `{accepted}/{submission}` `{persentage}`'


    def get_content(self) -> str:
        content = self.soup.find('div', id='problem_content')
        return parse(content)


    def get_theinput(self) -> str:
        content = self.soup.find('div', id='problem_theinput')
        return parse(content)


    def get_theoutput(self) -> str:
        content = self.soup.find('div', id='problem_theoutput')
        return parse(content)
    

    def get_tags(self) -> str:
        content = self.soup.find('span', class_ = 'tag')
        res = ''
        for a in content.find_all('a'):
            link = 'https://zerojudge.tw' + a['href'][1:]
            res += f'[{ a.string }]({ link })  '
        return res


    def get_examples(self) -> List[str]:
        contents = [ elem.string for elem in self.soup.find_all('pre') ]
        examples = []
        while contents:
            examples.append(contents[:2])
            contents = contents[2:]
        return examples


    def get_note(self) -> str:
        content = self.soup.find('div', id='problem_hint')
        return parse(content)