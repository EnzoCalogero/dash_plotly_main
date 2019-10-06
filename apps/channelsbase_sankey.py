# -*- coding: utf-8 -*-
import base64
import flask
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import os
from datetime import timedelta
from datetime import datetime as dt
import datetime

from app import app
from apps import db_onnections, general_configurations

#####################################
#### DBs information collections   ##
#####################################
list_db = db_onnections.list_dbs()

# Enable the DB selector
if len(list_db) == 1:
    enable_db_selector = True
else:
    enable_db_selector = False

#####################################
####  First Data Collection        ##
#####################################
FROM = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=45)).strftime("%Y-%m-%d")

df = db_onnections.ChannelDB(from_data=FROM, section=general_configurations.Current_active_DB)

df['created_at'] = pd.to_datetime(df['created_at'])

dataMax = df['created_at'].max()
dataMin = dataMax - timedelta(days=30)

available_Users = sorted(df['display_name'].unique())

# Dash Variables

colors = {
    'background': '#111111',
    'text': '#253471'}

image_filename = os.getcwd() + '/pics//enzo_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
layout = html.Div([
    html.Div([
        dcc.Interval(id='interval_channels_sand', interval=general_configurations.refresh_interval),
        html.Div([
            html.A(
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                         style={
                             'height': '20px',
                             'float': 'left',
                             'position': 'relative',
                             'bottom': '-10px',
                             'width': '100px'}
                         ), href='/', target="_self"),
            html.H2(
                children='Channels Sankey',
                id='H2_chan_sand',
                style={
                    'textAlign': 'center',
                    'font-family': 'Glacial Indifference',
                    'color': colors['text']}
            ),
        ], className='ten columns'),
        html.Div([
            html.A('Set the Default DB', href='/setdb', target="_blank")
        ], className='two columns'),
    ], className="row"),
    #################################################################################################
    html.Div([
        html.Div([
            html.Div(children="Source Database"),
        ], className='two columns'),
        html.Div([
            dcc.Dropdown(
                id="DB-selection-channel_sand",
                clearable=False,
                options=[{'label': i, 'value': i} for i in list_db],
                disabled=enable_db_selector,
                value=general_configurations.Current_active_DB)
        ], className='three columns'),
        html.Div([
            dcc.Link('Percentages', href='/channel_percent'),
        ], className='two columns'),
        html.Div([
            dcc.Link('HeatMaps', href='/channel_heatmap'),
        ], className='two columns'),
    ], className="row"),
    #####################################################################################################
    html.Div([
        html.Div([
            html.Div(children="Date Range Filter"),
        ], className='two columns'),
        html.Div([
            dcc.DatePickerRange(
                id='date-picker-range-channels_sand',
                minimum_nights=1,
                start_date=dataMin,
                end_date=dataMax),
        ], className='five columns'),
    ], className="row"),
    ####################################################################################################################
    html.Div([
        html.Div([
            dcc.Graph(id='indicator-graphic9b_sand',
                      config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo':False},
                      style={'width': '100%', 'display': 'inline-block','color': colors['text']}),
        ], className="row"),
    ], style={'font-family': 'Glacial Indifference','padding': '0px 10px 15px 10px',
              'marginLeft': 'auto', 'marginRight': 'auto', "width": "157vh",
              'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)','color': colors['text']}
    ),
    #######################################################################################################################
    html.Div([
        html.H4(
            children='Users View',
            style={
                'textAlign': 'left',
                'font-family': 'Glacial Indifference',
                'color': colors['text']}
        ),
    ], className="row"),
    ########################################################################
    html.Div([
        html.Div(children="User"),
    ], className='one columns'),
    html.Div([
        dcc.Dropdown(
            id='Users-column_Channel_sand',
            clearable=False,
            options=[{'label': i, 'value': i} for i in available_Users],
            value=available_Users[0]),
    ], className='two columns'),
    ###############################################################################################################
    html.Div([
        html.Div([
            dcc.Graph(id='indicator-graphic10b_sand',
                      config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo': False},
                      style={'width': '100%', 'display': 'inline-block', 'color': colors['text']}),
        ], className="row"),
    ], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto', 'marginRight': 'auto', "width": "157vh",
              'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113, 0.4)', 'color': colors['text']}
    ),
    html.Div(id='intermediate-value_chan_sank', style={'display': 'none'}),
    html.Div(id='display-time_channels_sand'),
    html.Div(id='display-DB-channel_sand'),
], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "160vh",
          'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113, 0.4)'}
)
# Closure Layout


