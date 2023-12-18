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
        try:
            char = td.rindex('[')
            if td[char] == '[':
                text = str(td[:char-11].strip()+ ' ' + td[char+113:].strip() + '.')
                part1, part2 = text.split(b)
                if part1 is None or part2 is None or b is None:
                    print('Error in split citation')
                splitted_citation = (part1, b, part2,)
                infos.append(splitted_citation)
        except ValueError as ex:
            print('Error in split citation')
            print(td)
            print(ex)

    return infos

def read_publications(beginYear, endYear):
    infosp = dict()
    infosa = dict()
    infosc = dict()

    for ano in range(beginYear, endYear+1):
        print(f'Downloading publications of year {ano}...')
        infosp[ano] = htmlInfos(
            str(f'https://eic.cefet-rj.br/lattes/ppcic-{ano}/PB0-0.html'))
        infosa[ano] = htmlInfos(
            str(f'https://eic.cefet-rj.br/lattes/ppcic-{ano}/PB7-0.html'))
        infosc[ano] = htmlInfos(
            str(f'https://eic.cefet-rj.br/lattes/ppcic-{ano}/PB4-0.html'))

    return infosp, infosa, infosc
