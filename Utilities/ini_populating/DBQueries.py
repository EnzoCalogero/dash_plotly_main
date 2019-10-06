# -*- coding: utf-8 -*-
import psycopg2
import pandas as pd
from configparser import ConfigParser


def config(filename='technote.ini', section='postgresql'):
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            if param[0] == 'database':
                db[param[0]] = param[1].replace('-', '')
            else:
                db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def listDB():
    """
    Connect to the PostgreSQL database server
    and return the list of the available Customer Databases.
    """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()

        cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        output = cur.fetchall()
        # print(output)

        skipdb = ['postgres', 'tech_view_viewer', 'demo']
        listDB = []

        for db in output:
            if db[0] not in skipdb:
                listDB.append(db[0])
        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            return listDB


def dictDB():
    conn = None
    skipdb = ['postgres', 'tech_view_viewer', 'demo']
    DB_ = listDB()
    params = config()
    dizzDBs = dict()
    df = pd.DataFrame()
    for db in DB_:
        try:
            params['database'] = db
            conn = psycopg2.connect(**params)
            cur = conn.cursor()

            cur.execute("select licencee from licences where id = (select max (id) from licences);")
            output = cur.fetchone()
            if output[0] not in skipdb:
                cur.execute("select hostname from devices where id=1;")
                host = cur.fetchone()
                output = "{}_-_{}".format(output[0], host[0])
                cur.execute("select max (updated_at) from channels")
                last_date = cur.fetchone()
                last_date = str(last_date[0]).split(' ')[0]

            dizzDBs[db] = output
            temp = pd.Series({'Hash': db, 'DB': output, 'Date': last_date})
            df = pd.concat([temp.to_frame().T, df], ignore_index=True)

            cur.close()
            conn.close()
        except:
            pass
    return df
