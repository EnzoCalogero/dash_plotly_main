# -*- coding: utf-8 -*-
import datetime
import pandas as pd
from datetime import timedelta
from apps import db_onnections
from apps import general_configurations

def themeriverbuildertasks(db):
    '''
    construct for the FLask streamline
    '''
    from_data = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=160)).strftime("%Y-%m-%d")
    data = db_onnections.tasksDB(from_data=from_data, section=db)

    data['event_time'] = pd.to_datetime(data['event_time'])

    from_data = (data['event_time'].max() - timedelta(days=21)).strftime("%Y-%m-%d")

    Templ = db_onnections.tasksDB(from_data=from_data, section=db)
    # if the entry is empty
    if Templ.empty:
        return None

    Templ['event_time'] = pd.to_datetime(Templ['event_time'])

    alpha = Templ.groupby('args.task_name').resample('D', on='event_time').count()
    alpha = alpha[['args.task_name']]
    alpha.columns = ["NumberEvents"]

    ######################################
    # To remember the echart lib expect  #
    # an entry for each day for each     #
    # label serie and day                #
    ######################################

    alpha = alpha.reset_index()
    alpha['event_time'] = alpha['event_time'].dt.strftime('%Y/%m/%d')
    alpha['event_time'] = alpha['event_time'].apply(str)
    alpha['NumberEvents'] = alpha['NumberEvents'].apply(str)

    alpha['output'] = '["' + alpha['event_time'] + '",' + alpha['NumberEvents'] + ',"' + alpha['args.task_name'] + '"]'

    events = '{}'.format(alpha.output.values)
    events = events.replace("\' \'", ",")
    events = events.replace("\'\n \'", ",")
    events = events.replace("\'", "")
    return events


def themeriverbuilderusers(from_data='2018-04-15'):
    df = db_onnections.sessionDB(from_data='2018-04-15', section=general_configurations.Current_active_DB)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df[['display_name', 'channel_count', 'created_at']]
    df = df[df['created_at'] > '2018-04-15']

    alpha = df.groupby('display_name').resample('D', on='created_at').sum()
    alpha.columns = ["NumberEvents"]

    ######################################
    # To remember the echart lib expect  #
    # an entry for each day for each     #
    # label serie and day                #
    ######################################

    alpha = alpha.reset_index()
    alpha['created_at'] = alpha['created_at'].dt.strftime('%Y/%m/%d')
    alpha['created_at'] = alpha['created_at'].apply(str)
    alpha['NumberEvents'] = alpha['NumberEvents'].apply(str)

    alpha['output'] = '["' + alpha['created_at'] + '",' + alpha['NumberEvents'] + ',"' + alpha['display_name'] + '"]'

    events = '{}'.format(alpha.output.values)
    events = events.replace("\' \'", ",")
    events = events.replace("\'\n \'", ",")
    events = events.replace("\'", "")
    return events
