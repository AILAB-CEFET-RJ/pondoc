import logging
import psycopg2
import os 

class Database():
    # Função para criar conexão no banco
    #TODO: Carregar credencias via environment
    def conect_db(self):
        attempt = 0
        error = None
        while attempt < 5:
            try:
                db = psycopg2.connect(host='localhost',
                                      dbname='postgres',
                                      user='postgres',
                                      password='admin',
                                      port='5433')
                return db
            except Exception as e:
                error = e
                logging.info("Error: %s" % error)
                attempt += 1
        if attempt == 5 and error is not None:
            raise error
        return db

    # Função para criar ou dropar uma tabela no banco
    def create_drop_db(self, sql):
        con = self.conect_db()
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()

    # Função para inserir dados no banco
    def insert_delete_db(self, sql):
        con = self.conect_db()
        cur = con.cursor()
        try:
            cur.execute(sql)
            con.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.info("Error: %s" % error)
            con.rollback()
            cur.close()
            return 1
        cur.close()

    def consult_db(self, sql):
        con=self.conect_db()
        cur=con.cursor()
        cur.execute(sql)
        recset=cur.fetchall()
        registros=[]
        for rec in recset:
            registros.append(rec)
        con.close()
        return registros


db=Database()
