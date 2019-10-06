# -*- coding: utf-8 -*-
import psycopg2
import pandas.io.sql as psql
import pandas as pd
from configparser import ConfigParser

# ini configuration file to connect to postgrtess
INI_FILE = "data/current.ini" #'data/db_local_developing.ini'
#import_path = "/home/enzo/neo4j/import"
#import_path = "./csv_files"
#import_path = "/home/enzo/neo4j/import"
import_path = "/import"
def config(filename=INI_FILE, section='postgresql'):
    #print(filename)
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    #print(parser)
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


def profiles(section='postgresql', filecsv="profiles.csv"):
    params = config(section=section)
    dataframe = pd.DataFrame()
    query = '''
        select id,name,display_name from profiles;
        '''
    #print(query)
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)

        print(dataframe.shape)
        conn.close()
    except:
        pass
    #print(dataframe.head())
    dataframe.to_csv("{}/{}".format(import_path, filecsv))
    return print(filecsv)


# def profiles(section='postgresql', filecsv="profiles.csv"):
#     params = config(section=section)
#     dataframe = pd.DataFrame()
#     query = '''
#         select id,name,display_name from profiles;
#         '''
#     try:
#         conn = psycopg2.connect(**params)
#         dataframe = psql.read_sql(query, conn)
#
#         print(dataframe.shape)
#         conn.close()
#     except:
#         pass
#     dataframe.to_csv("{}/{}".format(import_path, filecsv))
#     return print(filecsv)


def devices(section='postgresql', filecsv="devices.csv"):
    params = config(section=section)
    dataframe = pd.DataFrame()
    query = '''
        select id, name, hostname, display_name, devicetemplate_id, control_account_id from  devices;
        '''
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)

        print(dataframe.shape)
        conn.close()
    except:
        pass
    dataframe.to_csv("{}/{}".format(import_path, filecsv))
    return print(filecsv)


def Profile_devices(section='postgresql', filecsv="prof_devices.csv"):
    params = config(section=section)
    dataframe = pd.DataFrame()
    query = '''
select prof.id, prof.name as profile_name, prof.display_name as prof_display, accesstoken.id,
accesstoken.device_id,accesstoken.profile_id,accesstoken.device_account_id, dev.id,
dev.name as device_name,dev.hostname,dev.display_name as dev_dispaly
from profiles as prof, profiles_device_accesstokens as accesstoken, devices as dev
where prof.id = accesstoken.profile_id and dev.id=accesstoken.id
        '''
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)

        print(dataframe.shape)
        conn.close()
    except:
        pass
    dataframe.to_csv("{}/{}".format(import_path, filecsv))
    return print(filecsv)


def user_group(section='postgresql', filecsv="user_group.csv"):
    params = config(section=section)
    dataframe = pd.DataFrame()
    query = '''
select gr.name as group_name,us.name as userName, us.display_name as userDispalyName from user_groups as gr,
user_groups_users,users as us 
where user_groups_users.user_group_id = gr.id and 
us.id = user_groups_users.user_id;
        '''
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)

        print(dataframe.shape)
        conn.close()
    except:
        pass
    dataframe.to_csv("{}/{}".format(import_path, filecsv))
    return print(filecsv)


def profile_group(section='postgresql', filecsv="prof_group.csv"):
    params = config(section=section)
    dataframe = pd.DataFrame()
    query = '''
select gr.name as group_name,prof.id, prof.name as profile_name, 
prof.display_name as prof_display from user_groups as gr,profiles_user_groups, profiles as prof
where gr.id=profiles_user_groups.user_group_id and
profiles_user_groups.profile_id = prof.id;

        '''
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)

        print(dataframe.shape)
        conn.close()
    except:
        pass
    dataframe.to_csv("{}/{}".format(import_path, filecsv))
    return print(filecsv)


def profile_users(section='postgresql', filecsv="prof_users.csv"):
    params = config(section=section)
    dataframe = pd.DataFrame()
    query = '''
select users.name as userName,users.display_name as userDispalyName,
 prof.name as profile_name, prof.display_name as prof_display 
from users,
profiles_users,
profiles as prof
where users.id=profiles_users.user_id and
profiles_users.profile_id = prof.id;
        '''
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)

        print(dataframe.shape)
        conn.close()
    except:
        pass
    dataframe.to_csv("{}/{}".format(import_path, filecsv))
    return print(filecsv)


