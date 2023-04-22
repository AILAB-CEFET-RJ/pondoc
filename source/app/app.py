import os
from core.main import main
from core.scriptsdb import create_tables
from flask import Flask, render_template, request, abort
from flask_cors import CORS

create_tables()
app = Flask(__name__)
CORS(app)

#TODO: Listar relatóis para baixar
@app.route("/")
def index():
    return render_template('createReport.html', api_url=os.getenv('APP_PUBLIC_URL'))

#TODO: Criar estrutura de dados
@app.route("/createReport", methods=['POST'])
def createReport():
    body: dict = request.get_json()
    if not body.get('beginYear') or not body.get('endYear'):
        abort(400, "Especifique uma data.")
    return main(body.get('beginYear'), body.get('endYear'))


if __name__ == "__main__":
    app.run()
