from .database import db
import pandas as pd

# retorna lista com nome dos docentes e discentes que participaram normalizada. (SILVA, M. P. -> MARIA PEREIRA DA SILVA)


def normalizer(l):
    doc, dis = [], []
    for ref in l:
        surnameref = ref[0].strip() + ', '
        nameref = (surnameref + ' '.join(i.strip() for i in ref[1:])).upper().strip()
        docentes = pd.DataFrame(db.consult_db(
            "SELECT referencia FROM researchers"))
        for doc_ref in docentes[0]:
            if nameref == doc_ref:
                sql = f"SELECT nome FROM researchers WHERE referencia = '{doc_ref}'"
                fullname = db.consult_db(sql)[0][0]
                doc.append(fullname)

        discentes = pd.DataFrame(db.consult_db(
            "SELECT referencia FROM students"))
        for dis_ref in discentes[0]:
            if nameref == dis_ref:
                sql = f"SELECT nome FROM students WHERE referencia = '{dis_ref}'"
                fullname = db.consult_db(sql)[0][0]
                dis.append(fullname)

    return doc, ''.join(dis)
