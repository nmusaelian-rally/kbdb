import os
import pandas as pd
import psycopg2
from datetime import datetime
import pandas_datareader.data as web
import sqlalchemy

from read_coins import coins, getCurrentCoinData

def connect(table_name):
    dburi = os.environ['DATABASE_URL']
    path = dburi.split('://')[1]
    user, password = path.split('@')[0].split(':')
    host, dbname = path.split('@')[1].split('/')
    host, port = host.split(':')
    conn = psycopg2.connect(database=dbname, user=user, password=password, host=host, port=port)
    print("Opened database successfully")
    sql = "SELECT date from %s order by id desc limit 1;" % table_name
    cursor = conn.cursor()
    cursor.execute(sql)
    last_date = cursor.fetchone()[0]
    return conn, last_date

def disconnect(conn):
    print("Closing database connection")
    conn.close()


def getCurrentData(table_name, start):
    df = None
    today = datetime.today().strftime('%Y-%m-%d')
    end   = today

    if table_name == 'snp500':
        df = web.DataReader('SP500', "fred", start, end)

    elif table_name in coins:
        df = getCurrentCoinData(table_name, start, end)

    df.dropna(inplace=True)
    df.reset_index(inplace=True)
    df.columns = [c.lower() for c in df.columns]
    return df

def appendTable(df, table_name):
    engine = sqlalchemy.create_engine(os.environ['DATABASE_URL'])
    df.to_sql(table_name, engine, index=False, if_exists='append')

def update(table_name):
    conn, last_date = connect(table_name)
    disconnect(conn)

    today = datetime.today().strftime('%Y-%m-%d')
    if str(last_date).split()[0] != today:
        next_date = last_date + pd.DateOffset(days=1)
        next_date_str = str(next_date).split()[0]
        print("--------")
        print(next_date_str)
        current = getCurrentData(table_name,next_date_str)
        if not current.empty:
            print(current.head(1))
            print(current.tail(1))
            appendTable(current, table_name)
        else:
            print("Nothing to append")
    else:
        print("A row for %s already exist" % str(last_date))
