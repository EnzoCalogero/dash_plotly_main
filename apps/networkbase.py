# -*- coding: utf-8 -*-
import flask
from dash.dependencies import Input, Output
from datetime import datetime as dt
import base64
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import os
from datetime import timedelta
import datetime

from app import app
from apps import db_onnections, general_configurations

###############################
# Gives the list of databases #
###############################

list_db = db_onnections.list_dbs()
# print("#################################")
# print("list db{}".format(list_db))
# print(len(list_db))
if len(list_db) == 1:
    enable_db_selector = True
else:
    enable_db_selector = False
# print("#################################")
df = db_onnections.sessionDB(section=general_configurations.Current_active_DB)

df['created_at'] = pd.to_datetime(df['created_at'])

dataMax = df['created_at'].max()
dataMin = dataMax - timedelta(days=30)

###############################################
###    Subnets sides                       ####
###############################################


def SubnetsTrustnessGlobal(df=df):
    '''
    Global subnets used by the whole company
    '''

    Subnet = df[['created_at', 'display_name', 'subnet']].copy()

    Subnet['created_at'] = Subnet['created_at'].dt.date
    Subnet = Subnet.drop_duplicates()
    Subnet = Subnet.groupby('subnet').count()
    Subnet = Subnet[['display_name']]
    Subnet.columns = ['NumberEvents']

    Tot = Subnet.NumberEvents.sum(axis=0)
    Subnet['Trustness'] = Subnet.NumberEvents / Tot * 10
    SubnetDict = Subnet.to_dict(orient="index")

    return SubnetDict


def SubnetsUser(df=df, user=""):
    '''
    Subnets for a single user
    '''

    Subnet = df[['created_at', 'display_name', 'subnet']].copy()
    Subnet = Subnet[Subnet['display_name']==user]

    Subnet['created_at'] = Subnet['created_at'].dt.date
    Subnet = Subnet.drop_duplicates()
    Subnet = Subnet.groupby('subnet').count()
    Subnet = Subnet[['display_name']]
    Subnet.columns = ['NumberEvents']
    Subnet['subnet'] = Subnet.index
    return Subnet


def IPUser(df,user):
    '''
    IPs used by the single user
    '''
    IPAdds = df[['display_name', 'peer_address', 'created_at']].copy()
    IPAdds = IPAdds[IPAdds.display_name == user]
    IPAdds['created_at'] = IPAdds['created_at'].dt.date
    IPAdds = IPAdds.drop_duplicates()

    IPs = IPAdds.groupby('peer_address').count()
    IPs = IPs[['display_name']]
    IPs.columns = ['NumberEvents']
    IPs['IP'] = IPs.index

    return IPs


# Dash Variables
colors = {
    'background': '#111111',
    'text': '#253471'
}

available_Users = df['display_name'].unique()

subnetGlobal = SubnetsTrustnessGlobal(df=df)
Subnets = pd.DataFrame(subnetGlobal)

