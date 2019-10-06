import pandas as pd
import os
from DBQueries import *
from Dataframes import *
from anonymize import *



def customer_tasks(path,pathan):
    # Crete the Dataframes for the Tasks analytics
    tasks = tasksDB()
    os.rename('{}/data/tasks_.csv'.format(path), '{}/data/tasks_old.csv'.format(path))
    df_old = pd.read_csv('{}/data/tasks_old.csv'.format(path))
    list = set(tasks['db'])
    for hash in set(df_old['db']):
        if hash not in list:
            print("Found One to Update...")
            print(hash)
            temp = df_old[df_old['db'] == hash]
            tasks = tasks.append(temp)
    tasks.to_csv('{}/data/tasks_.csv'.format(path))
    tasks = CreateDataframetasks(path=path)
    tasks.to_csv('{}/data/tasks.csv'.format(path))
    tasks = anonymyCompany(path=path,file='{}/data/tasks.csv'.format(path))
    tasks.to_csv('{}/data/tasks_a.csv'.format(pathan))
    tasks = anonymyUser(path=path,file='{}/data/tasks_a.csv'.format(pathan), colNames='args.actioned_by_username', filter=True)
    tasks.to_csv('{}/data/tasks_a.csv'.format(pathan))
    return 0


def customer_activity(path,pathan):
    #Created the Expanded Dataframes for the Sessions
    print("Starting the Big One")
    cache = CreateDataframeCache(path)
    os.rename('{}/data/extendedsession.csv'.format(path), '{}/data/extendedsession_old.csv'.format(path))
    df_old = pd.read_csv('{}/data/extendedsession_old.csv'.format(path))
    list = set(cache['db'])
    for hash in set(df_old['db']):
        if hash not in list:
            print("Found One to Update...")
            print(hash)
            temp = df_old[df_old['Hash'] == hash]
            cache = cache.append(temp)
    cache.to_csv('{}/data/extendedsession.csv'.format(path))
    cache=anonymyCompany(path=path,file='{}/data/extendedsession.csv'.format(path))
    cache.to_csv('{}/data/extendedsession_a.csv'.format(pathan))
    cache=anonymyUser(path=path,file='{}/data/extendedsession_a.csv'.format(pathan), colNames='display_name', filter=True)
    cache.to_csv("{}/data/extendedsession_a.csv".format(pathan))


def customer_channel(path,pathan):
    # Crete the Dataframes for the Channel analytics
    channel = ChannelDB()
    os.rename('{}/data/Channels_.csv'.format(path), '{}/data/Channels_old.csv'.format(path))
    df_old = pd.read_csv('{}/data/Channels_old.csv'.format(path))
    list = set(channel['db'])
    for hash in set(df_old['db']):
        if hash not in list:
            print("Found One to Update...")
            print(hash)
            temp = df_old[df_old['db'] == hash]
            channel = channel.append(temp)
    channel.to_csv('{}/data/Channels_.csv'.format(path))
    channel = CreateDataframeChannel(path)
    channel.to_csv('{}/data/Channels.csv'.format(path))
    channel = anonymyCompany(path=path,file='{}/data/Channels.csv'.format(path))
    channel.to_csv('{}/data/Channels_a.csv'.format(pathan))
    channel = anonymyUser(path=path,file='{}/data/Channels_a.csv'.format(pathan), colNames='display_name', filter=True)
    channel.to_csv('{}/data/Channels_a.csv'.format(pathan))
    return 0


def customer_template(path,pathan):
    # Crete the Dataframes for the Templates analytics
    templ=templateDB()
    os.rename('{}/data/templetes_.csv'.format(path), '{}/data/templetes_old.csv'.format(path))
    df_old = pd.read_csv('{}/data/templetes_old.csv'.format(path))
    list = set(templ['db'])
    for hash in set(df_old['db']):
        if (hash not in list):
            print("Found One to Update...")
            print(hash)
            temp = df_old[df_old['db'] == hash]
            templ = templ.append(temp)
    templ.to_csv('{}/data/templetes_.csv'.format(path))
    templ=CreateDataframetemplate(path=path)
    templ.to_csv('{}/data/templetes.csv'.format(path))
    templ=anonymyCompany(path=path,file='{}/data/templetes.csv'.format(path))
    templ.to_csv('{}/data/templetes_a.csv'.format(pathan))
    return 0


def customer_loading(path):
    # Crete the list of the customers available
    df= dictDB()
    os.rename('{}/data/dblist.csv'.format(path),'{}/data/dblist_old.csv'.format(path))
    df_old=pd.read_csv('{}/data/dblist_old.csv'.format(path))
    list=set(df['Hash'])
    for hash in set(df_old['Hash']):
        if hash not in list:
            print("Found One to Update...")
            print(hash)
            temp=df_old[df_old['Hash']==hash]
            df = df.append(temp)
    df.to_csv('{}/data/dblist.csv'.format(path))
    #Crete the dictionary for anomize
    companymix=companymixer(path=path)
    companymix.to_csv('{}/data/companymixer.csv'.format(path))
    return 0


def customer_graph(path,pathan):
    # Crete the Dataframes for the Session Graph charts
    graph = Graph_ChartsDB()
    os.rename('{}/data/Graph_.csv'.format(path), '{}/data/Graph_old.csv'.format(path))
    df_old = pd.read_csv('{}/data/Graph_old.csv'.format(path))
    list = set(graph['db'])
    for hash in set(df_old['db']):
        if hash not in list:
            print("Found One to Update...")
            print(hash)
            temp = df_old[df_old['db'] == hash]
            graph = graph.append(temp)
    graph.to_csv('{}/data/Graph_.csv'.format(path))
    graph = CreateDataframeGraphCharts(path)
    graph.to_csv('{}/data/Graph.csv'.format(path))
    graph = anonymyUser(path=path,file='{}/data/Graph.csv'.format(path), colNames='display_name', filter=True)
    graph.to_csv('{}/data/Graph_a.csv'.format(pathan))
    graph = anonymyCompany(path=path,file='{}/data/Graph_a.csv'.format(pathan))
    graph.to_csv('{}/data/Graph_a.csv'.format(pathan))
    return 0


def customer_sessions(path,pathan):
  #Crete the Dataframes for the Session analytics
    sessioni=sessionDB()
    os.rename('{}/data/session_.csv'.format(path), '{}/data/session_old.csv'.format(path))
    df_old = pd.read_csv('{}/data/session_old.csv'.format(path))
    list = set(sessioni['db'])
    for hash in set(df_old['db']):
        if hash not in list:
            print("Found One to Update...")
            print(hash)
            temp = df_old[df_old['db'] == hash]
            sessioni= sessioni.append(temp)
    sessioni.to_csv('{}/data/session_.csv'.format(path))
    sessioni=CreateDataframesession(path=path)
    sessioni.to_csv('{}/data/session.csv'.format(path))
    sessioni=anonymyCompany(path=path,file='{}/data/session.csv'.format(path))
    sessioni.to_csv('{}/data/session_a.csv'.format(pathan))
    sessioni=anonymyUser(path=path,file='{}/data/session_a.csv'.format(pathan),colNames='display_name',filter=True)
    sessioni.to_csv('{}/data/session_a.csv'.format(pathan))
    return 0
