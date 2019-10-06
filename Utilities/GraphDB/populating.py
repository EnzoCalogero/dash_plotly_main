# -*- coding: utf-8 -*-
from neo4j.v1 import GraphDatabase

import psycopg2
import pandas.io.sql as psql
import pandas as pd
from configparser import ConfigParser

# ini configuration file to connect to postgrtess
INI_FILE = 'data/current.ini'
#driver = GraphDatabase.driver('bolt://10.9.99.66:7687')
driver = GraphDatabase.driver('bolt://neo4j:7687')
#, auth=basic_auth(“neo4j”, “neo4j”))


def config(filename=INI_FILE, section='postgresql'):

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


    ###########################################
    ##  Created the metadata Dataframe       ##
    ###########################################
def metadata_device(section='postgresql'):
    conn = None
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
        #print("metadata_device")
        print(dataframe.shape)
        conn.close()
    except:
        pass
    #print(dataframe.head)

    #dataframe.to_csv("csv_files/temp.csv")
    return dataframe


def metadata_users(section='postgresql'):
    conn = None
    params = config(section=section)
    dataframe = pd.DataFrame()
    query = '''
select  value, cols.display_name as columMeta, name,us.display_name from metavals as val, metacols as cols,users us
where val.metacol_id=cols.id and
val.linked_id= us.id and
linked_type='User';

        '''
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)
        #print("metadata_users")
        print(dataframe.shape)
        conn.close()
    except:
        pass

    return dataframe


def metadata_profiles(section='postgresql'):
    conn = None
    params = config(section=section)
    dataframe = pd.DataFrame()
    query = '''
select  value as ValueMetadata, cols.display_name as NameMetadata,pro.name as profile_name,
pro.display_name as profile_display_name
from metavals as val, metacols as cols, profiles as pro
where val.linked_type = 'Profile' and
val.linked_id=pro.id and
val.metacol_id=cols.id;
        '''
    try:
        conn = psycopg2.connect(**params)
        dataframe = psql.read_sql(query, conn)
        #print("metadata_profiles")
        print(dataframe.shape)
        conn.close()
    except:
        pass

    return dataframe


def populating_metadata_devices():
    sess = driver.session()
    p = metadata_device()
    for (inx, raw) in p.iterrows():

        q = '''
        match (aa:Device) where aa.Name = "{}" and aa.HostName = "{}"
          set aa.{} = "{}"
          '''.format(raw["name"], raw["hostname"], raw["namemetadata"], raw["valuemetadata"])

        _ = sess.run(q)


def populating_metadata_users():
    sess = driver.session()
    p = metadata_users()

    for (inx, raw) in p.iterrows():

        q = '''
        match (aa:User) where aa.Display_Name = "{}" and aa.Name = "{}"
          set aa.{} = "{}"
          '''.format(raw["display_name"], raw["name"], raw["colummeta"], raw["value"])

        _ = sess.run(q)


def populating_metadata_profiles():
    sess = driver.session()
    p = metadata_profiles()

    for (inx, raw) in p.iterrows():

        q = '''
        match (aa:Profile) where aa.Display_Name = "{}" and aa.Name = "{}"
          set aa.{} = "{}"
          '''.format(raw["profile_display_name"], raw["profile_name"], raw["namemetadata"], raw["valuemetadata"])

        _ = sess.run(q)


def profile_tasks(section='postgresql'):
    conn = None
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
    return dataframe


def populating_profile_tasks():
    sess = driver.session()
    p = profile_tasks()

    for (inx, raw) in p.iterrows():

        q = '''
        match (aa:Profile) where aa.Display_Name = "{}" and aa.Name = "{}"
          set aa.{} = "{}"
          '''.format(raw["profile_display_name"], raw["profile_name"], raw["namemetadata"], raw["valuemetadata"])

        _ = sess.run(q)


def entity_builder():
    # Preparing for the User Metadata Mapping
    p = metadata_users()
    user_fields = set(p['colummeta'])
    user_properties = ""
    for prop in user_fields:
        user_properties = user_properties + prop + ","
    user_properties = user_properties[:-1]

    # Preparing for the device Metadata Mapping
    p = metadata_device()
    device_fields = set(p['namemetadata'])
    device_properties = ""
    for prop in device_fields:
        device_properties = device_properties + prop + ","
    device_properties = device_properties[:-1]

    # Preparing for the Profile Metadata Mapping
    p = metadata_profiles()
    profile_fields = set(p['namemetadata'])
    profiles_properties = ""
    for prop in profile_fields:
        profiles_properties = profiles_properties + prop + ","
    profiles_properties = profiles_properties[:-1]

    #print(user_fields)
    #print(device_fields)
    #print(profile_fields)
    sess = driver.session()
    q = 'CREATE (n:Metadata) set n.NAME="Metadata", n.User = "{}", n.Device = "{}", n.Profile="{}"'\
        .format(user_properties, device_properties, profiles_properties)
   # print(q)
    _ = sess.run(q)

    return



