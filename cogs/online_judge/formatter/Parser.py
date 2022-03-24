from bs4 import element


def parse(content: element.Tag) -> str:
    return _parse(content)


def _parse(content: element.Tag):
    res = ""
    contents = content.children
    for elem in contents:
        
        if isinstance(elem, element.Tag):
            name = elem.name
            if name == 'br': res += '\n'
    
            elif name == 'table':
                res += '```'
                format = []
                for tr in elem.find_all('tr'):
                    content_lengths = []
                    th = tr.find('th')
                    content_lengths.append( len( parse(th) ) if th else 0 )
                    for td in tr.find_all('td'):
                        content_lengths.append( len( parse(td) ) )
                    format.append(content_lengths)
                frame = [max(lengths) for lengths in zip(*format)]

                for tr in elem.find_all('tr'):
                    if(frame[0]):
                        res += f"**{ tr.find('th').text.ljust( frame[0], ' ' ) }** "
                    for i, td in enumerate( tr.find_all('td') ):
                        res += td.text.ljust( frame[i+1], ' ' ) + ' '
                    res += '\n'
                res += '```\n'

            elif name.startswith('h') or name == 'strong':
                res += f'**{ elem.text }**'

            else: res += parse(elem)+'\n\u200b'

        elif isinstance(elem, str):
            res += elem.string

    if not contents:
        res += content.string or ''

    return res