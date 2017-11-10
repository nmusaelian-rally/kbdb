import os
import pandas as pd
import psycopg2
from datetime import datetime
import pandas_datareader.data as web
import sqlalchemy

def connect():
    dburi = os.environ['DATABASE_URL']
    path = dburi.split('://')[1]
    user, password = path.split('@')[0].split(':')
    host, dbname = path.split('@')[1].split('/')
    host, port = host.split(':')
    conn = psycopg2.connect(database=dbname, user=user, password=password, host=host, port=port)
    print("Opened database successfully")
    sql = "SELECT date from snp500 order by id desc limit 1;"
    cursor = conn.cursor()
    cursor.execute(sql)
    last_date = cursor.fetchone()[0]
    return conn, last_date

def disconnect(conn):
    print("Closing database connection")
    conn.close()


def getCurrentData(start):
    today = datetime.today().strftime('%Y-%m-%d')
    end   = today

    snp500 = web.DataReader('SP500', "fred", start, end)
    snp500.dropna(inplace=True)
    snp500.reset_index(inplace=True)
    snp500.columns = [c.lower() for c in snp500.columns]
    return snp500

def appendTable(df, table_name):
    engine = sqlalchemy.create_engine(os.environ['DATABASE_URL'])
    df.to_sql(table_name, engine, index=False, if_exists='append')

conn, last_date = connect()
disconnect(conn)

today = datetime.today().strftime('%Y-%m-%d')
if str(last_date).split()[0] != today:
    next_date = last_date + pd.DateOffset(days=1)
    next_date_str = str(next_date).split()[0]
    print("--------")
    print (next_date_str)
    current = getCurrentData(next_date_str)
    if not current.empty:
        print(current.head(1))
        print(current.tail(1))
        appendTable(current, 'snp500')
    else:
        print("Nothing to append")
else:
    print("A row for %s already exist" % str(last_date))

