#!/usr/bin/python
import psycopg2
import pandas.io.sql as psql
import pandas as pd
from configparser import ConfigParser


def config(filename='technote.ini', section='postgresql'):
    '''
    Configuration Reader
    '''
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            if(param[0]=='database'):
                db[param[0]] = param[1].replace('-','')
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
        print(output)


        skipdb=['postgres','tech_view_viewer','demo']
        listDB=[]

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
     params= config()
     dizzDBs= dict()
     df= pd.DataFrame()
     for db in DB_:
         try:
            params['database'] = db
            conn = psycopg2.connect(**params)
            cur = conn.cursor()

            cur.execute("select licencee from licences where id = (select max (id) from licences);")
            output = cur.fetchone()
            if output[0] not in skipdb:
               print(output[0])
               cur.execute("select hostname from devices where id=1;")
               host = cur.fetchone()
               output = "{}_-_{}".format(output[0], host[0])
               cur.execute("select max (updated_at) from channels")
               last_date = cur.fetchone()
               last_date=str(last_date[0]).split(' ')[0]

            dizzDBs[db]= output
            temp= pd.Series({'Hash': db,'DB': output,'Date': last_date}) #'host':host[0],
            df = pd.concat([temp.to_frame().T, df], ignore_index= True)

            cur.close()
            conn.close()
         except:
            pass
     return df


##########################################################
##    Nuova query to be add                            ###
##  select max (updated_at) from channels;             ###
##########################################################

def dictDBUnique():
    '''
    Return only one DB for each customer
    and select the DB most recent
    (last update on the session table.)
    '''
    conn = None
    DB_ = listDB()
    params=config()
    dizzDBs = dict()  # Entry on the licence defines the customer name
    timeDB = dict()   # Last entry on the session table
    hostDB = dict()   # Entry on the device table for the host name (multi enzo server on the same customer
    for db in DB_:
        try:
           params['database'] = db
           conn = psycopg2.connect(**params)
           cur = conn.cursor()

           cur.execute("select licencee from licences where id = (select max (id) from licences);")
           cliente = cur.fetchone()

           cur.execute("select hostname from devices where id=1;")
           host = cur.fetchone()
           cliente="{}_-_{}".format(cliente[0],host[0])

           cur.execute("select max(id) from sessions;")
           ValoreMax = cur.fetchone()

           if(cliente in timeDB.keys()):

               valold=timeDB[cliente]

               if int(valold) < int(ValoreMax[0]):
                   dizzDBs[cliente] = db
                   timeDB[cliente] = ValoreMax[0]
           else:
               dizzDBs[cliente] = db
               timeDB[cliente]=ValoreMax[0]
               hostDB[cliente]=host[0]

           cur.close()
           conn.close()
        except:
           pass
    return dizzDBs


def sessionDB():
    '''
    Return all the customer data in a single dataframe.
    With th eresult of the Session Query.

    '''
    conn = None
    s = dictDBUnique()
    DB_= set(s.values())
    params=config()
    dfDict=pd.DataFrame()
    query='''
        select us.display_name,us.failed_logins,extract(hour from ses.deleted_at) as HourOut, extract(hour from ses.created_at) as HourIn, extract(dow from ses.deleted_at) as WDay,peer_address,substring(peer_address from '^[0-9]*.[0-9]*.[0-9]*' ) as subnet,channel_count, ses.created_at  from sessions ses,users us 
        where ses.user_id=us.id
        and ses.deleted_at > '2017-01-01 00:00:00.000000';
        '''
    for db in DB_:
        try:
            params['database'] = db
            conn = psycopg2.connect(**params)
            dataframe=psql.read_sql(query,conn)

            dataframe['db']=db
            dfDict= pd.concat([dfDict, dataframe])

            print(dataframe.shape)
            conn.close()
        except:
            pass
    return dfDict