image_filename = os.getcwd() + '/pics//enzo_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Define Layout
layout = html.Div([
    dcc.Interval(id='interval_network', interval=general_configurations.refresh_interval),
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
                         ), href='/', target="_self"
            ),
            html.H2(
                children="Subnets and IPs ",
                id='H2_networking',
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
    #######################################################
    html.Div([
        html.Div([
            html.Div(children="Source Database"),
        ], className='two columns'),
        html.Div([
            dcc.Dropdown(
                id="DB-selection",
                clearable=False,
                options=[{'label': i, 'value': i} for i in list_db],
                disabled=enable_db_selector,
                value=general_configurations.Current_active_DB)
        ], className='three columns'),
    ], className="row"),
    ######################################################
    html.Div([
        html.Div([
            html.Div(children="Date Range Filter"),
        ], className='two columns'),
        html.Div([
            dcc.DatePickerRange(
                id='date-picker-range-IP',
                #min_date_allowed=dataMin,
                #max_date_allowed=dataMax,
                start_date=dataMin,
                end_date=dataMax),
        ], className='four columns'),
        html.Div([
            html.Div(children="     User: "),
        ], className='one columns'),
        html.Div([
            dcc.Dropdown(
                id='Users-column_IP',
                clearable=False,
                options=[{'label': i, 'value': i} for i in available_Users],
                value=''),
        ], className='three columns'),

    ], className="row"),
    ########################################################
    html.Div([
        dcc.Graph(id='indicator-graphic2_IP',config={'modeBarButtonsToRemove': ['sendDataToCloud'],'displaylogo':False },style={'width': '33%', 'display': 'inline-block'}),
        dcc.Graph(id='indicator-graphic3_IP',config={'modeBarButtonsToRemove': ['sendDataToCloud'],'displaylogo':False },style={'width': '33%', 'display': 'inline-block'}),
        dcc.Graph(id='indicator-graphic4_IP',config={'modeBarButtonsToRemove': ['sendDataToCloud'],'displaylogo':False },style={'width': '34%', 'display': 'inline-block'})
    ], style={'font-family': 'Glacial Indifference',
              'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto',
              'marginRight': 'auto', "width": "157vh",
              'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)'}
    ),
    html.Div(id='intermediate-value_network', style={'display': 'none'}),
    html.Div(id='display-DB'),
    html.Div(id='display-time_network'),

], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "160vh",
          'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)'}
)
# Clousure Layout


@app.callback(Output('date-picker-range-IP', 'end_date'),
              [Input('DB-selection', 'value')])
def update_db_(db):
    df = db_onnections.sessionDB(section=db)

    df['created_at'] = pd.to_datetime(df['created_at'])

    datamax = df['created_at'].max()
    return datamax


@app.callback(Output('date-picker-range-IP', 'start_date'),
              [Input('DB-selection', 'value')])
def update_db_(db):
    df = db_onnections.sessionDB(section=db)

    df['created_at'] = pd.to_datetime(df['created_at'])

    datamax = df['created_at'].max()
    datamin = datamax - timedelta(days=30)
    return datamin


# Cookies Related (First Half)
@app.callback(Output('intermediate-value_network', 'children'),
              [Input('H2_networking', 'children')])
def update_db_(_):
    try:
        cached_db = flask.request.cookies['DB']
    except:
        return list_db[0]
    else:
        return cached_db


# Cookies Related (Second Half)
@app.callback(Output('DB-selection', 'value'),
              [Input('intermediate-value_network', 'children')])
def update_db_(db):
    return db


####################################################################################################


# Time Related function
@app.callback(
    dash.dependencies.Output('display-time_network', 'children'),
    events=[dash.dependencies.Event('interval_network', 'interval')])
def display_time():
    global df
    df = db_onnections.sessionDB(section=general_configurations.Current_active_DB)
    df['created_at'] = pd.to_datetime(df['created_at'])
    return str(datetime.datetime.now())


# DB related Function
@app.callback(
    dash.dependencies.Output('display-DB', 'children'),
    [dash.dependencies.Input('DB-selection', 'value')])
def update_db(db):
    global df
    df = db_onnections.sessionDB(section=db)
    general_configurations.Current_active_DB = db
    return db


# Graphics Related Functions
@app.callback(
    dash.dependencies.Output('indicator-graphic2_IP', 'figure'),
    [dash.dependencies.Input('date-picker-range-IP', 'start_date'),
     dash.dependencies.Input('date-picker-range-IP', 'end_date'),
     dash.dependencies.Input('interval_network', 'n_intervals'),
     dash.dependencies.Input('DB-selection', 'value')
     ])
