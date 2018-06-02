import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.models import ColumnDataSource, SingleIntervalTicker, LinearAxis
from bokeh.models import HoverTool
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime

from append_table import update
from lows import getLows
from scenarios import timing
from read_coins import coins, getInitialOneYearDataDump

import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db is imported in manage.py
db = SQLAlchemy(app)
app.debug = True


@app.route('/')
def index():
    return render_template('index.html')


def connect():
    dburi = os.environ['DATABASE_URL']
    path = dburi.split('://')[1]
    user, password = path.split('@')[0].split(':')
    host, dbname = path.split('@')[1].split('/')
    host, port = host.split(':')
    conn = psycopg2.connect(database=dbname, user=user, password=password, host=host, port=port)
    print("Opened database successfully")
    return conn

def readSQL(tbl, conn):
    sql = 'select * from %s' % tbl
    df = pd.read_sql(sql, con=conn)
    return df


def disconnect(conn):
    print("Closing database connection")
    conn.close()

@app.route('/sp')
def buildSP500Chart():
    table_name = 'snp500'

    update(table_name)
    conn = connect()
    sp = readSQL(table_name, conn)
    lows, last_record = getLows(sp)
    disconnect(conn)

    ds = ColumnDataSource(sp)

    start = '2007-09-28'
    today = datetime.today().strftime('%Y-%m-%d')
    recessions = web.DataReader('USRECM', "fred", start, today)

    ds2 = ColumnDataSource(recessions)

    title = "SP500"
    fig = figure(plot_width   = 800,
                 plot_height  = 600,
                 x_axis_label = "Date",
                 y_axis_label = "SP500",
                 x_axis_type  = "datetime",
                 title = title)
    fig.xaxis[0].ticker.desired_num_ticks = 10
    fig.add_tools(HoverTool(tooltips=[("date", "@x{%F}"),("sp500", "@y{0.00}")],
                            formatters={"x": "datetime"}, names=['sp']))
    fig.add_tools(HoverTool(tooltips=[("DATE", "@x{%F}")],
                            formatters={"x": "datetime"}, names=['recession-dates']))
    fig.line(ds.data['date'],ds.data['sp500'], line_color="green", legend="sp500", name='sp')
    fig.line(ds2.data['DATE'], ds2.data['USRECM']*1000,  line_color="red",   legend="recession", name='recession-dates')
    fig.legend.location = "top_left"

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(fig)

    lows_html = lows.to_html(classes=["table table-bordered", "table table-striped", "table table-nonfluid"])

    html = render_template(
        'sp.html',
        data = lows_html,
        length = lows.shape[0],
        start  = start,
        last_record = last_record,
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)

@app.template_filter()
def stringifier(value):
    return str(value).split()[0]

app.jinja_env.filters['stringifier'] = stringifier