def device_Metadata(section='postgresql', filecsv="device_metadata.csv"):
    params = config(section=section)
    dataframe = pd.DataFrame()
    query = '''
select  value as ValueMetadata,cols.display_name as NameMetadata,  name, hostname, dev.display_name 
from metavals as val, metacols as cols,devices as dev
where val.metacol_id=cols.id and val.linked_id=dev.id and linked_type='Device';
        '''
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)

        print(dataframe.shape)
        conn.close()
    except:
        pass
    dataframe.to_csv("{}/{}".format(import_path, filecsv))
    return print(filecsv)


def profile_tasks(section='postgresql', filecsv="profile_tasks.csv"):
    params = config(section=section)
    dataframe = pd.DataFrame()
    query = '''
select tasks.name as task_name, tasks.display_name as task_display_name, profiles.name as profile_name,
 profiles.display_name as profile_display_name from tasks, profiles_tasks, profiles
where profiles_tasks.profile_id = profiles.id
and profiles_tasks.task_id = tasks.id;
        '''
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)

        print(dataframe.shape)
        conn.close()
    except:
        pass
    dataframe.to_csv("{}/{}".format(import_path, filecsv))
    return print(filecsv)


def profile_tools(section='postgresql', filecsv="profile_tools.csv"):
    params = config(section=section)
    dataframe = pd.DataFrame()
    query = '''
select tools.name as tool_name, tools.display_name as tool_display_name, profiles.name as profile_name,
 profiles.display_name as profile_display_name from tools, profiles_tools, profiles
where profiles_tools.profile_id = profiles.id
and profiles_tools.tool_id = tools.id;
        '''
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)

        print(dataframe.shape)
        conn.close()
    except:
        pass
    dataframe.to_csv("{}/{}".format(import_path, filecsv))
    return print(filecsv)


def templates_device(section='postgresql', filecsv="templates_device.csv"):
    params = config(section=section)
    dataframe = pd.DataFrame()
    query = '''
select vendor.name as vendor_name, vendor.display_name as vendor_dispaly_Name, typ.name as type_Device,
typ.display_name as type_Dispaly_name,
  dev.name as name_device, dev.hostname as dev_hostname, dev.display_name as dev_display_name,
   teml.devicevendor_id, teml.name as teml_name, teml.display_name as teml_display_name 
from devices as dev, devicetemplates as teml, devicetypes as typ, devicevendors as vendor
where dev.devicetemplate_id=teml.id and
typ.id =teml.devicetype_id and
vendor.id= teml.devicevendor_id;        
'''
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)

        print(dataframe.shape)
        conn.close()
    except:
        pass
    dataframe.to_csv("{}/{}".format(import_path, filecsv))
    return print(filecsv)


def templates_tools(section='postgresql', filecsv="templates_tools.csv"):
    params = config(section=section)
    dataframe = pd.DataFrame()
    query = '''
select tools.name as tool_name, tools.display_name as tool_display_name, devicetemplates.name as devicetemplates_name,
 devicetemplates.display_name as devicetemplates_display_name
from tools, devicetemplates, devicetemplates_tools
where devicetemplates_tools.devicetemplate_id =devicetemplates.id
and devicetemplates_tools.tool_id = tools.id;       
'''
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)

        print(dataframe.shape)
        conn.close()
    except:
        pass
    dataframe.to_csv("{}/{}".format(import_path, filecsv))
    return print(filecsv)


def templates_tasks(section='postgresql', filecsv="templates_tasks.csv"):
    params = config(section=section)
    dataframe = pd.DataFrame()
    query = '''
select tasks.name as task_name, tasks.display_name as task_display_name, devicetemplates.name as devicetemplates_name,
devicetemplates.display_name as devicetemplates_display_name
from tasks, devicetemplates, devicetemplates_tasks
where devicetemplates_tasks.devicetemplate_id =devicetemplates.id
and devicetemplates_tasks.task_id = tasks.id; 
'''
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)

        print(dataframe.shape)
        conn.close()
    except:
        pass
    dataframe.to_csv("{}/{}".format(import_path, filecsv))
    return print(filecsv)
