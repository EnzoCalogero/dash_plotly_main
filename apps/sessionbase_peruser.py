# -*- coding: utf-8 -*-
from dash.dependencies import Input, Output
import flask
from app import app
import base64
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import os
import datetime

from apps import db_onnections, general_configurations
list_db = db_onnections.list_dbs()

if len(list_db) == 1:
    enable_db_selector = True
else:
    enable_db_selector = False

df = db_onnections.sessionDB(section=general_configurations.Current_active_DB)
df['created_at'] = pd.to_datetime(df['created_at'])

# Dash Variables
colors = {
    'background': '#111111',
    'text': '#253471'
}

image_filename = os.getcwd() + '/pics//enzo_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Define Layout

layout = html.Div([
    dcc.Interval(id='interval_sessions_user', interval=general_configurations.refresh_interval),
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
                children="Sessions Timeseries per User",
                style={
                    'textAlign': 'center',
                    'font-family': 'Glacial Indifference',
                    'color': colors['text'],
                }),
        ], className='ten columns'),
        html.Div([
            html.A('Set the Default DB', href='/setdb', target="_blank")
        ], className='two columns'),
    ], className="row"),
    ##########################################################################################
    html.Div([
        html.Div(
            [
                html.Div(children="Source Database"),
            ], className='two columns'),
        html.Div([
            dcc.Dropdown(
                id="DB-selection-session_user",
                clearable=False,
                options=[{'label': i, 'value': i} for i in list_db],
                disabled=enable_db_selector,
                value=general_configurations.Current_active_DB)
        ], className='three columns'),
        html.Div([
            dcc.Link('Session Global', href='/session_global'),
        ], className='two columns'),
        html.Div([
            dcc.Link('Session Distribution', href='/session_distribution'),
        ], className='two columns'),
    ], className="row"),
    ########################################################################################
    html.Div([
        html.Div([
            dcc.RadioItems(
                id='yaxis-column-Session_user',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )], style={'width': '10%', 'display': 'inline-block', 'float': 'right'}),
    ],),
    ###########################################################################################
    html.Div([
        dcc.Graph(id='indicator-Session-TimeSeries-users_',
                  config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo': False},
                  style={'width': '100%', 'height': '50vh', 'display': 'inline-block', 'color': colors['text']}),
        dcc.Graph(id='indicator-Channel-TimeSeries-users_',
                  config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo': False},
                  style={'width': '100%', 'height': '50vh', 'display': 'inline-block', 'color': colors['text']}),
    ], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto', 'marginRight': 'auto', "width": "157hv",
              'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113, 0.4)', 'color': colors['text']}
    ),
    #############################################################################################
    # Cookies Related
    html.Div(id='intermediate-value_ses_user', style={'display': 'none'}),
    html.Div(id='display-time_session_user'),

    html.Div(id='display-DB-session_user'),
], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "160vh",
          'boxShadow': '0px 0px 5px 5px rgba(37 ,52, 113, 0.4)'}
)
# Clousure Layout


##################################################################################################

# Cookies Related (First Half)
@app.callback(Output('intermediate-value_ses_user', 'children'),
              [Input('yaxis-column-Session_user', 'value')])
def update_db_(_):
    try:
        cached_db = flask.request.cookies['DB']
    except:
        return list_db[0]
    else:
        return cached_db


# Cookies Related (Second Half)
@app.callback(Output('DB-selection-session_user', 'value'),
              [Input('intermediate-value_ses_user', 'children')])
def update_db_(db):
    return db


####################################################################################################

@app.callback(
    dash.dependencies.Output('indicator-Session-TimeSeries-users_', 'figure'),
    [dash.dependencies.Input('yaxis-column-Session_user', 'value'),
     dash.dependencies.Input('interval_sessions_user', 'n_intervals'),
     dash.dependencies.Input('DB-selection-session_user', 'value')])
def update_graph7(yaxis_type, n, db):
    Session = db_onnections.sessionDB(section=db)
    Session = Session[['display_name', 'created_at', 'channel_count']]
    Session['created_at'] = pd.to_datetime(Session['created_at'])
    Session['created_at'] = Session['created_at'].dt.date

    alpha = Session.pivot_table(index='created_at', columns='display_name', values='channel_count', aggfunc="count")
    alpha = alpha.fillna(0)
    data_ = [{
        'x': alpha.index,
        'y': alpha[col],
        'name': col,
        'connectgaps': False,
        'fill': "tozeroy",
        'line': {
            "shape": "linear",
            "width": 2}
    } for col in alpha.columns]
    return {
        'data': data_,
        'layout': go.Layout(
            title="Sessions per Day",
            font={'color': colors['text'], 'family': 'Glacial Indifference'},
            xaxis=dict(
                tickangle=-25,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='todate'),
                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(),
                type='date'),
            yaxis={"title": "Sessions per Day",
                   'type': 'linear' if yaxis_type == 'Linear' else 'log'}
        )}


@app.callback(
    dash.dependencies.Output('indicator-Channel-TimeSeries-users_', 'figure'),
    [dash.dependencies.Input('yaxis-column-Session_user', 'value'),
     dash.dependencies.Input('interval_sessions_user', 'n_intervals'),
     dash.dependencies.Input('DB-selection-session_user', 'value')])
def update_graph7(yaxis_type, n, db):
    Channel = db_onnections.sessionDB(section=db)

    Channel = Channel[['display_name', 'created_at', 'channel_count']]
    Channel['created_at'] = pd.to_datetime(Channel['created_at'])
    Channel['created_at'] = Channel['created_at'].dt.date

    alpha = Channel.pivot_table(index='created_at', columns='display_name', values='channel_count', aggfunc="sum")
    alpha = alpha.fillna(0)

    data_ = [{
        'x': alpha.index,
        'y': alpha[col],
        'name': col,
        'connectgaps': False,
        'fill': "tozeroy",
        'line': {
            "shape": "linear",
            "width": 2}
    } for col in alpha.columns]
    return {
        'data': data_,
        'layout': go.Layout(
            title="Channels Per Days",
            font={'color': colors['text'], 'family': 'Glacial Indifference'},
            xaxis=dict(
                tickangle=-25,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='todate'),
                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(),
                type='date'),
            yaxis={"title": "Chanels per Day",
                   'type': 'linear' if yaxis_type == 'Linear' else 'log'}
        )}


# DB related Function
@app.callback(
    dash.dependencies.Output('display-DB-session_user', 'children'),
    [dash.dependencies.Input('DB-selection-session_user', 'value')])
def update_db(db):
    general_configurations.Current_active_DB = db
    return db


# Time Related function
@app.callback(
    dash.dependencies.Output('display-time_session_user', 'children'),
    events=[dash.dependencies.Event('interval_sessions_user', 'interval')])
def display_time_sessions():

    return str(datetime.datetime.now())