@app.route('/yield')
def buildYieldChart():
    start = '2000-01-01'
    # match results with the dates of two latest recessions:
    # March-November 2001 Recession and December 2007 - June 2009  Recession
    # January of 2000 seems like a good date to start

    today = datetime.today().strftime('%Y-%m-%d')
    t_yields = web.DataReader(['GS3M', 'GS10'], "fred", start, today)
    old_column_names = ['GS3M', 'GS10']
    new_column_names = ['3MonthRate', '10YearRate']
    name_map = dict(zip(old_column_names, new_column_names))
    t_yields.rename(columns=name_map, inplace=True)
    for index, row in t_yields.iterrows():
        t_yields.loc[index, 'Difference'] = t_yields.loc[index, '10YearRate'] - t_yields.loc[index, '3MonthRate']

    ds = ColumnDataSource(t_yields)

    recessions = web.DataReader('USRECM', "fred", start, today)

    ds2 = ColumnDataSource(recessions)

    title = "Yield difference between 10-Year and 3-Month Treasurys"
    fig = figure(plot_width   = 800,
                 plot_height  = 600,
                 x_axis_label = "Date",
                 y_axis_label = "Delta",
                 x_axis_type  = "datetime",
                 title = title)
    fig.xaxis[0].ticker.desired_num_ticks = 10
    fig.add_tools(HoverTool(tooltips=[("DATE", "@x{%F}"),("10Y Rate - 3M Rate", "@y{0.00 a}")],
                            formatters={"x": "datetime"}, names=['rate-delta']))
    fig.add_tools(HoverTool(tooltips=[("DATE", "@x{%F}")],
                            formatters={"x": "datetime"}, names=['recession-dates']))
    fig.line(ds.data['DATE'],ds.data['Difference'], line_color="green", legend="delta", name='rate-delta')
    fig.line(ds2.data['DATE'], ds2.data['USRECM'],  line_color="red",   legend="recession", name='recession-dates')

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(fig)
    html = render_template(
        'yield.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)

@app.route('/scenarios')
def buildTimingScenarios():
    df = pd.read_csv('data/timing.csv', index_col=0)
    tdf = timing(df)
    tdf_html = tdf.to_html(classes=["table table-bordered", "table table-striped", "table table-nonfluid"])
    html = render_template(
        'scenarios.html',
        data=tdf_html
    )
    return encode_utf8(html)

# Commented out due to error because of the change in the api:
#sqlalchemy.exc.ProgrammingError: (psycopg2.ProgrammingError) column "open*" of relation "burst" does not exist
#LINE 1: INSERT INTO burst (date, "open*", high, low, "close**", volu...
# @app.route('/coins')
# def buildCoinData():
#     #------initial data dump is done once------
#     #for coin in coins:
#         #getInitialOneYearDataDump(coin)
#     #-------------------------------------------
#
#     def getCurrentDetails(coin):
#         url = 'https://api.coinmarketcap.com/v1/ticker/%s/' % coin
#         r = requests.get(url)
#         return r.json()
#
#     conn = None
#     page_components = []
#     current_objects = []
#     # for coin in coins:
#     #     update(coin)
#     for idx, coin in enumerate(coins):
#         update(coin)
#         if idx == 0:
#             conn = connect()
#         df = readSQL(coin, conn)
#         ds = ColumnDataSource(df)
#         if idx == len(coins) - 1:
#             disconnect(conn)
#
#         title = coin
#         fig = figure(plot_width=600,
#                      plot_height=300,
#                      x_axis_label="Date",
#                      y_axis_label="Closing Price",
#                      x_axis_type="datetime",
#                      title=title)
#         fig.xaxis[0].ticker.desired_num_ticks = 10
#
#         fig.line(ds.data['date'], ds.data['close'], name=coin)
#
#         # volume returns ???
#         # fig.add_tools(HoverTool(tooltips=[("date", "@x{%F}"), ("close", "@y{0.00}"), ("volume", "@volume")],
#         #                         formatters={"x": "datetime"}, names=[coin]))
#
#         fig.add_tools(HoverTool(tooltips=[("date", "@x{%F}"), ("close", "@y{0.00}")],
#                                 formatters={"x": "datetime"}, names=[coin]))
#
#         script, div = components(fig)
#         page_components.append((script, div))
#         current_objects.append(getCurrentDetails(coin))
#
#     js_resources = INLINE.render_js()
#     css_resources = INLINE.render_css()
#
#
#
#     html = render_template(
#         'coins.html',
#         plot_script0=page_components[0][0],
#         plot_div0=page_components[0][1],
#         plot_script1=page_components[1][0],
#         plot_div1=page_components[1][1],
#         plot_script2=page_components[2][0],
#         plot_div2=page_components[2][1],
#         plot_script3=page_components[3][0],
#         plot_div3=page_components[3][1],
#         current=current_objects,
#         js_resources=js_resources,
#         css_resources=css_resources
#     )
#
#     return encode_utf8(html)

if __name__ == '__main__':
    app.run()
