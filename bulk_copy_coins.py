import os
import psycopg2

from read_coins import coins

def connect_db():
    dburi = os.environ['DATABASE_URL']
    path = dburi.split('://')[1]
    user, password = path.split('@')[0].split(':')
    host, dbname = path.split('@')[1].split('/')
    host, port   = host.split(':')
    conn = psycopg2.connect(database=dbname, user=user, password=password, host=host, port=port)
    print("Opened database successfully")
    for coin in coins:
        populateFromCSV(conn, coin, 'data/%s.csv' %coin)
    conn.close()

def populateFromCSV(conn, table_name, csv_file):
    f = open(csv_file, 'r')
    next(f)
    copy_command = "COPY %s (date,open,high,low,close,volume,marketcap) FROM STDIN NULL '' DELIMITER ',' CSV;" % table_name
    conn.cursor().copy_expert(copy_command, f)
    #conn.cursor().copy_from(f, table_name, columns=('date','open','high','low','close','volume','marketcap'), sep=',')
    #sql = "ALTER TABLE %s ADD PRIMARY KEY (%s);" % (table_name, 'date')
    #conn.cursor().execute(sql)
    conn.commit()
    f.close()
connect_db()