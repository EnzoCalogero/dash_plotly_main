# -*- coding: utf-8 -*-
import os
import flask
from datetime import timedelta
import datetime
import base64
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from app import app
from apps import db_onnections, general_configurations


def generate_table(dataframe, max_rows=100):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


######################################
## Initial time references         ##
#####################################
FROM = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=240)).strftime("%Y-%m-%d")
TO = (pd.to_datetime(datetime.datetime.now())).strftime("%Y-%m-%d")

# define list DBs
list_db = db_onnections.list_dbs()
if len(list_db) == 1:
    enable_db_selector = True
else:
    enable_db_selector = False

df = db_onnections.taskvsChannel(from_data=FROM, to_data=TO, section=general_configurations.Current_active_DB)
df['created_at'] = pd.to_datetime(df['created_at'])

available_users = list(df['user_name'].unique())
available_users = available_users + ["-- all --"]
available_users = sorted(available_users)

available_device = list(df["device_name"].unique())
available_device = available_device + ["-- all --"]
available_device = sorted(available_device)

dataMax = df['created_at'].max()
dataMin = df['created_at'].min()

# Dash Variables
colors = {
    'background': '#111111',
    'text': '#253471'
}

image_filename = os.getcwd() + '/pics//enzo_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Define Layout
layout = html.Div([
    dcc.Interval(id='interval_sessions_gl', interval=general_configurations.refresh_interval),
    html.Div([
        html.Div([
            html.A(
                html.Img(
                    src='data:image/png;base64,{}'.format(encoded_image.decode()),
                    style={
                        'height': '20px',
                        'float': 'left',
                        'position': 'relative',
                        'bottom': '-10px',
                        'width': '100px'}
                ), href='/', target="_self"),
            html.H2(
                children="Connections",
                id='H2_chan_sand',
                style={
                    'textAlign': 'center',
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
            html.Div(children= "Source Database"),
        ], className='two columns'),
        html.Div([
            dcc.Dropdown(
                id="DB-selection-connection",
                clearable=False,
                options=[{'label': i, 'value': i} for i in list_db],
                disabled=enable_db_selector,
                value=general_configurations.Current_active_DB)
        ], className='three columns'),
    ], className="row"),
    ########################################################################################
    html.Div([
        html.Div([
            dcc.Graph(id='Connection-TS01',
                      config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo': False},
                      style={'width': '100%', 'height': '50vh', 'display': 'inline-block', 'color': colors['text']}
                      ),
        ], className="row"),
    ], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto', 'marginRight': 'auto', "width": "157hv",
              'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)', 'color': colors['text']}
    ),
    ###############################################################################################
    html.Div([
        html.Div([
            dcc.DatePickerSingle(
                id="Selector-Date",
                is_RTL=False,
                first_day_of_week=3,
                date=dataMax),
        ], className='two columns'),
        html.Div([
            html.Div(children="     User: "),
        ], className='one columns'),
        html.Div([
            dcc.Dropdown(
                id='Users-Connection',
                clearable=False,
                options=[{'label': i, 'value': i} for i in available_users],
                value='-- all --')
        ], className='two columns'),
        html.Div([
            html.Div(children="     Device: "),
        ], className='one columns'),
        html.Div([
            dcc.Dropdown(
                id='Device-Connection',
                clearable=False,
                options=[{'label': i, 'value': i} for i in available_device],
                value='-- all --')
        ], className='two columns'),
    ], className="row"),
    ##############################################################################################
    html.Div(children=[
        html.H4(children='Sessions List'),
        html.Div(id='table-container'),
    ]),
    html.Div(id='intermediate-value__connection', style={'display': 'none'}),
    html.Div(id='display-time_connection'),
    html.Div(id='display-DB-connection'),
], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "160vh",
          'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113, 0.4)'}
)
# Closure Layout


# Cookies Related (First Half)
@app.callback(
    dash.dependencies.Output('intermediate-value__connection', 'children'),
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
    dash.dependencies.Output('DB-selection-connection', 'value'),
    [dash.dependencies.Input('intermediate-value__connection', 'children')])
