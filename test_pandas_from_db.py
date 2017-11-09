import os
import pandas as pd
import psycopg2
from datetime import datetime
import pandas_datareader.data as web
import sqlalchemy

def connect(dbname):
    conn = psycopg2.connect(database=dbname, user="postgres", password="postgres", host="127.0.0.1", port="5432")
    print("Opened database successfully")
    return conn


def disconnect(conn):
    print("Closing database connection")
    conn.close()

def readSQL(table_name, conn):
    sql = 'select * from %s' %table_name
    df = pd.read_sql(sql, con=conn)

    # do this incrementally in chunks?
    #df = pd.DataFrame()
    #for chunk in pd.read_sql('select * from table_name', con=conn, chunksize=5000):
        #df = df.append(chunk)

    return df

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

conn = connect('kbdbf')
df = readSQL('snp500', conn)
disconnect(conn)
print(df.head(1))
print(df.tail(1))

last_date = df['date'].iloc[-1]
today = datetime.today().strftime('%Y-%m-%d')
if str(last_date).split()[0] != today:
    next_date = last_date + pd.DateOffset(days=1)
    next_date_str = str(next_date).split()[0]
    print("--------")
    print (next_date_str)
    current = getCurrentData(next_date_str)
    print(current.head(1))
    print(current.tail(1))
    appendTable(current, 'snp500')
else:
    print("A row for %s already exist" % str(last_date))

