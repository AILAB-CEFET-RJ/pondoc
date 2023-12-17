from io import BytesIO
import logging
from flask import Flask, render_template, request, send_file

from main import main

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/report")
def download_report():
    try:
        begin_year = int(request.args.get('beginYear'))
        end_year = int(request.args.get('endYear'))

        # Validate
        def validate_year(yyyy: int) -> bool:
            if not (2012 < yyyy < 3000):
                return True
            return False

        if validate_year(begin_year) or validate_year(end_year) or begin_year > end_year:
            return 'Invalid input'
        
        # Generate report
        excel_data = BytesIO()
        main(list(range(begin_year, end_year + 1))).save(excel_data)
        excel_data.seek(0)

    except Exception as error:
        logging.debug((begin_year,end_year))
        logging.error(error)
        return 'Error, please check your inputs.'

    return send_file(
        excel_data,
        as_attachment=True,
        download_name=f'report-{begin_year}-{end_year}.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
