from flask import Flask, make_response, render_template, flash, redirect, url_for
from cStringIO import StringIO
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt

from pandas.io.sql import read_sql
import pandas as pd

from app import app
from .forms import TextboxForm

import sys
sys.path.append('../')
from fns import *
engine, conn, metadata = connect()
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select
db_connection = conn
metadata.reflect()
big_t = metadata.tables['pricedata_t1']





@app.route('/')
def index():
    return render_template('home.html', title='Home')


@app.route('/plots', methods=['GET', 'POST'])
def tickerform():
    form = TextboxForm()
    if form.validate_on_submit():
        symbol=form.ticker
        #url = ''.join(("/plots/", str(symbol)))
        return redirect(url_for('plot', ticker=symbol.data))
    return render_template('enterticker.html',title='Enter Ticker', form=form)

@app.route('/plots/<ticker>')
def plot(ticker):
    query = select([big_t]).where(big_t.c.Ticker==ticker)
    df = read_sql(query, db_connection, index_col='Date')
    #df.date = pd.to_datetime(df.date)
    #df.set_index('date', inplace=True)
    #df = df.reindex(pd.date_range(min(df.index), max(df.index)), fill_value=0)

    plt.clf()
    plt.plot(df.Price)
    canvas = FigureCanvas(plt.gcf())
    output = StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response
