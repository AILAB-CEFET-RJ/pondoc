import pandas as pd
import openpyxl
from transcriber import researchersCorrelation
rCauthorsnorm = [['JOEL ANDRE FERREIRA DOS SANTOS'], [], ['DIEGO NUNES BRANDAO'], ['DIEGO NUNES BRANDAO'], [], [], [], [], [], ['JOAO ROBERTO DE TOLEDO QUADROS'], [], [], [], ['RAFAELLI DE CARVALHO COUTINHO'], ['JORGE DE ABREU SOARES', 'RAFAELLI DE CARVALHO COUTINHO'], [], ['DIEGO NUNES BRANDAO'], ['DIEGO NUNES BRANDAO'], [], [], ['DIEGO BARRETO HADDAD', 'LAURA SILVA DE ASSIS'], ['GLAUCO FIOROTT AMORIM', 'JOEL ANDRE FERREIRA DOS SANTOS'], [], ['JORGE DE ABREU SOARES'], ['GLAUCO FIOROTT AMORIM'], [], [], [], ['LAURA SILVA DE ASSIS', 'EDUARDO BEZERRA DA SILVA', 'GUSTAVO PAIVA GUEDES E SILVA'], [
    'GUSTAVO PAIVA GUEDES E SILVA'], [], [], [], [], [], ['DIEGO BARRETO HADDAD'], ['DIEGO BARRETO HADDAD'], ['EDUARDO SOARES OGASAWARA'], ['EDUARDO SOARES OGASAWARA'], ['FELIPE DA ROCHA HENRIQUES'], ['JOEL ANDRE FERREIRA DOS SANTOS'], ['JOAO ROBERTO DE TOLEDO QUADROS', 'EDUARDO SOARES OGASAWARA'], ['DIEGO BARRETO HADDAD'], ['DIEGO BARRETO HADDAD'], [], [], ['DIEGO BARRETO HADDAD'], [], [], [], [], [], ['DIEGO BARRETO HADDAD'], [], ['RAFAELLI DE CARVALHO COUTINHO'], ['JOEL ANDRE FERREIRA DOS SANTOS'], [], [], [], [], ['EDUARDO SOARES OGASAWARA'], ['GLAUCO FIOROTT AMORIM', 'GUSTAVO PAIVA GUEDES E SILVA']]


def nextChar(char, offset=1) -> str:
    # converting chararacter to byte
    char = bytes(char, 'utf-8')
    s = bytes([char[0] + offset])
    s = str(s)
    return s


rJauthorsnorm = [[], [], [], ['JOEL ANDRE FERREIRA DOS SANTOS'], [], [], [
    'KELE TEIXEIRA BELLOZE', 'PEDRO HENRIQUE GONZALEZ SILVA'], ['KELE TEIXEIRA BELLOZE'], []]
wb = openpyxl.load_workbook(filename='source/app/core/producao.xlsx')


def addResearchersScore(wb: openpyxl.Workbook, authorsnorm: list, startCol='K', startrow=2):
    researchers = researchersCorrelation(authorsnorm)
    current_col = startCol
    for researcher in researchers:
        points = researchers[researcher]
        current_row = startrow
        if current_col != startCol:
            current_col = nextChar(current_col)
        for point in points:
            if point != '':
                wb[f'{current_col}{current_row}'] = point
            current_row = current_row + 1


addResearchersScore(wb['Conferencias'], rCauthorsnorm)
addResearchersScore(wb['Periodicos'], rJauthorsnorm)
wb.save('testfim.xlsx')
wb.close()
