from .ZeroJudgeFormatter import ZeroJudgeFormatter
from .Parser import parse

class RyanJudgeFormatter(ZeroJudgeFormatter):

    url = r'ryanjudge.servebeer.com/ShowProblem?problemid='
    index_pattern = r'[a-h]\d{3}'

    def get_tags(self) -> str:
        content = self.soup.find('span', class_ = 'tag')
        res = ''
        for a in content.find_all('a'):
            link = 'http://ryanjudge.servebeer.com' + a['href'][1:]
            res += f'[{ a.string }]({ link })  '
        return res