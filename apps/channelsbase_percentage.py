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
FROM = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=120)).strftime("%Y-%m-%d")

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
    dcc.Interval(id='interval_channels_perc', interval=general_configurations.refresh_interval),
    html.Div([
        html.Div([
            html.A(
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={
                    'height': '20px',
                    'float': 'left',
                    'position': 'relative',
                    'bottom': '-10px',
                    'width': '100px',
                }), href='/', target="_self"),
            html.H2(
                children='Channels Percentage',
                id='H2_chan_perc',
                style={
                    'textAlign': 'center',
                    'font-family': 'Glacial Indifference',
                    'color': colors['text']
                }
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
                id="DB-selection-channel_perc",
                clearable=False,
                options=[{'label': i, 'value': i} for i in list_db],
                disabled=enable_db_selector,
                value=general_configurations.Current_active_DB)
        ], className='three columns'),
        html.Div([
            dcc.Link('HeatMaps', href='/channel_heatmap'),
        ], className='two columns'),
        html.Div([
            dcc.Link('Sankeys', href='/channel_sankey'),
        ], className='two columns'),
    ], className="row"),
    ##############################################################################################
    html.Div([
        html.Div([
            html.Div(children="Date Range Filter"),
        ], className='two columns'),
        html.Div([
            dcc.DatePickerRange(
                id='date-picker-range-channels_perc',
                minimum_nights=1,
                start_date=dataMin,
                end_date=dataMax),
        ], className='five columns'),
    ], className="row"),
    #######################################################################################################################
    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id='indicator-graphic1b_perc',
                          config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo':False},
                          style={'width': '100%','display': 'inline-block', 'color': colors['text']}),
            ], className='four columns'),
            html.Div([
                dcc.Graph(id='indicator-graphic7b_perc',
                          config={'modeBarButtonsToRemove': ['sendDataToCloud'],'displaylogo':False },
                          style={'width': '100%', 'display': 'inline-block', 'color': colors['text']}),
            ], className='four columns'),
            html.Div([
                dcc.Graph(id='indicator-graphic5b_perc',
                          config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo': False},
                          style={'width': '100%', 'display': 'inline-block', 'color': colors['text']}),
            ], className='four columns'),
        ], className="row"),
    ], style={'font-family': 'Glacial Indifference',
              'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto',
              'marginRight': 'auto',
              'width': "157vh",
              'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)',
              'color': colors['text']}
    ),
    #############################################################################################
    html.Div([
        html.H4(
            children='Users View',
            style={
                'textAlign': 'left',
                'font-family': 'Glacial Indifference',
                'color': colors['text']
            }),
    ], className="row"),
    #####################################################################################################
    html.Div([
        html.Div([
            html.Div([
                html.Div(children="User"),
            ], className='one columns'),
            html.Div([
                dcc.Dropdown(
                    id='Users-column_Channel_perc',
                    clearable=False,
                    options=[{'label': i, 'value': i} for i in available_Users],
                    value=available_Users[0]),
            ], className='two columns'),
        ], className="row"),
        #############################################################################################################
        html.Div([
            html.Div([
                dcc.Graph(id='indicator-graphic2b_perc',
                          config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo':False},
                          style={'width': '100%', 'display': 'inline-block', 'color': colors['text']}),
            ], className='four columns'),
            html.Div([
                dcc.Graph(id='indicator-graphic8b_perc',
                          config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo':False},
                          style={'width': '100%', 'display': 'inline-block', 'color': colors['text']}),
            ], className='four columns'),
            html.Div([
                dcc.Graph(id='indicator-graphic6b_perc',
                          config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo':False},
                          style={'width': '100%', 'display': 'inline-block', 'color': colors['text']}),
            ], className='four columns'),
        ], className="row"),
        #####################################################################################################
    ], style={'font-family': 'Glacial Indifference',
              'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto',
              'marginRight': 'auto',
              "width": "157vh",
              'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113, 0.4)',
              'color': colors['text']}
    ),
    # Cookies Related
    html.Div(id='intermediate-value_chan_perc', style={'display': 'none'}),
    html.Div(id='display-time_channels_perc'),
    html.Div(id='display-DB-channel_perc'),
], style={'font-family': 'Glacial Indifference',
          'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto',
          'marginRight': 'auto',
          "width": "160vh",
          'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113 ,0.4)'}
)
# Clousure Layout


