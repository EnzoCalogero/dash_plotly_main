# -*- coding: utf-8 -*-
from dash.dependencies import Input, Output
import base64
import flask
import os
import pandas as pd
from datetime import timedelta
from datetime import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import datetime

from app import app
from apps import db_onnections, general_configurations

colors = {
    'background': '#111111',
    'text': '#253471',
}

FROM = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=90)).strftime("%Y-%m-%d")
Data = db_onnections.tasksDB(from_data=FROM, section=general_configurations.Current_active_DB)

list_db = db_onnections.list_dbs()

# Enable the DB selector
if len(list_db) == 1:
    enable_db_selector = True
else:
    enable_db_selector = False

image_filename = os.getcwd() + '/pics//enzo_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# if Data.empty:
#     layout = html.Div([
#         html.Div([
#             html.A(
#                 html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={
#                     'height':'20px',
#                     'float':'left',
#                     'position':'relative',
#                     'bottom':'-10px',
#                     'width':'100px',
#                 }), href='/', target="_self"),
#             html.H2(
#                 children="Analytics Menu",
#                 style={
#                     'textAlign':'center',
#                     'text':colors['text'],
#                     'font-family':'Glacial Indifference',
#                     'color':colors['text'],
#                     'bgcolor':colors['background']
#                 })
#         ], style={'height':'60px','width':'70%'}),
#         html.Div([
#             html.H3(
#                 children="No Available Data for Analytics Tasks ",
#
#                 style={
#                     'textAlign': 'center',
#                     'text': colors['text'],
#                     'font-family': 'Glacial Indifference',
#                     'color': colors['text'],
#                     'bgcolor': colors['background']
#                 })
#         ]),
#     ], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
#               'marginLeft': 'auto', 'marginRight': 'auto', "width": "160vh", 'color': colors['text'],
#               'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)'})
#
# else:
# Dash Variables

dataMax = Data['event_time'].max()
dataMin = Data['event_time'].min()

image_filename = os.getcwd() + '/pics//enzo_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

layout = html.Div([
    html.Div([
        html.Div([
            dcc.Interval(id='interval_tasks_sand', interval= general_configurations.refresh_interval),
            html.A(
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={
                    'height': '20px',
                    'float': 'left',
                    'position': 'relative',
                    'bottom': '-10px',
                    'width': '100px',
                }), href='/', target="_self"),
            html.H2(
                children='Tasks: Users vs Devices',
                id='H2_task_sand',
                style={
                    'textAlign': 'center',
                    'color': colors['text'],
                    'font-family': 'Glacial Indifference',
                    'bgcolor': colors['background']
                }
            ),
        ], className='ten columns'),
        html.Div([
            html.A('Set the Default DB', href='/setdb', target="_blank")
        ], className='two columns'),
    ], className="row"),
    #########################################################################################
    html.Div([
        html.Div(
            [
                html.Div(children="Source Database"),
            ], className='two columns'),
        html.Div([
            dcc.Dropdown(
                id="DB-selection-task-sand",
                clearable=False,
                options=[{'label': i, 'value': i} for i in list_db],
                disabled=enable_db_selector,
                value=general_configurations.Current_active_DB)
        ], className='three columns'),
        html.Div([
            dcc.Link('Sankey per User', href='/tasks_sankey_user'),
        ], className='two columns'),
        html.Div([
            dcc.Link('Timeseries', href='/tasks_timeseries'),
        ], className='two columns'),
        html.Div([
            dcc.Link('Stream Line', href='/tasks_river'),
        ], className='two columns'),
    ], className="row"),
    ########################################################################################
    html.Div([
        html.Div([
            html.Div(children="Date Range Filter"),
        ], className='two columns'),
        html.Div([
            dcc.DatePickerRange(
                id='date-picker-range-tasks_sand',
                start_date=dataMin,
                end_date=dataMax
            ),
        ], className='four columns'),
    ], className="row"),
    #############################################################################################
    html.Div([
        dcc.Graph(id='graphic-Task3_sand',
                  config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo': False},
                  style={'width': '100%', 'display': 'inline-block'}),
    ], style={'font-family': 'Glacial Indifference',
              'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto',
              'marginRight': 'auto',
              "width": "157vh",
              'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113, 0.4)'
              }
    ),
    html.Div([
        dcc.Graph(id='graphic-Task1_sand',
                  config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo': False},
                  style={'width': '100%', 'display': 'inline-block'}),
    ], style={'font-family': 'Glacial Indifference',
              'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto',
              'marginRight': 'auto',
              "width": "157vh",
              'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)'
              }
    ),
    html.Div(id='intermediate-value_tasks_sand', style={'display': 'none'}),
    html.Div(id='display-time_tasks_sand'),
    html.Div(id='display-DB-tasks-sand'),

], style={'font-family': 'Glacial Indifference',
          'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto',
          'marginRight': 'auto',
          'width': '160vh',
          'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)'}
)
# Closure Layout


# Cookies Related (First Half)
@app.callback(
    dash.dependencies.Output('intermediate-value_tasks_sand', 'children'),
    [dash.dependencies.Input('H2_task_sand', 'children')])
def update_db_chan_heat(_):
    try:
        cached_db = flask.request.cookies['DB']
    except:
        return list_db[0]
    else:
        return cached_db


# Cookies Related (Second Half)
@app.callback(
    dash.dependencies.Output('DB-selection-task-sand', 'value'),
    [dash.dependencies.Input('intermediate-value_tasks_sand', 'children')])
def update_db_chan_heat_(db):
    return db


