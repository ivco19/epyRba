from io import StringIO

import pandas as pd

from flask import Flask, render_template, make_response

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route('/download_csv')
def download_csv():
    si = StringIO()

    df = pd.read_csv("/home/juan/proyectos/arcolib19/src/databases/cases.csv")
    df.to_csv(si)

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output



app.run(port=5000)
