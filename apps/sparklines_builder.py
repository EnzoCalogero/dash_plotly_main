# -*- coding: utf-8 -*-
import pandas as pd

from apps import general_configurations


def tasksparkline(from_data, db):
    from apps import db_onnections

    templ = db_onnections.tasksDB(from_data=from_data, section=db)
    templ['event_time'] = pd.to_datetime(templ['event_time'])
    alpha = templ.resample('W-Mon', on='event_time').count()
    alpha = alpha[['args.task_name']]
    alpha.columns = ["NumberEvents"]
    # Add value for missing weeks
    alpha = alpha.reset_index()
    max_ = alpha.NumberEvents.max()
    events = alpha.NumberEvents
    events = "{}".format(events.values).replace(" ", ",").replace('[', '').replace(']', '').replace('\n', '')
    return events, max_


def session_chanelsparkline(from_data, db):
    from apps import db_onnections

    Templ = db_onnections.sessionDB(from_data=from_data, section=db)
    if Templ.empty:
        return 0, 0, 0, 0

    Templ['created_at'] = pd.to_datetime(Templ['created_at'])
    Templ = Templ.set_index('created_at')
    alpha = pd.DataFrame()
    alpha['SessionNumber'] = Templ['subnet'].resample('W-Mon').count()
    alpha['ChannelNumber'] = Templ['channel_count'].resample('W-Mon').sum()

    session_max = alpha['SessionNumber'].max()
    channel_max = alpha['ChannelNumber'].max()
    alpha = alpha.reset_index()
    Session_events = "{}"\
        .format(alpha['SessionNumber'].values).replace(" ", ",").replace('[', '').replace(']', '').replace('\n', '')
    Channel_events = "{}"\
        .format(alpha['ChannelNumber'].values).replace(" ", ",").replace('[', '').replace(']', '').replace('\n', '')

    return Session_events, session_max, Channel_events, channel_max


def failpsw_sparkline():
    from apps import elasticsearch_connections
    failedpwd = elasticsearch_connections.search_UserFailedLoginOdc()
    if failedpwd.empty:
        return 0, 0

    failedpwd['@timestamp'] = pd.to_datetime(failedpwd['@timestamp'])
    alpha = failedpwd.resample('W-Mon', on='@timestamp').count()
    alpha = alpha[['user']]
    alpha.columns = ["NumberEvents"]
    # Add value for missing weeks
    alpha = alpha.reset_index()
    max = alpha.NumberEvents.max()
    events = alpha.NumberEvents
    events = "{}".format(events.values).replace(" ", ",").replace('[', '').replace(']', '').replace('\n', '')
    return events, max


def Reveal_psw_sparkline():
    from apps import elasticsearch_connections
    revealedpwd = elasticsearch_connections.search_revealpassword()
    if revealedpwd.empty:
        return 0, 0

    revealedpwd['@timestamp'] = pd.to_datetime(revealedpwd['@timestamp'])
    alpha = revealedpwd.resample('W-Mon', on='@timestamp').count()
    alpha = alpha[['user']]
    alpha.columns = ["NumberEvents"]
    # Add value for missing weeks
    alpha = alpha.reset_index()
    max_ = alpha.NumberEvents.max()
    events = alpha.NumberEvents
    events = "{}".format(events.values).replace(" ", ",").replace('[', '').replace(']', '').replace('\n', '')
    return events, max


def long_running_sparkline():
    from apps import elasticsearch_connections
    longrun = elasticsearch_connections.search_long_run()
    if longrun.empty:
        return 0, 0

    longrun['@timestamp'] = pd.to_datetime(longrun['@timestamp'])
    alpha = longrun.resample('W-Mon', on='@timestamp').count()
    alpha = alpha[['user']]
    alpha.columns = ["NumberEvents"]
    # Add value for missing weeks
    alpha = alpha.reset_index()
    max_ = alpha.NumberEvents.max()
    events = alpha.NumberEvents
    events = "{}".format(events.values).replace(" ", ",").replace('[', '').replace(']', '').replace('\n', '')
    return events, max_
