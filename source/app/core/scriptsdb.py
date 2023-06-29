import json
import os
from .database import db
import csv
from unidecode import unidecode

def create_tables():
    tables = ['researchers', 'students', 'qualis']

    # Dropando a tabelas caso elas já existam
    for table in tables:
        db.create_drop_db(f'DROP TABLE IF EXISTS {table}')

    # Criando a tabelas
    db.create_drop_db('''CREATE TABLE researchers( 
                    nome                VARCHAR(255), 
                    referencia          VARCHAR(50),
                    PRIMARY KEY (nome, referencia)
                    )''')

    db.create_drop_db('''CREATE TABLE students( 
                    nome                VARCHAR(255), 
                    referencia          VARCHAR(50),
                    PRIMARY KEY (nome, referencia)
                    )''')

    db.create_drop_db('''CREATE TABLE qualis(
                    issn          VARCHAR(9), 
                    nome          VARCHAR(255), 
                    qualis        VARCHAR(2),
                    PRIMARY KEY (issn, nome)
                    )''')

    # inserindo dados na tabela
    # researchers
    basePath = os.path.dirname(os.path.abspath(__file__))
    with open(f'{basePath}/PPCICresearchers.json', encoding='utf-8') as arq:
        researchers = json.load(arq)

        for researcher in researchers:
            for citations in researchers[researcher]:
                db.insert_delete_db(
                    f"INSERT INTO researchers (nome, referencia) VALUES ('{unidecode(researcher).upper()}', '{unidecode(citations).upper()}')")

    # students
    with open(f'{basePath}/discentes.csv', encoding='utf-8') as arq:
        discentes = csv.reader(arq)
        'INSERT INTO table_name (column_list) VALUES (value_list_1), (value_list_2), (value_list_n)'
        for line in discentes:
            if 'nome' not in line:
                db.insert_delete_db(
                    f"INSERT INTO students (nome, referencia) VALUES ('{unidecode(line[0]).upper()}', '{unidecode(line[1]).upper()}')")
                db.insert_delete_db(
                    f"INSERT INTO students (nome, referencia) VALUES ('{unidecode(line[0]).upper()}', '{unidecode(line[2]).upper()}')")
    # qualis
    with open(f'{basePath}/qualis.csv', encoding='utf-8') as arq:
        qualis = csv.reader(arq)
        LIMIT = 1000
        rows = []
        for line in qualis:
            if 'ISSN' in line or len(unidecode(line[0]).upper()) > 8:
                continue
            line[1] = line[1].replace("'", '')
            rows.append(f"('{unidecode(line[0]).upper()}', '{unidecode(line[1])}', '{unidecode(line[2])}')")
            if len(rows)  == LIMIT:
                values = ''
                for row in rows:
                    values += row + ','
                values = values[:len(values)-1]
                db.insert_delete_db(
                    f"INSERT INTO qualis (issn, nome, qualis) VALUES {values}")
                rows = []