def update_graph2(start_date, end_date, n, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    df = db_onnections.sessionDB(section=db)

    tempdf = df.copy()
    tempdf = tempdf[tempdf['created_at'] >= start_date]
    tempdf = tempdf[tempdf['created_at'] <= end_date]

    subnetGlobal = SubnetsTrustnessGlobal(df=tempdf)
    Subnets = pd.DataFrame(subnetGlobal)

    return {

        'data': [go.Pie(labels=Subnets.columns,
                        values=Subnets.iloc[0],
                        pull=.1,
                        hole=.1
                        )
                 ],
        'layout': go.Layout(
            title='Subnets Used Globally',
            font={'color': colors['text'], 'family': 'Glacial Indifference'}
        )
    }


@app.callback(
    dash.dependencies.Output('indicator-graphic3_IP', 'figure'),
    [dash.dependencies.Input('Users-column_IP', 'value'),
     dash.dependencies.Input('date-picker-range-IP', 'start_date'),
     dash.dependencies.Input('date-picker-range-IP', 'end_date'),
     dash.dependencies.Input('interval_network', 'n_intervals'),
     dash.dependencies.Input('DB-selection', 'value')
     ])
def update_graph3(user, start_date, end_date, n, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    df = db_onnections.sessionDB(section=db)

    tempdf = df.copy()
    tempdf = tempdf[tempdf['created_at'] >= start_date]
    tempdf = tempdf[tempdf['created_at'] <= end_date]

    Sub = SubnetsUser(df=tempdf, user=user)

    return {
        'data': [go.Pie(labels=Sub.subnet,
                        values=Sub.NumberEvents,
                        pull=.1,
                        hole=.1)
                 ],
        'layout': go.Layout(
            title='Subnets Used by {}'.format(user),
            font={'color': colors['text'], 'family': 'Glacial Indifference'}
        )}


@app.callback(
    dash.dependencies.Output('indicator-graphic4_IP', 'figure'),
    [dash.dependencies.Input('Users-column_IP', 'value'),
     dash.dependencies.Input('date-picker-range-IP', 'start_date'),
     dash.dependencies.Input('date-picker-range-IP', 'end_date'),
     dash.dependencies.Input('interval_network', 'n_intervals'),
     dash.dependencies.Input('DB-selection', 'value')])
def update_graph4(user, start_date, end_date, n, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    df = db_onnections.sessionDB(section=db)

    tempdf = df.copy()
    tempdf = tempdf[tempdf['created_at'] >= start_date]
    tempdf = tempdf[tempdf['created_at'] <= end_date]

    Ips = IPUser(df=tempdf, user=user)

    return {
        'data': [go.Pie(labels=Ips.IP,
                        values=Ips.NumberEvents,
                        pull=.1,
                        hole=.1)
                 ],
        'layout': go.Layout(
            title='IPs Used by {}'.format(user),
            font={'color': colors['text'], 'family':'Glacial Indifference'}
        )
    }


@app.callback(
    Output('Users-column_IP','options'),
    [dash.dependencies.Input('date-picker-range-IP', 'start_date'),
     dash.dependencies.Input('date-picker-range-IP', 'end_date'),
     dash.dependencies.Input('DB-selection', 'value')])
def update_index1(start_date, end_date, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    df = db_onnections.sessionDB(section=db)

    tempdf = df.copy()
    tempdf = tempdf[tempdf['created_at'] >= start_date]
    tempdf = tempdf[tempdf['created_at'] <= end_date]

    available_Users = tempdf['display_name'].unique()
    return [{'label': i, 'value': i} for i in available_Users]


@app.callback(
    Output('Users-column_IP','value'),
    [dash.dependencies.Input('date-picker-range-IP', 'start_date'),
     dash.dependencies.Input('date-picker-range-IP', 'end_date'),
     dash.dependencies.Input('DB-selection', 'value')
     ])
def update_index1(start_date, end_date,db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    df = db_onnections.sessionDB(section=db)
    tempdf = df.copy()
    tempdf = tempdf[tempdf['created_at'] >= start_date]
    tempdf = tempdf[tempdf['created_at'] <= end_date]

    available_Users = tempdf['display_name'].unique()

    return  available_Users[0]
