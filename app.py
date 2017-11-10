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
import pandas_datareader.data as web
from datetime import datetime


# def connect_db():
#     dburi = os.environ['DATABASE_URL']
#     path = dburi.split('://')[1]
#     user, password = path.split('@')[0].split(':')
#     host, dbname = path.split('@')[1].split('/')
#     host, port   = host.split(':')
#     conn = psycopg2.connect(database=dbname, user=user, password=password, host=host, port=port)
#     print("Opened database successfully")
#     populateFromCSV(conn, 'snp500', 'data/snp500dump.csv')
#     conn.close()
#
# def populateFromCSV(conn, table_name, csv_file):
#     f = open(csv_file, 'r')
#     next(f)
#     conn.cursor().copy_from(f, table_name, columns=('date', 'sp500'), sep=',')
#     conn.commit()
#
#
#
#
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# app.debug = True
# connect_db()


app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/t-yield-delta')
def bokeh():
    start = '2000-01-01'
    # we are going to match results with the dates of two latest recessions:
    # March-November 2001 Recession and December 2007 - June 2009  Recession
    # so January of 2000 seems like a good date to start

    today = datetime.today().strftime('%Y-%m-%d')
    t_yields = web.DataReader(['GS3M', 'GS10'], "fred", start, today)
    old_column_names = ['GS3M', 'GS10']
    new_column_names = ['3MonthRate', '10YearRate']
    name_map = dict(zip(old_column_names, new_column_names))
    t_yields.rename(columns=name_map, inplace=True)
    for index, row in t_yields.iterrows():
        t_yields.loc[index, 'Difference'] = t_yields.loc[index, '10YearRate'] - t_yields.loc[index, '3MonthRate']


    ds = ColumnDataSource(t_yields)
    title = "Yield difference between 10-Year and 3-Month Treasurys"
    fig = figure(plot_width=800,
                 plot_height=600,
                 x_axis_label = "Date",
                 y_axis_label = "Delta",
                 x_axis_type="datetime",
                 title = title)
    fig.xaxis[0].ticker.desired_num_ticks = 10
    fig.add_tools(HoverTool(tooltips=[("DATE", "@x{%F}"),("Treasurys 10YearRate - 3MonthRate", "@y{0.00 a}")],
                            formatters={"x": "datetime"}))
    fig.line(ds.data['DATE'],ds.data['Difference'], line_color="green", legend="delta")
    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)
    html = render_template(
        'yield.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)

if __name__ == '__main__':
    app.run()
