import os
import logging
from datetime import datetime
from .normalizer import normalizer
from .transcriber import insertData
from .scriptsdb import create_tables
from .reader import read_publications
from .analyzer import parsePublication
import traceback
logging.basicConfig(level=logging.DEBUG)


def log_traceback(ex, ex_traceback=None):
    if ex_traceback is None:
        ex_traceback = ex.__traceback__
    tb_lines = [ line.rstrip('\n') for line in
                 traceback.format_exception(ex.__class__, ex, ex_traceback)]
    # logging.error(tb_lines)

def main(beginYear: str, endYear: str):
    now = datetime.now()
    filename =str(int(now.timestamp())) + '.xlsx'
    # filename = 'source/app/core/producao.xlsx'
    logging.info(f"Gerando relatório:")
    logging.info(f"De: {beginYear}")
    logging.info(f"Até: {endYear}")
    logging.info(f"File Output: {filename}")

    period = []
    period.append(beginYear)
    period.append(endYear)
    resultsJournals, resultsConferences = [], []
    rJauthorsnorm, rCauthorsnorm, discauthorsJ, discauthorsC = [], [], [], []

    infosp, infosa, infosc = read_publications(int(period[0]), int(period[1])+1)

    errors_periodics = []
    errors_publications = []
    errors_conferences = []

    n_periodics = 0
    n_publications = 0
    n_conferences = 0

    for ano in range(int(period[0]), int(period[1])+1):

        number_of_errors_periodics = 0
        number_of_errors_publications = 0
        number_of_errors_conferences = 0
        n_periodics += len(infosp[ano]) 
        n_publications += len(infosa[ano]) 
        n_conferences += len(infosc[ano]) 

        logging.info(f'Tratando {len(infosp[ano])} dados de Periodicos - {ano}')
        for i in infosp[ano]:
            doc = result = dis = None
            try:
                result=parsePublication(i)
                resultsJournals.append(result)
                doc, dis=normalizer(result[0])
                rJauthorsnorm.append(doc)
                discauthorsJ.append(dis)
            except Exception as ex:
                errors_periodics.append(i)
                number_of_errors_periodics += 1
                if doc and doc in rJauthorsnorm:
                    rJauthorsnorm.remove(doc)
                if dis and dis in discauthorsJ:
                    discauthorsJ.remove(dis)
                if result and result in resultsJournals:
                    resultsJournals.remove(result)
                logging.error('Error in citation: %s', i)
                log_traceback(ex)

        logging.info(f'Tratando {len(infosa[ano])} dados de Publicações Aceitas - {ano}')
        for i in infosa[ano]:
            try:
                result=parsePublication(i)
                resultsJournals.append(result)
                doc, dis=normalizer(result[0])
                rJauthorsnorm.append(doc)
                discauthorsJ.append(dis)
            except Exception as ex:
                number_of_errors_publications += 1
                errors_publications.append(i)
                if doc and doc in rJauthorsnorm:
                    rJauthorsnorm.remove(doc)
                if dis and dis in discauthorsJ:
                    discauthorsJ.remove(dis)
                if result and result in resultsJournals:
                    resultsJournals.remove(result)
                logging.error('Error in citation: %s', i)
                log_traceback(ex)


        logging.info(f'Tratando {len(infosc[ano])} dados de  Conferências - {ano}')
        for i in infosc[ano]:
            try:
                result=parsePublication(i)
                resultsConferences.append(result)
                doc, dis=normalizer(result[0])
                rCauthorsnorm.append(doc)
                discauthorsC.append(dis)
            except Exception as ex:
                errors_conferences.append(i)
                number_of_errors_conferences += 1
                if doc and doc in resultsConferences:
                    resultsConferences.remove(doc)
                if dis and dis in discauthorsC:
                    discauthorsC.remove(dis)
                if result and result in resultsJournals:
                    resultsJournals.remove(result)
                logging.error('Error in citation: %s', i)
                log_traceback(ex)
        
    logging.debug("Erros em publicações aceitas: %s", str(number_of_errors_publications))
    logging.debug("Erros em conferencias: %s", str(number_of_errors_conferences))
    logging.debug("Erros em periódicos: %s", str(number_of_errors_periodics))
    logging.info('Inserindo dados...')

    try:
        with open('errors.txt', 'w') as file:
            lists = [
                {'name': '############# Periodics #############', 'errors': errors_periodics, 'total': n_periodics},
                {'name': '############# Publications #############', 'errors': errors_publications, 'total': n_publications},
                {'name': '############# Conferences #############', 'errors': errors_conferences, 'total': n_conferences}]
            for lst in lists:
                file.write(lst['name'] + '\n\n')
                for i in lst['errors']:
                    file.write(' '.join(i) + '\n')
                    file.write('\n\n')
                total_errors = len(lst['errors'])
                total_citations = lst['total']
                file.write('Number of citations: ' + str(total_citations) + '\n')
                file.write('Number of errors: ' + str(total_errors) + '\n')
                per = str(((total_errors/total_citations)*100))
                file.write('Citation with error percentage: ' + per + '%\n')
                file.write('\n')
                file.write('\n')
    except Exception:
        pass
    insertData(period, filename, rJauthorsnorm, resultsJournals,
               discauthorsJ, rCauthorsnorm, resultsConferences, discauthorsC)
    return filename