def ChannelDB():
    '''
    Return all the customer data in a single dataframe.
    With the result of the Channel Query.
   '''
    conn = None
    s = dictDBUnique()
    DB_ = set(s.values())
    params=config()
    dfDict=pd.DataFrame()
    query='''
        select ch.device_id as device,templ.devicetype_id,us.display_name,us.failed_logins,dev.hostname,
        extract(hour from ses.deleted_at) as HourOut, extract(hour from ses.created_at) as HourIn,access_role_id, account, protocol,
        (ses.deleted_at - ses.created_at) as durSession, extract(dow from ses.deleted_at) as WDay,(ch.deleted_at - ch.created_at) as durChanel,device_account_id,
        peer_address,substring(peer_address from '^[0-9].[0-9].[0-9]*' ) as subnet,channel_count from channels ch, sessions ses,users us,devices dev,
        devicetemplates templ 
        where ses.id= ch.session_id and ses.user_id=us.id and
        ch.device_id=dev.id and
        dev.devicetemplate_id=templ.id and 
        ses.deleted_at > '2018-01-01 00:00:00.000000';
        '''
    for db in DB_:
        try:
            params['database'] = db
            conn = psycopg2.connect(**params)
            dataframe=psql.read_sql(query,conn)

            dataframe['db']=db
            dfDict= pd.concat([dfDict, dataframe])

            print(dataframe.shape)
            conn.close()
        except:
            pass
    return dfDict


def templateDB():
    '''
    Return all the customer data in a single dataframe.
    With the result of the Temp[late Query.
    '''
    conn = None

    s = dictDBUnique()
    DB_ = set(s.values())

    params=config()
    dfdict=pd.DataFrame()
    query='''
select ch.protocol, ch.deleted_at, ch.created_at, dev.display_name as nameDevice, templ.name as templateName,templ.display_name  as dispalynameTemp,types.name as typeslName, 
types.display_name as typesDisplayName,vendor.name as vendor
from channels ch,devices dev,devicetemplates templ, devicetypes types,devicevendors vendor 
where ch.device_id=dev.id and dev.devicetemplate_id=templ.id
and vendor.id= templ.devicevendor_id 
and types.id = templ.devicetype_id
and  ch.deleted_at > '2017-01-01 00:00:00.000000';
        '''
    for db in DB_:
        try:
            params['database'] = db
            conn = psycopg2.connect(**params)
            dataframe=psql.read_sql(query,conn)

            dataframe['db']=db
            dfdict= pd.concat([dfdict, dataframe])

            print(dataframe.shape)
            conn.close()
        except:
            pass
    return dfdict


def tasksDB():
    '''
    Return all the customer data in a single dataframe.
    With the result of the Tasks Query.
    '''
    conn = None

    s = dictDBUnique()
    DB_ = set(s.values())

    params=config()
    dfDict=pd.DataFrame()
    query='''
    select users.display_name,device_name,task_name,last_event,event_time from taskrecords as tasks,users where event_time > '2016-01-01 00:00:00.203006' and users.id=tasks.user_id;
        '''
    for db in DB_:
        try:
            params['database'] = db
            conn = psycopg2.connect(**params)
            dataframe=psql.read_sql(query,conn)

            dataframe['db']=db
            dfDict= pd.concat([dfDict, dataframe])

            print(dataframe.shape)
            conn.close()
        except:
            pass
    return dfDict


def Graph_ChartsDB():
    '''
    Return all the customer data in a single dataframe.
    With the result of the Graph Charts Query.
    '''
    conn = None

    s = dictDBUnique()
    DB_ = set(s.values())

    params=config()
    dfDict=pd.DataFrame()
    query='''
    select templ.devicetype_id,us.display_name,dev.hostname, account, protocol,(ses.deleted_at - ses.created_at) as durSession, (ch.deleted_at - ch.created_at) as durChanel,peer_address,substring(peer_address from '^[0-9]*.[0-9]*.[0-9]*' ) as subnet,channel_count,
    templ.name as templateName,templ.display_name  as dispalynameTemp,types.name as typeslName, 
    types.display_name as typesDisplayName,vendor.name as vendor
    from channels ch, sessions ses,users us,devices dev,devicetemplates templ,devicetypes types,devicevendors vendor 
    where ses.id= ch.session_id 
    and ses.user_id=us.id
    and ch.device_id=dev.id
    and dev.devicetemplate_id=templ.id
    and vendor.id= templ.devicevendor_id 
    and types.id = templ.devicetype_id
    and ses.deleted_at > '2018-01-01 00:00:00.000000';
    '''
    for db in DB_:
        try:
            params['database'] = db
            conn = psycopg2.connect(**params)
            dataframe=psql.read_sql(query,conn)

            dataframe['db']=db
            dfDict= pd.concat([dfDict, dataframe])

            print(dataframe.shape)
            conn.close()
        except:
            pass
    return dfDict