def update_db_chan_heat_(db):
    return db


@app.callback(
    dash.dependencies.Output('Connection-TS01', 'figure'),
    [dash.dependencies.Input('DB-selection-connection', 'value')])
def update_connection_ts01(db):
    temp = db_onnections.taskvsChannel(from_data=FROM, to_data=TO, section=db)
    temp['created_at'] = pd.to_datetime(temp['created_at'])
    temp['created_at'] = temp['created_at'].dt.date
    alpha = temp.pivot_table(index='created_at', columns="Connection", values='session_id', aggfunc="count")
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
            title="Basic Template vs Tasks Connections over Time (Days)",
            font={'color': colors['text'], 'family': ' Glacial Indifference'},
            xaxis=dict(
                tickangle=25,
                rangeslider=dict(),
                type='date'),
            yaxis={"title": "Connections per Day",
                   'type': 'linear'}
        )
    }


@app.callback(Output('table-container', 'children'),
              [Input('DB-selection-connection', 'value'),
               Input('Users-Connection', 'value'),
               Input('Device-Connection', 'value'),
               Input('Selector-Date', 'date')])
def update_table(db, user, device, select_date):
    select_date = pd.to_datetime(select_date)

    select_date = select_date.strftime('%Y-%m-%d')

    dff = db_onnections.taskvsChannel(from_data=FROM, to_data=TO, section=db)

    dff["data"] = pd.to_datetime(dff["created_at"])
    dff["data"] = dff["data"].astype(str).str[0:10]

    dff = dff[dff["data"] == select_date]
    dff["created_at"] = dff["created_at"].astype(str).str[0:19]
    dff = dff[["created_at", "session_id", "Connection", "template", "user_name", "device_name", "name"]]

    if user != "-- all --":
        dff = dff[dff["user_name"] == user]

    if device != "-- all --":
        dff = dff[dff["device_name"] == device]

    return generate_table(dff.sort_values(by=['created_at']))


@app.callback(
    Output('Users-Connection', 'options'),
    [Input('Selector-Date', 'date'),
     dash.dependencies.Input('DB-selection-connection', 'value')])
def update_index1(select_date, db):

    select_date = pd.to_datetime(select_date)
    select_date = select_date.strftime('%Y-%m-%d')

    dff = db_onnections.taskvsChannel(from_data=FROM, to_data=TO, section=db)

    dff["data"] = pd.to_datetime(dff["created_at"])
    dff["data"] = dff["data"].astype(str).str[0:10]

    dff = dff[dff["data"] == select_date]

    available_users = list(dff['user_name'].unique())
    available_users = available_users + ["-- all --"]
    available_users = sorted(available_users)

    return [{'label': i, 'value': i} for i in available_users]


@app.callback(
    Output('Device-Connection', 'options'),
    [Input('Selector-Date', 'date'),
     dash.dependencies.Input('DB-selection-connection', 'value')])
def update_index1(select_date, db):

    select_date = pd.to_datetime(select_date)
    select_date = select_date.strftime('%Y-%m-%d')

    dff = db_onnections.taskvsChannel(from_data=FROM, to_data=TO, section=db)

    dff["data"] = pd.to_datetime(dff["created_at"])
    dff["data"] = dff["data"].astype(str).str[0:10]

    dff = dff[dff["data"] == select_date]

    available_device = list(dff["device_name"].unique())
    available_device = available_device + ["-- all --"]
    available_device = sorted(available_device)

    return [{'label': i, 'value': i} for i in available_device]


@app.callback(
    Output('Selector-Date', 'date'),
    [Input('DB-selection-connection', 'value')])
def update_index1(db):
    FROM = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=120)).strftime("%Y-%m-%d")
    TO = (pd.to_datetime(datetime.datetime.now())).strftime("%Y-%m-%d")
    df = db_onnections.taskvsChannel(from_data=FROM, to_data=TO, section=db)
    df['created_at'] = pd.to_datetime(df['created_at'])
    return  df['created_at'].max()
