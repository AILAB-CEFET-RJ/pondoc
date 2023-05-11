from datetime import datetime
from .normalizer import normalizer
from .reader import htmlInfos
from .scriptsdb import create_tables
from .transcriber import insertData
from .analyzer import parsePublication
import argparse
import traceback
import logging
from .database import db
from unidecode import unidecode
logging.basicConfig(level=logging.DEBUG)


def log_traceback(ex, ex_traceback=None):
    if ex_traceback is None:
        ex_traceback = ex.__traceback__
    tb_lines = [ line.rstrip('\n') for line in
                 traceback.format_exception(ex.__class__, ex, ex_traceback)]
    logging.error(tb_lines)

def main(beginYear: str, endYear: str):
    now = datetime.now()
    filename = '/report_%s.xlsx' % int(now.timestamp())
    logging.info(f"Gerando relatório:")
    logging.info(f"De: {beginYear}")
    logging.info(f"Até: {endYear}")
    logging.info(f"File Output: {filename}")

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
        number_of_errors_periodics = 0
        number_of_errors_publications = 0
        number_of_errors_conferences = 0

        logging.info(f'Tratando dados de Periodicos - {ano}')

        for i in infosp:
            doc = result = dis = None
            try:
                result=parsePublication(unidecode(i).upper())
                resultsJournals.append(result)
                doc, dis=normalizer(result[0])
                rJauthorsnorm.append(doc)
                discauthorsJ.append(dis)
            except Exception as ex:
                number_of_errors_periodics += 1
                if doc and doc in rJauthorsnorm:
                    rJauthorsnorm.remove(doc)
                if dis and dis in discauthorsJ:
                    discauthorsJ.remove(dis)
                if result and result in resultsJournals:
                    resultsJournals.remove(result)
                logging.error('Error in citation: %s', unidecode(i))
                log_traceback(ex)

        logging.info(f'Tratando dados de Publicações Aceitas - {ano}')
        for i in infosa:
            try:
                result=parsePublication(unidecode(i).upper())
                resultsJournals.append(result)
                doc, dis=normalizer(result[0])
                rJauthorsnorm.append(doc)
                discauthorsJ.append(dis)
            except Exception as ex:
                number_of_errors_publications += 1
                if doc and doc in rJauthorsnorm:
                    rJauthorsnorm.remove(doc)
                if dis and dis in discauthorsJ:
                    discauthorsJ.remove(dis)
                if result and result in resultsJournals:
                    resultsJournals.remove(result)
                logging.error('Error in citation: %s', unidecode(i))
                log_traceback(ex)


        logging.info(f'Tratando dados de Conferência - {ano}')
        for i in infosc:
            try:
                result=parsePublication(unidecode(i).upper())
                resultsConferences.append(result)
                doc, dis=normalizer(result[0])
                rCauthorsnorm.append(doc)
                discauthorsC.append(dis)
            except Exception as ex:
                number_of_errors_conferences += 1
                if doc and doc in resultsConferences:
                    resultsConferences.remove(doc)
                if dis and dis in discauthorsC:
                    discauthorsC.remove(dis)
                if result and result in resultsJournals:
                    resultsJournals.remove(result)
                logging.error('Error in citation: %s', unidecode(i))
                log_traceback(ex)
        
    logging.debug("Erros em publicações aceitas: %s", str(number_of_errors_publications))
    logging.debug("Erros em conferencias: %s", str(number_of_errors_conferences))
    logging.debug("Erros em periódicos: %s", str(number_of_errors_periodics))
    logging.info('Inserindo dados...')
    insertData(period, filename, rJauthorsnorm, resultsJournals,
               discauthorsJ, rCauthorsnorm, resultsConferences, discauthorsC)
    return filename
