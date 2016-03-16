from flask import Flask, make_response
from cStringIO import StringIO
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt

from pandas.io.sql import read_sql
import pandas as pd

from sqlalchemy import create_engine

engine = create_engine('postgresql://ljrconnell:rocco1!1@liamsdatabase.cbjwfk4y5vix.us-east-1.rds.amazonaws.com:5432/firstdb')

conn = engine.connect()     #do I need this?

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

metadata = MetaData(bind=engine)     #bind = engine?


app = Flask(__name__)

db_connection = conn

@app.route('/')
def index():
    return """\
<html>
<body>
<img src="/plot.png">
</body>
</html>"""

@app.route('/plot.png')
def plot():
    query = """\
SELECT * FROM ibmtest
"""
    df = read_sql(query, db_connection, index_col='Date')
    #df.date = pd.to_datetime(df.date)
    #df.set_index('date', inplace=True)
    #df = df.reindex(pd.date_range(min(df.index), max(df.index)), fill_value=0)

    plt.plot(df)
    canvas = FigureCanvas(plt.gcf())
    output = StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


if __name__ == '__main__':
    app.run(host=app.config.get("HOST", "ec2-52-90-86-30.compute-1.amazonaws.com"),
        port=app.config.get("PORT", 8888),
        debug=True)

