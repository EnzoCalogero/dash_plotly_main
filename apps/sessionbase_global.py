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
    dcc.Interval(id='interval_sessions_gl', interval=general_configurations.refresh_interval),  # Time Counter Object
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
                children="Sessions over time",
                style={
                    'textAlign': 'center',
                    'font-family': 'Glacial Indifference',
                    'color': colors['text'],
                }
            ),
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
                id="DB-selection-session_gl",
                clearable=False,
                options=[{'label': i, 'value': i} for i in list_db],
                disabled=enable_db_selector,
                value=general_configurations.Current_active_DB
            )
        ], className='three columns'),
        html.Div([
            dcc.Link('Session per User', href='/session_user'),
        ], className='two columns'),
        html.Div([
            dcc.Link('Session Distribution', href='/session_distribution'),
        ], className='two columns'),
    ], className="row"),
    ########################################################################################
    html.Div([
        html.Div([
            dcc.RadioItems(
                id='yaxis-column-Session_gl',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )], style={'width': '20%', 'display': 'inline-block', 'float': 'right'}),
        dcc.Graph(id='indicator-graphic7_gl',
                  config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo': False},
                  style={'width': '100%', 'height': '50vh', 'display': 'inline-block', 'color': colors['text']}),
        dcc.Graph(id='indicator-graphic8_gl',
                  config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo': False},
                  style={'width': '100%', 'height': '50vh', 'display': 'inline-block', 'color': colors['text']})
    ], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto', 'marginRight': 'auto', "width": "157hv",
              'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)', 'color': colors['text']}),

    #############################################################################################
    # Cookies Related
    html.Div(id='intermediate-value_ses_global', style={'display': 'none'}),
    html.Div(id='display-time_session_gl'),
    html.Div(id='display-DB-session_gl'),
], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "160vh",
          'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)'}
)
# Clousure Layout


# DB related Function
@app.callback(
    dash.dependencies.Output('display-DB-session_gl', 'children'),
    [dash.dependencies.Input('DB-selection-session_gl', 'value')])
def update_db(db):
    cached_db = flask.request.cookies['DB']
    general_configurations.Current_active_DB = cached_db
    return cached_db

##################################################################################################


# Cookies Related (First Half)
@app.callback(Output('intermediate-value_ses_global', 'children'),
              [Input('yaxis-column-Session_gl', 'value')])
def update_db_(_):
    try:
        cached_db = flask.request.cookies['DB']
    except:
        return list_db[0]
    else:
        return cached_db


# Cookies Related (Second Half)
@app.callback(Output('DB-selection-session_gl', 'value'),
              [Input('intermediate-value_ses_global', 'children')])
def update_db_(db):
    return db


####################################################################################################
# Time Related function
@app.callback(
    dash.dependencies.Output('display-time_session_gl', 'children'),
    events=[dash.dependencies.Event('interval_sessions_gl', 'interval')])
def display_time_sessions():

    return str(datetime.datetime.now())


@app.callback(
    dash.dependencies.Output('indicator-graphic7_gl', 'figure'),
    [dash.dependencies.Input('yaxis-column-Session_gl', 'value'),
     dash.dependencies.Input('interval_sessions_gl', 'n_intervals'),
     dash.dependencies.Input('DB-selection-session_gl', 'value')])
def update_graph7(yaxis_type, n, db):
    Session = db_onnections.sessionDB(section=db)
    Session = Session[['created_at', 'channel_count']].copy()
    Session['created_at'] = pd.to_datetime(Session['created_at'])
    Session['created_at'] = Session['created_at'].dt.date

    SessionNum = Session.groupby('created_at')[['created_at']].count()
    SessionNum.columns = ['Number sessions']
    SessionNum['Day'] = SessionNum.index
    return {
        'data': [go.Scatter(name='SessionNum per Day',
                            x=SessionNum['Day'],
                            y=SessionNum['Number sessions'],
                            connectgaps=False,
                            fill="tozeroy",
                            line={
                                "color": "rgb(37, 52, 113)",
                                "shape": "linear",
                                "width": 2},
                            fillcolor="rgb(217, 217, 217)")
                 ],
        'layout': go.Layout(
            title="Sessions over Time (Days)",
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
    dash.dependencies.Output('indicator-graphic8_gl', 'figure'),
    [dash.dependencies.Input('yaxis-column-Session_gl', 'value'),
     dash.dependencies.Input('interval_sessions_gl', 'n_intervals'),
     dash.dependencies.Input('DB-selection-session_gl', 'value')])
def update_graph8(yaxis_type, n, db):
    Session = db_onnections.sessionDB(section=db)
    Session = Session[['created_at', 'channel_count']]
    Session['created_at'] = pd.to_datetime(Session['created_at'])
    Session['created_at'] = Session['created_at'].dt.date

    ChannelNum = Session.groupby('created_at')[['channel_count']].sum()
    ChannelNum['Day'] = ChannelNum.index
    return {
        'data': [go.Scatter(name='SessionNum per Day',
                            x=ChannelNum['Day'], y=ChannelNum['channel_count'],
                            connectgaps=False,
                            fill="tozeroy",
                            line={
                                "color": "rgb(37, 52, 113)",
                                "shape": "linear",
                                "width": 2},
                            fillcolor="rgb(217,217, 217, 217)")
                 ],
        'layout': go.Layout(
            title="Channels over Time (Days)",
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
            yaxis={"title": "Aggregate Channels per Day",
                   'type': 'linear' if yaxis_type == 'Linear' else 'log'}
        )}
