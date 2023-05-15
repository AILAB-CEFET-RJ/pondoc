import logging
from bs4 import BeautifulSoup
import requests

def htmlInfos(url):
    file = requests.get(url).content
    content = BeautifulSoup(file, 'html.parser')

    works = content.findAll('tr')

    infos=[]
    for work in works:
        tdElement = work.select('td')[1]
        td: str = tdElement.text
        b = tdElement.select('b')[0].text
        for char in range(len(td)):
            try:
                if td[char] == '[':
                    text = str(td[:char-11].strip()+ ' ' + td[char+113:].strip() + '.')
                    part1, part2 = text.split(b)
                    if part1 is None or part2 is None or b is None:
                        logging.critical('Error in split citation')
                    splitted_citation = (part1, b, part2,)
                    infos.append(splitted_citation)
            except ValueError as ex:
                logging.error('Error in split citation')
                logging.error(td)
                logging.error(ex)

    
    return infos