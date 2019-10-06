# -*- coding: utf-8 -*-
import psycopg2
import pandas.io.sql as psql
import pandas as pd
from configparser import ConfigParser
from apps import general_configurations

# ini configuration file to connect to postgrtess
INI_FILE = 'data/current.ini'


def config(filename=INI_FILE, section=general_configurations.Current_active_DB):
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
            if param[0] == 'database':
                db[param[0]] = param[1].replace('-', '')
            else:
                db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db


def sessionDB(from_data='2018-01-01', section=general_configurations.Current_active_DB):
    '''
    Return session query results in a single dataframe.

    '''
    conn = None
    params = config(section=section)
    dataframe = pd.DataFrame()
    query = '''
        select us.display_name,extract(hour from ses.deleted_at) as HourOut, 
        extract(hour from ses.created_at) as HourIn, extract(dow from ses.deleted_at) as WDay,
        peer_address,substring(peer_address from '^[0-9]*.[0-9]*.[0-9]*' ) as subnet,channel_count, 
        ses.created_at  from sessions ses,users us 
        where ses.user_id=us.id
        and ses.deleted_at > '{} 00:00:00.000000';
    '''.format(from_data)
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)

        # print(dataframe.shape)
        conn.close()
    except:
        pass
    return dataframe


def ChannelDB(from_data='2018-01-01', to_data=None, section=general_configurations.Current_active_DB):
    '''
    Return all the customer data in a single dataframe.
    With the result of the Channel Query.
   '''
    conn = None
    params = config(section=section)
    dataframe = pd.DataFrame()
    if to_data is None:
        ending = ""
    else:
        ending = "and ses.deleted_at <  '{} 00:00:00.000000'".format(to_data)

    query = '''
        select ch.device_id as device,templ.devicetype_id,us.display_name,us.failed_logins,dev.hostname,
        extract(hour from ses.deleted_at) as HourOut, extract(hour from ses.created_at) as HourIn,access_role_id,
        account, protocol, (ses.deleted_at - ses.created_at) as durSession,
        extract(dow from ses.deleted_at) as WDay,(ch.deleted_at - ch.created_at) as durChanel,device_account_id,
        peer_address,substring(peer_address from '^[0-9].[0-9].[0-9]*' ) as subnet,
        channel_count, ses.created_at from channels ch, sessions ses,users us,devices dev, 
        devicetemplates templ 
        where ses.id= ch.session_id and ses.user_id=us.id and
        ch.device_id=dev.id and
        dev.devicetemplate_id=templ.id and 
        ses.deleted_at >  '{} 00:00:00.000000' {};
    '''.format(from_data, ending)
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)

        # print(dataframe.shape)
        conn.close()
    except:
        pass
    dataframe['devicetype_id'] = dataframe['devicetype_id'].astype('category', ordered=True)
    typelist = [1, 16, 17, 20, 21]
    elelmenti = "firewall,linuxserver,windows,other,hypervisor".split(',')
    translation = dict(zip(typelist, elelmenti))
    dataframe['devicetype_id'] = dataframe['devicetype_id'].map(translation)
    return dataframe


def templateDB(from_data='2018-01-01', to_data=None, section=general_configurations.Current_active_DB):
    '''
    Return all the customer data in a single dataframe.
    With the result of the Temp[late Query.
    '''
    conn = None

    params = config(section=section)

    if to_data is None:
        ending = ""
    else:
        ending = "and ch.deleted_at <  '{} 00:00:00.000000'".format(to_data)

    dataframe = pd.DataFrame()
    query = '''
        select ch.protocol, ch.deleted_at, ch.created_at, dev.display_name as nameDevice, templ.name as templateName,
        templ.display_name  as dispalynameTemp,types.name as typeslName, 
        types.display_name as typesDisplayName,vendor.name as vendor
        from channels ch,devices dev,devicetemplates templ, devicetypes types,devicevendors vendor 
        where ch.device_id=dev.id and dev.devicetemplate_id=templ.id
        and vendor.id= templ.devicevendor_id 
        and types.id = templ.devicetype_id
        and  ch.deleted_at > '{} 00:00:00.000000' {};
    '''.format(from_data, ending)
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)
        # print(dataframe.shape)
        conn.close()
    except:
        pass
    return dataframe


def tasksDB(from_data='2018-01-01', to_data=None, section=general_configurations.Current_active_DB):
    '''
    Return all the customer data in a single dataframe.
    With the result of the Tasks Query.
    '''
    conn = None

    params = config(section=section)
    if to_data is None:
        ending = ""
    else:
        ending = "and event_time <=  '{} 00:00:00.000000'".format(to_data)

    Data = pd.DataFrame()
    query = '''
        select users.display_name,device_name,task_name,last_event,event_time from taskrecords as tasks,users
        where users.id=tasks.user_id and
        event_time >=  '{} 00:00:00.000000' {};
        
    '''.format(from_data, ending)
    try:
        conn = psycopg2.connect(**params)
        Data = psql.read_sql(query, conn)
        # print(Data.shape)
        conn.close()
    except:
        return Data
    Data = Data[Data['last_event'] == 'SUCCESS']
    Data['event_time'] = pd.to_datetime(Data['event_time'])
    Data['event_time'] = Data['event_time'].dt.date
    Data = Data[Data['display_name'] != 'Osirium Server']
    Data['args.task_name'] = Data['task_name']
    Data['name'] = Data['task_name']
    Data['args.actioned_by_username'] = Data['display_name']
    Data['args.device_display_name'] = Data['device_name']

    Data = Data[['name', 'args.task_name', 'args.actioned_by_username', 'args.device_display_name', 'event_time']]

    Data['event_time'] = pd.to_datetime(Data['event_time'])

    return Data