@app.callback(dash.dependencies.Output('date-picker-range-channels_sand', 'end_date'),
              [dash.dependencies.Input('DB-selection-channel_sand', 'value')])
def update_db_(db):
    from_day = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=120)).strftime("%Y-%m-%d")

    df = db_onnections.ChannelDB(from_data=from_day, section=db)

    df['created_at'] = pd.to_datetime(df['created_at'])

    datamax = df['created_at'].max()
    return datamax


@app.callback(dash.dependencies.Output('date-picker-range-channels_sand', 'start_date'),
              [dash.dependencies.Input('DB-selection-channel_sand', 'value')])
def update_db_(db):
    from_day = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=120)).strftime("%Y-%m-%d")

    df = db_onnections.ChannelDB(from_data=from_day, section=db)

    df['created_at'] = pd.to_datetime(df['created_at'])

    datamax = df['created_at'].max()
    datamin = datamax - timedelta(days=15)
    return datamin


# Cookies Related (First Half)
@app.callback(
    dash.dependencies.Output('intermediate-value_chan_sank', 'children'),
    [dash.dependencies.Input('H2_chan_sand', 'children')])
def update_db_chan_heat(_):
    try:
        cached_db = flask.request.cookies['DB']
    except:
        return list_db[0]
    else:
        return cached_db


# Cookies Related (Second Half)
@app.callback(
    dash.dependencies.Output('DB-selection-channel_sand', 'value'),
    [dash.dependencies.Input('intermediate-value_chan_sank', 'children')])
def update_db_chan_heat_(db):
    return db
##########################
# Time Related function  #
##########################


@app.callback(
    dash.dependencies.Output('display-time_channels_sand', 'children'),
    events=[dash.dependencies.Event('interval_channels_sand', 'interval')])
def display_time():

    return str(datetime.datetime.now())


# DB related Function
@app.callback(
    dash.dependencies.Output('display-DB-channel_sand', 'children'),
    [dash.dependencies.Input('DB-selection-channel_sand', 'value')])
def update_db(db):
    general_configurations.Current_active_DB = db
    return db

#################################
# Graphics Related Functions    #
#################################


@app.callback(
    dash.dependencies.Output('indicator-graphic9b_sand', 'figure'),
    [dash.dependencies.Input('interval_channels_sand', 'n_intervals'),
     dash.dependencies.Input('date-picker-range-channels_sand', 'start_date'),
     dash.dependencies.Input('date-picker-range-channels_sand', 'end_date'),
     dash.dependencies.Input('DB-selection-channel_sand', 'value')])
