from .normalizer import normalizer
from .reader import htmlInfos
from .scriptsdb import create_tables
from .transcriber import insertData
from .analyzer import parsePublication
import argparse
import logging
from .database import db
logging.basicConfig(level=logging.DEBUG)

# TODO: Criar o report não deve ser responsabilidade do main, e sim de um serviço
def main(beginYear: str, endYear: str):

    # TODO: Permitir mais de um arquivo sendo salvo por vez
    file = 'report'
    logging.info(f"Gerando relatório:")
    logging.info(f"De: {beginYear}")
    logging.info(f"Até: {endYear}")
    logging.info(f"File Output: {file}")

    period = []
    period.append(beginYear)
    period.append(endYear)
    resultsJournals, resultsConferences = [], []
    rJauthorsnorm, rCauthorsnorm, discauthorsJ, discauthorsC = [], [], [], []

    for ano in range(int(period[0]), int(period[1])+1):
        infosp = htmlInfos(
            str(f'https://eic.cefet-rj.br/lattes/ppcic-{ano}/PB0-0.html'))
        infosa = htmlInfos(
            str(f'https://eic.cefet-rj.br/lattes/ppcic-{ano}/PB7-0.html'))
        infosc = htmlInfos(
            str(f'https://eic.cefet-rj.br/lattes/ppcic-{ano}/PB4-0.html'))

        print(f'Tratando dados de Periodicos - {ano}')
        for i in infosp:
            result = parsePublication(i.upper())
            resultsJournals.append(result)
            doc, dis = normalizer(result[0])
            rJauthorsnorm.append(doc)
            discauthorsJ.append(dis)

        print(f'Tratando dados de Publicações Aceitas - {ano}')
        for i in infosa:
            result = parsePublication(i.upper())
            resultsJournals.append(result)
            doc, dis = normalizer(result[0])
            rJauthorsnorm.append(doc)
            discauthorsJ.append(dis)

        print(f'Tratando dados de Conferência - {ano}')
        for i in infosc:
            result = parsePublication(i.upper())
            resultsConferences.append(result)
            doc, dis = normalizer(result[0])
            rCauthorsnorm.append(doc)
            discauthorsC.append(dis)

    print('Inserindo dados...')
    insertData(period, file, rJauthorsnorm, resultsJournals,
               discauthorsJ, rCauthorsnorm, resultsConferences, discauthorsC)
        #TODO: Inserir dados também no banco postgres