@app.callback(dash.dependencies.Output('date-picker-range-channels_perc', 'end_date'),
              [dash.dependencies.Input('DB-selection-channel_perc', 'value')])
def update_db_(db):
    from_day = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=120)).strftime("%Y-%m-%d")

    df = db_onnections.ChannelDB(from_data=from_day, section=db)

    df['created_at'] = pd.to_datetime(df['created_at'])

    datamax = df['created_at'].max()
    return datamax


@app.callback(dash.dependencies.Output('date-picker-range-channels_perc', 'start_date'),
              [dash.dependencies.Input('DB-selection-channel_perc', 'value')])
def update_db_(db):
    from_day = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=120)).strftime("%Y-%m-%d")

    df = db_onnections.ChannelDB(from_data=from_day, section=db)

    df['created_at'] = pd.to_datetime(df['created_at'])

    datamax = df['created_at'].max()
    datamin = datamax - timedelta(days=30)
    return datamin


# Cookies Related (First Half)
@app.callback(
    dash.dependencies.Output('intermediate-value_chan_perc', 'children'),
    [dash.dependencies.Input('H2_chan_perc', 'children')])
def update_db_chan_heat(_):
    try:
        cached_db = flask.request.cookies['DB']
    except:
        return list_db[0]
    else:
        return cached_db


# Cookies Related (Second Half)
@app.callback(
    dash.dependencies.Output('DB-selection-channel_perc', 'value'),
    [dash.dependencies.Input('intermediate-value_chan_perc', 'children')])
def update_db_chan_heat_(db):
    return db


##########################
# Time Related function  #
##########################
@app.callback(
    dash.dependencies.Output('display-time_channels_perc', 'children'),
    events=[dash.dependencies.Event('interval_channels_perc', 'interval')])
def display_time():

    return str(datetime.datetime.now())


# DB related Function
@app.callback(
    dash.dependencies.Output('display-DB-channel_perc', 'children'),
    [dash.dependencies.Input('DB-selection-channel_perc', 'value')])
def update_db(db):
    general_configurations.Current_active_DB = db
    return db


#################################
# Graphics Related Functions    #
#################################
@app.callback(
    dash.dependencies.Output('indicator-graphic1b_perc', 'figure'),
    [dash.dependencies.Input('date-picker-range-channels_perc', 'start_date'),
     dash.dependencies.Input('date-picker-range-channels_perc', 'end_date'),
     dash.dependencies.Input('interval_channels_perc', 'n_intervals'),
     dash.dependencies.Input('DB-selection-channel_perc', 'value')])
