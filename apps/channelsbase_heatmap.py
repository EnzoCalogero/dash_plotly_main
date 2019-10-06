# -*- coding: utf-8 -*-
import base64
import pandas as pd
import flask
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
    html.Div([
        html.Div([
            dcc.Interval(id='interval_channels_heat', interval=general_configurations.refresh_interval),
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
                children='Channels HeatMaps',
                id="H2_chan_heat",
                style={'textAlign': 'center',
                       'font-family': 'Glacial Indifference',
                       'color': colors['text']}
            )
        ], className='ten columns'),
        html.Div([
             html.A('Set the Default DB', href='/setdb', target="_blank")
        ], className='two columns'),
    ], className="row"),
##########################################################################################
    html.Div([
            html.Div([
                html.Div(children="Source Database"),
            ], className='two columns'),
            html.Div([
                dcc.Dropdown(
                    id="DB-selection-channel_heat",
                    clearable=False,
                    options=[{'label': i, 'value': i} for i in list_db],
                    disabled=enable_db_selector,
                    value=general_configurations.Current_active_DB)
            ], className='three columns'),
            html.Div([
                 dcc.Link('Percentages', href='/channel_percent'),
            ], className='two columns'),
            html.Div([
                 dcc.Link('Sankeys', href='/channel_sankey'),
            ], className='two columns'),
    ], className="row"),
    html.Div([
        html.Div([
             html.Div(children="Date Range Filter"),
        ], className='two columns'),
        html.Div([
            dcc.DatePickerRange(
                     id='date-picker-range-channels_heat',
                     minimum_nights=1,
                     start_date='01/01/2018',
                     end_date=dataMax
            ),
        ], className='five columns'),
    ], className="row"),
##########################################################################################################################
    html.Div([
           dcc.Graph(id='indicator-graphic4b_heat',
                     config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo': False},
                     style={'width': '100%', 'display': 'inline-block', 'color': colors['text']}
                     ),
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
                   'color': colors['text']}
           ),
    ], className="row"),
#####################################################################################################
    html.Div([
        html.Div([
            html.Div(children="User"),
        ], className='one columns'),
        html.Div([
            dcc.Dropdown(
                id='Users-column_Channel_heat',
                clearable=False,
                options=[{'label': i, 'value': i} for i in available_Users],
                value=available_Users[0]),
        ], className='two columns'),
    ], className="row"),
    #####################################################################################################
    html.Div([
        dcc.Graph(id='indicator-graphic3b_heat',
                  config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo':False},
                  style={'width': '100%', 'display': 'inline-block', 'color': colors['text']}),
    ], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto', 'marginRight': 'auto', "width": "157vh",
              'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)', 'color': colors['text']}),
           # Cookies Related
           html.Div(id='intermediate-value_chan_heat', style={'display': 'none'}),
           html.Div(id='display-time_channels_heat'),
           html.Div(id='display-DB-channel_heat'),
], style={'font-family': 'Glacial Indifference',
          'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto',
          'marginRight': 'auto',
          "width": "160vh",
          'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)'}
)
# Closure Layout


@app.callback(dash.dependencies.Output('date-picker-range-channels_heat', 'end_date'),
              [dash.dependencies.Input('DB-selection-channel_heat', 'value')])
def update_db_(db):
    from_day = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=120)).strftime("%Y-%m-%d")

    df = db_onnections.ChannelDB(from_data=from_day, section=db)

    df['created_at'] = pd.to_datetime(df['created_at'])

    datamax = df['created_at'].max()
    return datamax


@app.callback(dash.dependencies.Output('date-picker-range-channels_heat', 'start_date'),
              [dash.dependencies.Input('DB-selection-channel_heat', 'value')])
def update_db_(db):
    from_day = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=120)).strftime("%Y-%m-%d")

    df = db_onnections.ChannelDB(from_data=from_day, section=db)

    df['created_at'] = pd.to_datetime(df['created_at'])

    datamax = df['created_at'].max()
    datamin = datamax - timedelta(days=30)
    return datamin


# DB related Function
@app.callback(
    dash.dependencies.Output('display-DB-channel_heat', 'children'),
    [dash.dependencies.Input('DB-selection-channel_heat', 'value')])
def update_db(db):
    cached_db = flask.request.cookies['DB']
    general_configurations.Current_active_DB = cached_db
    return cached_db


# Cookies Related (First Half)
@app.callback(
    dash.dependencies.Output('intermediate-value_chan_heat', 'children'),
    [dash.dependencies.Input('H2_chan_heat', 'children')])
def update_db_chan_heat(_):
    try:
        cached_db = flask.request.cookies['DB']
    except:
        return list_db[0]
    else:
        return cached_db


# Cookies Related (Second Half)
@app.callback(
    dash.dependencies.Output('DB-selection-channel_heat', 'value'),
    [dash.dependencies.Input('intermediate-value_chan_heat', 'children')])
def update_db_chan_heat_(db):
    return db


##########################
# Time Related function  #
##########################
@app.callback(
    dash.dependencies.Output('display-time_channels_heat', 'children'),
    events=[dash.dependencies.Event('interval_channels_heat', 'interval')])
def display_time():

    return str(datetime.datetime.now())