def runquery(query, section=general_configurations.Current_active_DB):
    '''
    Return the result of the query in a single dataframe.

    '''
    conn = None
    params = config(section=general_configurations.Current_active_DB)
    dataframe = pd.DataFrame()

    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)

        # print(dataframe.shape)
        conn.close()
    except:
        pass
    return dataframe


def anomalityDB(section=general_configurations.Current_active_DB):

    '''
    Return all the customer data in a single dataframe.
    With the result of the Channel Query.
   '''
    from_data = '2018-01-01'
    border_data = "2018-06-18"
    end_date = "2018-06-25"

    conn = None
    params = config(section=section)
    dataframe = pd.DataFrame()
    query = '''
        select ses.deleted_at as timestamp, ch.device_id as device,templ.devicetype_id,us.display_name,
        us.failed_logins,dev.hostname, extract(hour from ses.deleted_at) as HourOut,
        extract(hour from ses.created_at) as HourIn,access_role_id, account, protocol,
        (ses.deleted_at - ses.created_at) as durSession, extract(dow from ses.deleted_at) as WDay,
        (ch.deleted_at - ch.created_at) as durChanel,device_account_id,
        peer_address,substring(ses.peer_address from '^[0-9]*.[0-9]*.[0-9]*' ) as subnet,
        channel_count from channels ch, sessions ses,users us,devices dev,
        devicetemplates templ 
        where ses.id= ch.session_id and ses.user_id=us.id and
        ch.device_id=dev.id and
        dev.devicetemplate_id=templ.id and 
        ses.deleted_at >  '{} 00:00:00.000000';
    '''.format(from_data)

    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)

        # print(dataframe.shape)
        conn.close()
    except:
        pass

    df = dataframe[["timestamp", "display_name", "hostname", "protocol", "subnet"]].copy()
    df['Hostname_'] = df['hostname']
    df['Protocol_'] = df['protocol']
    df['Subnet_'] = df['subnet']
    df = pd.get_dummies(df, columns=["protocol"])
    df = pd.get_dummies(df, columns=["subnet"])
    df = pd.get_dummies(df, columns=["hostname"])

    history = df[df['timestamp'] <= border_data].copy()
    history = history.drop(['Hostname_', 'Protocol_', 'Subnet_'], axis=1)
    predict = df[df['timestamp'] > border_data].copy()
    predict = predict[predict['timestamp'] <= end_date]
    return history, predict

############################################################################
### Multi DBs sections                                                   ###
############################################################################


# Returning the number of DBs
def number_dbs(filename=INI_FILE, section='DBs'):
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            if param[0] == 'number':
                return param[1]
            else:
                return 1  # no DBS sections
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))


# Returning the list of DBs
def list_dbs(filename=INI_FILE):
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    dbs = []
    for db in parser.sections():
        if (db != "DBs") and (db != "ElasticSearch") and (db != "neo4j"):
            dbs.append(db)
    return dbs


###################################
## Generic Connections vs Tasks  ##
###################################
def ChannelTasks(from_data='2018-01-01', to_data=None, section=general_configurations.Current_active_DB):
    '''
    Return all the customer data in a single dataframe.
    With the result of the Channel Query.
   '''
    conn = None
    params = config(section=section)
    dataframe = pd.DataFrame()
    if to_data is None:
        ending = ""
    else:
        ending = "and ses.deleted_at <  '{} 00:00:00.000000'".format(to_data)

    query = '''
        select templ.name as template,ses.created_at,ses.id as session_id,us.id as user_id,us.display_name as user_name,
        ch.device_id as device_id, dev.name as device_name,ch.id as Connection_id,protocol as Name
        from channels ch, sessions ses,users us,devices dev, devicetemplates templ 
        where ses.id= ch.session_id and ses.user_id=us.id and
        ch.device_id=dev.id and
        dev.devicetemplate_id=templ.id and
        ses.deleted_at >  '{} 00:00:00.000000' {};
    '''.format(from_data, ending)
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)

        # print(dataframe.shape)
        conn.close()
    except:
        pass
    dataframe["Connection"] = "BasicTemplate"
    return dataframe


def SessionvsTasks(from_data='2018-01-01', to_data=None, section=general_configurations.Current_active_DB):
    '''
    Return all the customer data in a single dataframe.
    With the result of the Tasks Query.
   '''
    conn = None
    params = config(section=section)
    dataframe = pd.DataFrame()
    if to_data is None:
        ending = ""
    else:
        ending = "and sessions.deleted_at <  '{} 00:00:00.000000'".format(to_data)

    query = '''
        SELECT sessions.created_at,sessions.id AS session_id, taskrecords.user_id, taskrecords.user_name,
        taskrecords.device_id, taskrecords.device_name, taskrecords.task_id as Connection_id,
        taskrecords.task_name as Name FROM taskrecords, sessions 
        where sessions.user_id = taskrecords.user_id AND 
        taskrecords.created_at > sessions.created_at AND 
        taskrecords.created_at < sessions.deleted_at and
        sessions.deleted_at >  '{} 00:00:00.000000' {};
    '''.format(from_data, ending)
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)

        # print(dataframe.shape)
        conn.close()
    except:
        pass
    dataframe["Connection"] = "Task"
    dataframe["template"]="---"
    return dataframe


def taskvsChannel(from_data='2018-01-01', to_data=None, section="first_edition"):
    chatk = ChannelTasks(from_data=from_data, to_data=to_data, section=section)
    sestk = SessionvsTasks(from_data=from_data, to_data=to_data, section=section)
    frames = [sestk, chatk]
    result = pd.concat(frames)
    return result