def update_graph1b(start_date, end_date, n, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    df = db_onnections.ChannelDB(from_data=start_date, to_data=end_date, section=db)

    ProtoGlobal = df[['display_name', 'protocol']].copy()

    ProtoGlobal = ProtoGlobal.groupby('protocol').count()
    ProtoGlobal.columns = ['NumberEvents']
    ProtoGlobal['Protocol'] = ProtoGlobal.index

    return {
        'data': [go.Pie(labels=ProtoGlobal.Protocol,
                        values=ProtoGlobal.NumberEvents,
                        pull=.1,
                        hole=.1,
                        hoverinfo='label+percent',
                        textinfo='label',
                        showlegend=False,
                        marker=dict(colors=colors,
                                    line=dict(color='#000000', width=1)
                                    )
                        )
                 ],
        'layout': go.Layout(
            title='Protocols Used Globally',
            autosize=True,
            font={'family': 'Glacial Indifference', 'color': colors['text']}
        )
    }


@app.callback(
    dash.dependencies.Output('indicator-graphic2b_perc', 'figure'),
    [dash.dependencies.Input('Users-column_Channel_perc', 'value'),
     dash.dependencies.Input('date-picker-range-channels_perc', 'start_date'),
     dash.dependencies.Input('date-picker-range-channels_perc', 'end_date'),
     dash.dependencies.Input('interval_channels_perc', 'n_intervals'),
     dash.dependencies.Input('DB-selection-channel_perc', 'value')])
def update_graph2b(user, start_date, end_date, n, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    df = db_onnections.ChannelDB(from_data=start_date, to_data=end_date, section=db)
    ProtUser = df[['display_name', 'protocol']].copy()
    ProtUser = ProtUser[ProtUser['display_name'] == user]

    ProtUser = ProtUser.groupby('protocol').count()
    ProtUser.columns = ['NumberEvents']
    ProtUser['Protocol'] = ProtUser.index

    return {
        'data': [go.Pie(labels=ProtUser.Protocol,
                        values=ProtUser.NumberEvents,
                        pull=.1,
                        hole=.1,
                        hoverinfo='label+percent',
                        textinfo='label',
                        showlegend=False,
                        marker=dict(colors=colors,
                                    line=dict(color='#000000', width=1))
                        )
                 ],
        'layout': go.Layout(
            title='Protocols Used by {}'.format(user),
            autosize=True,
            font={'family': 'Glacial Indifference', 'color': colors['text']}
        )
    }


@app.callback(
    dash.dependencies.Output('indicator-graphic5b_perc', 'figure'),
    [dash.dependencies.Input('date-picker-range-channels_perc', 'start_date'),
     dash.dependencies.Input('date-picker-range-channels_perc', 'end_date'),
     dash.dependencies.Input('interval_channels_perc', 'n_intervals'),
     dash.dependencies.Input('DB-selection-channel_perc', 'value')])
def update_graph5b(start_date, end_date, n, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    DevIDUser = db_onnections.ChannelDB(from_data=start_date, to_data=end_date, section=db)
    DevIDUser = DevIDUser[['devicetype_id', 'display_name']]
    scalar = 1 + DevIDUser.shape[0]

    DevIDUser = DevIDUser.groupby('devicetype_id').count()
    DevIDUser.columns = ['NumberEvents']
    DevIDUser = DevIDUser.applymap(lambda x: x / scalar)
    DevIDUser['DevIDUser'] = DevIDUser.index
    return {
        'data': [go.Pie(labels=DevIDUser.DevIDUser,
                        values=DevIDUser.NumberEvents,
                        pull=.1,
                        hole=.1,
                        hoverinfo='label+percent',
                        textinfo='label',
                        showlegend=False,
                        marker=dict(colors=colors,
                                    line=dict(color='#000000', width=1)
                                    )
                        )
                 ],
        'layout': go.Layout(
            title='Devices Types Globally',
            autosize=True,
            font={'family': 'Glacial Indifference', 'color': colors['text']}
        )
    }


@app.callback(
    dash.dependencies.Output('indicator-graphic6b_perc', 'figure'),
    [dash.dependencies.Input('Users-column_Channel_perc', 'value'),
     dash.dependencies.Input('date-picker-range-channels_perc', 'start_date'),
     dash.dependencies.Input('date-picker-range-channels_perc', 'end_date'),
     dash.dependencies.Input('interval_channels_perc', 'n_intervals'),
     dash.dependencies.Input('DB-selection-channel_perc', 'value')])
def update_graph6b(user, start_date, end_date, n, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    DevIDUser = db_onnections.ChannelDB(from_data=start_date, to_data=end_date, section=db)
    DevIDUser = DevIDUser[['devicetype_id', 'display_name']]
    DevIDUser = DevIDUser[DevIDUser['display_name'] == user]
    scalar = 1 + DevIDUser.shape[0]

    DevIDUser = DevIDUser.groupby('devicetype_id').count()
    DevIDUser.columns = ['NumberEvents']
    DevIDUser = DevIDUser.applymap(lambda x: x / scalar)
    DevIDUser['DevIDUser'] = DevIDUser.index
    return {
        'data': [go.Pie(labels=DevIDUser.DevIDUser,
                        values=DevIDUser.NumberEvents,
                        pull=.1,
                        hole=.1,
                        hoverinfo='label+percent',
                        textinfo='label',
                        showlegend=False,
                        marker=dict(colors=colors,
                                    line=dict(color='#000000', width=1))
                        )
                 ],
        'layout': go.Layout(
            title='Devices types Used by {}'.format(user),
            autosize=True,
            font={'family': 'Glacial Indifference', 'color': colors['text']}
        )
    }


@app.callback(
    dash.dependencies.Output('indicator-graphic7b_perc', 'figure'),
    [dash.dependencies.Input('date-picker-range-channels_perc', 'start_date'),
     dash.dependencies.Input('date-picker-range-channels_perc', 'end_date'),
     dash.dependencies.Input('interval_channels_perc', 'n_intervals'),
     dash.dependencies.Input('DB-selection-channel_perc', 'value')])
def update_graph7b(start_date, end_date, n, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    DevUser = db_onnections.ChannelDB(from_data=start_date, to_data=end_date, section=db)
    DevUser = DevUser[['hostname', 'display_name']]
    scalar = 1 + DevUser.shape[0]

    DevUser = DevUser.groupby('hostname').count()
    DevUser.columns = ['NumberEvents']
    DevUser = DevUser.applymap(lambda x: x / scalar)
    DevUser['Device'] = DevUser.index
    return {
        'data': [go.Pie(labels=DevUser.Device,
                        values=DevUser.NumberEvents,
                        pull=.1,
                        hole=.1,
                        hoverinfo='label+percent',
                        textinfo='label',
                        showlegend=False,
                        marker=dict(colors=colors,
                                    line=dict(color='#000000', width=1))
                        )
                 ],
        'layout': go.Layout(
            title='Devices Used Globally',
            autosize=True,
            font={'family': 'Glacial Indifference', 'color': colors['text']}
        )
    }


@app.callback(
    dash.dependencies.Output('indicator-graphic8b_perc', 'figure'),
    [dash.dependencies.Input('Users-column_Channel_perc', 'value'),
     dash.dependencies.Input('date-picker-range-channels_perc', 'start_date'),
     dash.dependencies.Input('date-picker-range-channels_perc', 'end_date'),
     dash.dependencies.Input('interval_channels_perc', 'n_intervals'),
     dash.dependencies.Input('DB-selection-channel_perc', 'value')])
def update_graph8b(user, start_date, end_date, n, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    DevUser = db_onnections.ChannelDB(from_data=start_date, to_data=end_date, section=db)
    DevUser = DevUser[['hostname', 'display_name']]
    DevUser = DevUser[DevUser['display_name'] == user]
    scalar = 1 + DevUser.shape[0]

    DevUser = DevUser.groupby('hostname').count()
    DevUser.columns = ['NumberEvents']
    DevUser = DevUser.applymap(lambda x: x / scalar)
    DevUser['Device'] = DevUser.index
    return {
        'data': [go.Pie(labels=DevUser.Device,
                        values=DevUser.NumberEvents,
                        pull=.1,
                        hole=.1,
                        hoverinfo='label+percent',
                        textinfo='label',
                        showlegend=False,
                        marker=dict(colors=colors,
                                    line=dict(color='#000000', width=1))
                        )
                 ],
        'layout': go.Layout(
            title='Devices Used by {}'.format(user),
            autosize=True,
            font={'family': 'Glacial Indifference', 'color': colors['text']}
        )
    }


@app.callback(
    dash.dependencies.Output('Users-column_Channel_perc', 'options'),
    [dash.dependencies.Input('date-picker-range-channels_perc', 'start_date'),
     dash.dependencies.Input('date-picker-range-channels_perc', 'end_date'),
     dash.dependencies.Input('DB-selection-channel_perc', 'value')])
def update_index1(start_date, end_date, db):

    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    df = db_onnections.ChannelDB(from_data=start_date, to_data=end_date, section=db)
    available_users = sorted(df['display_name'].unique())

    return [{'label': i, 'value': i} for i in available_users]


@app.callback(
    dash.dependencies.Output('Users-column_Channel_perc', 'value'),
    [dash.dependencies.Input('date-picker-range-channels_perc', 'start_date'),
     dash.dependencies.Input('date-picker-range-channels_perc', 'end_date'),
     dash.dependencies.Input('DB-selection-channel_perc', 'value')])
def update_index2(start_date, end_date, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    tempdf = db_onnections.ChannelDB(from_data=start_date, to_data=end_date, section=db)

    available_users = sorted(tempdf['display_name'].unique())

    return available_users[0]