#################################
# Graphics Related Functions    #
#################################
@app.callback(
    dash.dependencies.Output('indicator-graphic3b_heat', 'figure'),
    [dash.dependencies.Input('Users-column_Channel_heat', 'value'),
     dash.dependencies.Input('date-picker-range-channels_heat', 'start_date'),
     dash.dependencies.Input('date-picker-range-channels_heat', 'end_date'),
     dash.dependencies.Input('interval_channels_heat', 'n_intervals'),
     dash.dependencies.Input('DB-selection-channel_heat', 'value')])
def update_graph3b(user, start_date, end_date, n, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    ProtocolUser= db_onnections.ChannelDB(from_data=start_date, to_data=end_date, section=db)
    ProtocolUser = ProtocolUser[ProtocolUser['display_name'] == user]
    ProtocolUser = ProtocolUser[['hostname', 'protocol']]
    #scalar = 1 + ProtocolUser.shape[0]
    ProtocolUser = pd.crosstab(ProtocolUser.hostname, ProtocolUser.protocol)
    # ProtocolUser = ProtocolUser.applymap(lambda x: x / scalar)

    hovertext = list()
    zz = [ProtocolUser[name] for name in ProtocolUser.columns]

    for yi, yy in enumerate(ProtocolUser.columns):
        hovertext.append(list())
        for xi, xx in enumerate(ProtocolUser.index):
            hovertext[-1].append(
                'User: {} <br />Protocol: {}<br />Device: {}<br />Connections in the Time Range: {}'.format(
                    user, yy, xx, zz[yi][xi]
                )
            )

    return {
        'data': [go.Heatmap(z=[ProtocolUser[name] for name in ProtocolUser.columns],
                            y=ProtocolUser.columns,
                            x=ProtocolUser.index,
                            hoverinfo='text',
                            text=hovertext,
                            colorscale=[[0, 'rgb(217,217,217)'], [1, 'rgb(37,52,113)']],
                            showscale=False,
                            )
                 ],
        'layout': go.Layout(
                            title='Protocols vs Devices by {}'.format(user),
                            font={'family': 'Glacial Indifference', 'color': colors['text']},

                            xaxis={
                               'showgrid': True,
                               "tickangle": -35,
                               'showticklabels': True,
                               'linecolor': 'black'},
                            yaxis={
                               'visible': True,
                               "tickangle": -35,
                               'showticklabels': True,
                               'showgrid': True,
                               'linecolor': 'black'}
        )
    }


@app.callback(
    dash.dependencies.Output('indicator-graphic4b_heat', 'figure'),
    [dash.dependencies.Input('date-picker-range-channels_heat', 'start_date'),
     dash.dependencies.Input('date-picker-range-channels_heat', 'end_date'),
     dash.dependencies.Input('interval_channels_heat', 'n_intervals'),
     dash.dependencies.Input('DB-selection-channel_heat', 'value')])
def update_graph4b(start_date, end_date, n, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    ProtocolUser = db_onnections.ChannelDB(from_data=start_date, to_data=end_date, section=db)
    ProtocolUser = ProtocolUser[['hostname', 'protocol']]
    ProtocolUser = pd.crosstab(ProtocolUser.hostname, ProtocolUser.protocol)

    hovertext = list()
    zz = [ProtocolUser[name] for name in ProtocolUser.columns]
    for yi, yy in enumerate(ProtocolUser.columns):
        hovertext.append(list())
        for xi, xx in enumerate(ProtocolUser.index):
            hovertext[-1].append(
                'Protocol: {}<br />Device: {}<br />Connections in the Time Range: {}'.format(yy, xx, zz[yi][xi]))

    return {
        'data': [go.Heatmap(z=[ProtocolUser[name] for name in ProtocolUser.columns],
                            y=ProtocolUser.columns,
                            x=ProtocolUser.index,
                            hoverinfo='text',
                            text=hovertext,
                            colorscale=[[0, 'rgb(217,217,217)'], [1, 'rgb(37,52,113)']],
                            showscale=False
                            )
                 ],
        'layout': go.Layout(
            title='Protocols vs Devices Globally',
            font={'family': 'Glacial Indifference', 'color': colors['text']},
            xaxis={
                               'showgrid': True,
                               'showticklabels': True,
                               "tickangle": -35,
                               'linecolor': 'black'},
            yaxis={
                                'visible': True,
                                "tickangle": -35,
                                'showticklabels': True,
                                'showgrid': True,
                                'linecolor': 'black'}
        )
    }


@app.callback(
    dash.dependencies.Output('Users-column_Channel_heat', 'options'),
    [dash.dependencies.Input('date-picker-range-channels_heat', 'start_date'),
     dash.dependencies.Input('date-picker-range-channels_heat', 'end_date'),
     dash.dependencies.Input('DB-selection-channel_heat', 'value')])
def update_index1(start_date, end_date, db):

    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    df = db_onnections.ChannelDB(from_data=start_date, to_data=end_date, section=db)
    available_users = sorted(df['display_name'].unique())

    return [{'label': i, 'value': i} for i in available_users]


@app.callback(
    dash.dependencies.Output('Users-column_Channel_heat', 'value'),
    [dash.dependencies.Input('date-picker-range-channels_heat', 'start_date'),
     dash.dependencies.Input('date-picker-range-channels_heat', 'end_date'),
     dash.dependencies.Input('DB-selection-channel_heat', 'value')])
def update_index2(start_date, end_date, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    tempdf = db_onnections.ChannelDB(from_data=start_date, to_data=end_date, section=db)

    available_users = sorted(tempdf['display_name'].unique())

    return available_users[0]
