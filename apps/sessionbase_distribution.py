# -*- coding: utf-8 -*-
from dash.dependencies import Input, Output
import flask
from datetime import datetime as dt
from app import app
import base64
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.figure_factory as ff
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

dataMax = df['created_at'].max()
dataMin = df['created_at'].min()

# Dash Variables
colors = {
    'background': '#111111',
    'text': '#253471'
}
available_Users = sorted(df['display_name'].unique())

image_filename = os.getcwd() + '/pics//enzo_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Define Layout

layout = html.Div([

    dcc.Interval(id='interval_sessions_dist', interval=general_configurations.refresh_interval),  # Time Counter Object
    html.Div([
        html.Div([
            html.A(
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                         style={
                             'height': '20px',
                             'float': 'left',
                             'position': 'relative',
                             'bottom': '-10px',
                             'width': '100px',
                         }
                         ),
                href='/',
                target="_self"
            ),
            html.H2(
                children="Sessions Distribution",
                id="H2_ses_dist",
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
                id="DB-selection-session_dist",
                clearable=False,
                options=[{'label': i, 'value': i} for i in list_db],
                disabled=enable_db_selector,
                value=general_configurations.Current_active_DB)
        ], className='three columns'),

        html.Div([
            dcc.Link('Session Global', href='/session_global'),
        ], className='two columns'),
        html.Div([
            dcc.Link('Session Per User', href='/session_user'),
        ], className='two columns'),
    ], className="row"),
    ########################################################################################
    html.Div([
        html.Div([
            html.Div(children="Date Range Filter"),
        ], className='two columns'),
        html.Div([
            dcc.DatePickerRange(
                id='date-picker-range-session_dist',
                min_date_allowed=dataMin,
                max_date_allowed=dataMax,
                start_date=dataMin,
                end_date=dataMax
            ),
        ], className='four columns'),
        html.Div([
            html.Div(children="     User: "),
        ], className='one columns'),
        html.Div([
            dcc.Dropdown(
                id='Users-column_dist',
                clearable=False,
                options=[{'label': i, 'value': i} for i in available_Users],
                value='')], className='two columns'),
    ], className="row"),
    #############################################################################################
    html.Div([
        dcc.Graph(id='indicator-graphic5_dist',
                  config={'modeBarButtonsToRemove': ['sendDataToCloud'],
                          'displaylogo': False},
                  style={'width': '50%',
                         'display': 'inline-block',
                         'color': colors['text']}
                  ),
        dcc.Graph(id='indicator-graphic6_dist',
                  config={'modeBarButtonsToRemove': ['sendDataToCloud'],
                          'displaylogo': False},
                  style={'width': '50%',
                         'display': 'inline-block',
                         'color': colors['text']}
                  )
    ], style={'font-family': 'Glacial Indifference',
              'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto',
              'marginRight': 'auto',
              "width": "157hv",
              'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)'}
    ),
    # Cookies Related
    html.Div(id='intermediate-value_ses_dist', style={'display': 'none'}),
    html.Div(id='display-time_session_dist'),
    html.Div(id='display-DB-session_dist'),
], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "160vh",
          'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)'}
)
# Clousure Layout


# Cookies Related (First Half)
@app.callback(Output('intermediate-value_ses_dist', 'children'),
              [Input('H2_ses_dist', 'children')])
def update_db_(_):
    try:
        cached_db = flask.request.cookies['DB']
    except:
        return list_db[0]
    else:
        return cached_db


# Cookies Related (Second Half)
@app.callback(Output('DB-selection-session_dist', 'value'),
              [Input('intermediate-value_ses_dist', 'children')])
def update_db_(db):
    return db


# DB related Function
@app.callback(
    dash.dependencies.Output('display-DB-session_dist', 'children'),
    [dash.dependencies.Input('DB-selection-session_dist', 'value')])
def update_db(db):
    general_configurations.Current_active_DB = db
    return db


# Time Related function
@app.callback(
    dash.dependencies.Output('display-time_session_dist', 'children'),
    events=[dash.dependencies.Event('interval_sessions_dist', 'interval')])
def display_time_sessions():

    return str(datetime.datetime.now())


