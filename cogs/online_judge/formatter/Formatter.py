from typing import List


class Formatter:

    url = ''
    index_pattern = ''

    def __init__(self, soup):
        self.soup = soup


    def get_title(self) -> str:
        pass


    def get_statistics(self) -> str:
        pass


    def get_content(self) -> str:
        pass


    def get_theinput(self) -> str:
        pass


    def get_theoutput(self) -> str:
        pass


    def get_examples(self) -> List[str]:
        pass


    def get_note(self) -> str:
        pass