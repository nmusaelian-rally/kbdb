import os
import psycopg2


def connect_db():
    dburi = os.environ['DATABASE_URL']
    path = dburi.split('://')[1]
    user, password = path.split('@')[0].split(':')
    host, dbname = path.split('@')[1].split('/')
    host, port   = host.split(':')
    conn = psycopg2.connect(database=dbname, user=user, password=password, host=host, port=port)
    print("Opened database successfully")
    populateFromCSV(conn, 'snp500', 'data/snp500dump.csv')
    conn.close()

def populateFromCSV(conn, table_name, csv_file):
    f = open(csv_file, 'r')
    next(f)
    conn.cursor().copy_from(f, table_name, columns=('date', 'sp500'), sep=',')
    conn.commit()

connect_db()