@app.callback(
    dash.dependencies.Output('indicator-graphic5_dist', 'figure'),
    [dash.dependencies.Input('Users-column_dist', 'value'),
     dash.dependencies.Input('date-picker-range-session_dist', 'start_date'),
     dash.dependencies.Input('date-picker-range-session_dist', 'end_date'),
     dash.dependencies.Input('interval_sessions_dist', 'n_intervals'),
     dash.dependencies.Input('DB-selection-session_dist', 'value')])
def update_graph5(user, start_date, end_date, n, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    tempdf = db_onnections.sessionDB(section=db)
    tempdf = tempdf[tempdf['created_at'] >= start_date]
    GlobalDuration = tempdf[tempdf['created_at'] <= end_date]
    GlobalDuration['Duration'] = GlobalDuration['hourout'] - GlobalDuration['hourin']

    GlobalDuration = GlobalDuration[GlobalDuration['Duration'] >= 0]
    GlobalDuration = GlobalDuration[['display_name', 'Duration']]

    User = GlobalDuration[GlobalDuration['display_name'] == user]
    hist_data = [GlobalDuration.Duration, User.Duration]

    group_labels = ['{}'.format('Global'), '{}'.format(user)]
    colors_ = ['#253471', '#199dd9']
    fig = ff.create_distplot(hist_data, group_labels, colors=colors_)
    fig.layout.update({'title': "Session Durations"}, font={'color': colors['text'], 'family': ' Glacial Indifference'})
    return fig


@app.callback(
    dash.dependencies.Output('indicator-graphic6_dist', 'figure'),
    [dash.dependencies.Input('Users-column_dist', 'value'),
     dash.dependencies.Input('date-picker-range-session_dist', 'start_date'),
     dash.dependencies.Input('date-picker-range-session_dist', 'end_date'),
     dash.dependencies.Input('interval_sessions_dist', 'n_intervals'),
     dash.dependencies.Input('DB-selection-session_dist', 'value')])
def update_graph5(user, start_date, end_date, n, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    tempdf = db_onnections.sessionDB(section=db)
    tempdf = tempdf[tempdf['created_at'] >= start_date]
    GlobalsessNumber = tempdf[tempdf['created_at'] <= end_date]
    GlobalsessNumber = GlobalsessNumber[['display_name', 'channel_count']]

    User = GlobalsessNumber[GlobalsessNumber['display_name'] == user]
    hist_data = [GlobalsessNumber.channel_count, User.channel_count]

    group_labels = ['{}'.format('Global'), '{}'.format(user)]
    colors_ = ['#253471', '#199dd9']
    fig = ff.create_distplot(hist_data, group_labels, colors=colors_)
    fig.layout.update({'title': "Number of Sessions"}, font={'color': colors['text'], 'family': 'Glacial Indifference'},
                      scene=dict(
                          xaxis=dict(range=[0, 10])
                      )
                      )
    return fig


@app.callback(
    Output('Users-column_dist', 'options'),
    [dash.dependencies.Input('date-picker-range-session_dist', 'start_date'),
     dash.dependencies.Input('date-picker-range-session_dist', 'end_date'),
     dash.dependencies.Input('DB-selection-session_dist', 'value')])
def update_index1(start_date, end_date, db):

    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    tempdf = db_onnections.sessionDB(section=db)
    tempdf = tempdf[tempdf['created_at'] >= start_date]
    tempdf = tempdf[tempdf['created_at'] <= end_date]

    available_Users = sorted(tempdf['display_name'].unique())
    return [{'label': i, 'value': i} for i in available_Users]


@app.callback(
    Output('Users-column_dist', 'value'),
    [dash.dependencies.Input('date-picker-range-session_dist', 'start_date'),
     dash.dependencies.Input('date-picker-range-session_dist', 'end_date'),
     dash.dependencies.Input('DB-selection-session_dist', 'value')])
def update_index1(start_date, end_date, db):

    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    tempdf = db_onnections.sessionDB(section=db)
    tempdf = tempdf[tempdf['created_at'] >= start_date]
    tempdf = tempdf[tempdf['created_at'] <= end_date]

    available_Users = sorted(tempdf['display_name'].unique())

    return available_Users[0]