@app.callback(dash.dependencies.Output('date-picker-range-tasks_sand', 'end_date'),
              [dash.dependencies.Input('DB-selection-task-sand', 'value')])
def update_db_(db):
    from_data = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=160)).strftime("%Y-%m-%d")
    data = db_onnections.tasksDB(from_data=from_data, section=db)

    data['event_time'] = pd.to_datetime(data['event_time'])

    return data['event_time'].max()


@app.callback(dash.dependencies.Output('date-picker-range-tasks_sand', 'start_date'),
              [dash.dependencies.Input('DB-selection-task-sand', 'value')])
def update_db_(db):
    from_data = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=160)).strftime("%Y-%m-%d")
    data = db_onnections.tasksDB(from_data=from_data, section=db)

    data['event_time'] = pd.to_datetime(data['event_time'])

    return data['event_time'].max() - timedelta(days=14)


##########################
# Time Related function  #
##########################
@app.callback(
    dash.dependencies.Output('display-time_tasks_sand', 'children'),
    events=[dash.dependencies.Event('interval_tasks_sand', 'interval')])
def display_time():
    return str(datetime.datetime.now())


##########################
# DB related Function    #
##########################
@app.callback(
    dash.dependencies.Output('display-DB-tasks-sand', 'children'),
    [dash.dependencies.Input('DB-selection-task-sand', 'value')])
def update_db(db):
    general_configurations.Current_active_DB = db
    return db


#################################
# Graphics Related Functions    #
#################################
@app.callback(
    dash.dependencies.Output('graphic-Task1_sand', 'figure'),
    [dash.dependencies.Input('date-picker-range-tasks_sand', 'start_date'),
     dash.dependencies.Input('date-picker-range-tasks_sand', 'end_date'),
     dash.dependencies.Input('interval_tasks_sand', 'n_intervals'),
     dash.dependencies.Input('DB-selection-task-sand', 'value')])
def updatetask1(start_date, end_date, n, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    Tasks = db_onnections.tasksDB(from_data=start_date, to_data=end_date, section=db)

    Tasks = Tasks[['args.task_name', 'name']].copy()
    Tasks = Tasks.groupby('args.task_name').count()
    Tasks.columns = ['NumberEvents']
    Tasks['Name'] = Tasks.index

    return {
        'data': [go.Pie(labels=Tasks.Name,
                        values=Tasks.NumberEvents,
                        pull=.1,
                        hole=.1,
                        hoverinfo='label+percent',
                        textinfo='label',
                        showlegend=True,
                        marker=dict(colors=colors,
                                    line=dict(color='#000000', width=1))
                        )
                 ],

        'layout': go.Layout(
            title='Tasks Frequency',
            autosize=True,
            font={'family': 'Glacial Indifference', 'color': colors['text']}
        )}


@app.callback(
    dash.dependencies.Output('graphic-Task3_sand', 'figure'),
    [dash.dependencies.Input('date-picker-range-tasks_sand', 'start_date'),
     dash.dependencies.Input('date-picker-range-tasks_sand', 'end_date'),
     dash.dependencies.Input('interval_tasks_sand', 'n_intervals'),
     dash.dependencies.Input('DB-selection-task-sand', 'value')])
def update_Task3(start_date, end_date, n, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    temp = db_onnections.tasksDB(from_data=start_date, to_data=end_date, section=db)

    TaskNode = temp[['args.task_name']].copy()
    TaskNode = TaskNode.drop_duplicates()
    TaskNode.columns = ['Nome_nodo']

    UserNode = temp[['args.actioned_by_username']].copy()
    UserNode = UserNode.drop_duplicates()
    UserNode.columns = ['Nome_nodo']

    DeviceNode = temp[['args.device_display_name']].copy()
    DeviceNode = DeviceNode.drop_duplicates()
    DeviceNode.columns = ['Nome_nodo']

    nodes = pd.concat([TaskNode, UserNode, DeviceNode], axis=0)
    refrenza = [x for x in range(0, nodes.shape[0])]
    nodesDict = dict(zip(nodes.Nome_nodo, refrenza))

    links = temp[['args.task_name', 'args.actioned_by_username', 'args.device_display_name']].copy()
    links = links[links['args.actioned_by_username'] != 'nan']
    links = links[links['args.actioned_by_username'] != 'enzo_server']
    links = links[links['args.task_name'] != 'nan']

    links = links.groupby(['args.task_name', 'args.device_display_name'], as_index=False).count()
    links['value'] = links['args.actioned_by_username']
    links['source'] = links['args.task_name'].map(nodesDict)
    links['target'] = links['args.device_display_name'].map(nodesDict)
    links = links[['source', 'target', 'value']]

    links2 = temp[['args.task_name', 'args.actioned_by_username', 'name']].copy()
    links2 = links2[links2['args.task_name'] != 'nan']

    links2 = links2[links2['args.actioned_by_username'] != 'nan']
    links2 = links2[links2['args.actioned_by_username'] != 'enzo_server']

    links2 = links2.groupby(['args.task_name', 'args.actioned_by_username'], as_index=False).count()
    links2['value'] = links2['name']
    links2['source'] = links2['args.actioned_by_username'].map(nodesDict)
    links2['target'] = links2['args.task_name'].map(nodesDict)
    links2 = links2[['source', 'target', 'value']]
    links = pd.concat([links, links2], axis=0)

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
                      thickness=20
                      ),
        )],
        'layout': go.Layout(
            title="Users vs Tasks vs Devices",
            autosize=True,
            font={'family': 'Glacial Indifference', 'color': colors['text']}
        )
    }