def update_graph9b(n, start_date, end_date, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    tempdf = db_onnections.ChannelDB(from_data=start_date, to_data=end_date, section=db)

    Users = tempdf[['display_name']].drop_duplicates()
    Users.columns = ['Nome_nodo']
    tempdf['protDev'] = "[" + tempdf.protocol + '] - ' + tempdf.hostname
    tempdf['protDev'] = tempdf['protDev'].replace(' ', '')

    Protocols = tempdf[['protDev']].drop_duplicates()
    Protocols.columns = ['Nome_nodo']
    nodes = pd.concat([Users, Protocols], axis=0)
    refrenza = [x for x in range(0, nodes.shape[0])]

    nodesDict = dict(zip(nodes.Nome_nodo, refrenza))

    links = tempdf[['display_name', 'protocol', 'protDev', 'hostname', 'device']]
    links = links.groupby(['display_name', 'protDev'], as_index=False).count()
    links['value'] = links['hostname']
    links['source'] = links['display_name'].map(nodesDict)
    links['target'] = links['protDev'].map(nodesDict)
    links = links[links['protDev'] != 'nan']
    links = links[links['display_name'] != 'nan']
    return {
        'data': [dict(
            type="sankey",
            domain=dict(
                x=[0, 1],
                y=[0, 1]),
            link={
                "source": links.source.dropna(axis=0, how='any'),
                "target": links.target.dropna(axis=0, how='any'),
                "value": links['value'].dropna(axis=0, how='any')
            },
            node=dict(label=nodes.Nome_nodo,
                      pad=6,
                      ),
        )],
        'layout': go.Layout(
            title="Sankey Diagram Users vs Protocols-Devices Globally",
            autosize=True,
            font={'family': 'Glacial Indifference', 'color': colors['text']}
        )
    }


@app.callback(
    dash.dependencies.Output('indicator-graphic10b_sand', 'figure'),
    [dash.dependencies.Input('Users-column_Channel_sand', 'value'),
     dash.dependencies.Input('date-picker-range-channels_sand', 'start_date'),
     dash.dependencies.Input('date-picker-range-channels_sand', 'end_date'),
     dash.dependencies.Input('interval_channels_sand', 'n_intervals'),
     dash.dependencies.Input('DB-selection-channel_sand', 'value')])
def update_graph10b(user, start_date, end_date, n, db):

    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    TempDf = db_onnections.ChannelDB(from_data=start_date, to_data=end_date, section=db)
    TempDf = TempDf[TempDf['display_name'] == user]
    TempDf['protDev'] = '[' + TempDf.protocol + '] - ' + TempDf.hostname
    TempDf['protDev'] = TempDf['protDev'].replace(' ', '')

    Users = TempDf[['display_name']].drop_duplicates()
    Users.columns = ['Nome_nodo']
    Protocols = TempDf[['protDev']].drop_duplicates()
    Protocols.columns = ['Nome_nodo']
    nodes = pd.concat([Users, Protocols], axis=0)
    refrenza = [x for x in range(0, nodes.shape[0])]

    nodesDict = dict(zip(nodes.Nome_nodo, refrenza))
    links = TempDf[['display_name', 'protocol', 'protDev', 'hostname', 'device']]
    links = links.groupby(['display_name', 'protDev'], as_index=False).count()
    links['value'] = links['hostname']
    links['source'] = links['display_name'].map(nodesDict)
    links['target'] = links['protDev'].map(nodesDict)
    links = links[links['protDev'] != 'nan']
    links = links[links['display_name'] != 'nan']

    return {
        'data': [dict(
            type="sankey",
            domain=dict(
                x=[0, 1],
                y=[0, 1]),
            link={
                "source": links.source.dropna(axis=0, how='any'),
                "target": links.target.dropna(axis=0, how='any'),
                "value": links['value'].dropna(axis=0, how='any')
            },
            node=dict(label=nodes.Nome_nodo),
        )],
        'layout': go.Layout(
            title="Sankey {} vs protocols-Devices".format(user),
            autosize=True,
            font={'family': 'Glacial Indifference', 'color': colors['text']}
        )
    }


@app.callback(
    dash.dependencies.Output('Users-column_Channel_sand', 'options'),
    [dash.dependencies.Input('date-picker-range-channels_sand', 'start_date'),
     dash.dependencies.Input('date-picker-range-channels_sand', 'end_date'),
     dash.dependencies.Input('DB-selection-channel_sand', 'value')])
def update_index1(start_date, end_date, db):

    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    df = db_onnections.ChannelDB(from_data=start_date, to_data=end_date, section=db)
    available_users = sorted(df['display_name'].unique())

    return [{'label': i, 'value': i} for i in available_users]


@app.callback(
    dash.dependencies.Output('Users-column_Channel_sand', 'value'),
    [dash.dependencies.Input('date-picker-range-channels_sand', 'start_date'),
     dash.dependencies.Input('date-picker-range-channels_sand', 'end_date'),
     dash.dependencies.Input('DB-selection-channel_sand', 'value')])
def update_index2(start_date, end_date, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    tempdf = db_onnections.ChannelDB(from_data=start_date, to_data=end_date, section=db)

    available_users = sorted(tempdf['display_name'].unique())

    return available_users[0]
