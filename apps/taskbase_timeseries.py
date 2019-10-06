# -*- coding: utf-8 -*-
import base64
import flask
import os
import pandas as pd
from datetime import timedelta
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from app import app
from apps import db_onnections, general_configurations

colors = {
    'background': '#111111',
    'text': '#253471',
}
image_filename = os.getcwd() + '/pics//enzo_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

FROM = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=300)).strftime("%Y-%m-%d")
Data = db_onnections.tasksDB(from_data=FROM, section=general_configurations.Current_active_DB)
list_db = db_onnections.list_dbs()

# Enable the DB selector
if len(list_db) == 1:
    enable_db_selector = True
else:
    enable_db_selector = False

####################################################################################################
# if Data.empty:
#     layout = html.Div([
#         html.Div([
#             html.Div([
#                 html.A(
#                     html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={
#                         'height': '20px',
#                         'float': 'left',
#                         'position': 'relative',
#                         'bottom': '-10px',
#                         'width': '100px',
#                     }), href='/', target="_self"),
#                 html.H2(
#                     children="Tasks Timeseries",
#                     style={
#                         'textAlign': 'center',
#                         'text': colors['text'],
#                         'font-family': 'Glacial Indifference',
#                         'color': colors['text'],
#                         'bgcolor': colors['background']
#                     })
#             ], className='ten columns'),
#             html.Div([
#                 html.A('Set the Default DB', href='/setdb', target="_blank")
#             ], className='two columns'),
#         ], className="row"),
#         ##############################################################################################
#         html.Div([
#             html.Div(
#                 [
#                     html.Div(children="Source Database"),
#                 ], className='two columns'),
#             html.Div([
#                 dcc.Dropdown(
#                     id="DB-task_times",
#                     clearable=False,
#                     options=[{'label': i, 'value': i} for i in list_db],
#                     disabled=enable_db_selector,
#                     value=general_configurations.Current_active_DB)
#             ], className='three columns'),
#             html.Div([
#                 dcc.Link('Sankey', href='/tasks_sankey_gl'),
#             ], className='two columns'),
#             html.Div([
#                 dcc.Link('Sankey per User', href='/tasks_sankey_user'),
#             ], className='two columns'),
#             html.Div([
#                 dcc.Link('Streamline', href='/tasks_river'),
#             ], className='two columns'),
#         ], className="row"),
#         ###########################################################################################
#         html.Div([
#             html.H3(
#                 children="No Available Data for Tasks Analytics",
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
# #######################################################################################################################
# else:
# Dash Variables
available_Task_Users = Data['args.actioned_by_username'].unique()

dataMax = Data['event_time'].max()
dataMin = Data['event_time'].min()

image_filename = os.getcwd() + '/pics//enzo_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

layout = html.Div([
    html.Div([
        html.Div([
            dcc.Interval(id='interval_tasks_times', interval=general_configurations.refresh_interval),
            html.A(
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                         style={
                             'height': '20px',
                             'float': 'left',
                             'position': 'relative',
                             'bottom': '-10px',
                             'width': '100px',
                         }
                         ), href='/', target="_self"),
            html.H2(
                children='Tasks over Time',
                id='H2_tasks_times',
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
    ##############################################################################################
    html.Div([
        html.Div(
            [
                html.Div(children="Source Database"),
            ], className='two columns'),
        html.Div([
            dcc.Dropdown(
                id="DB-task_times",
                clearable=False,
                options=[{'label': i, 'value': i} for i in list_db],
                disabled=enable_db_selector,
                value=general_configurations.Current_active_DB)
        ], className='three columns'),
        html.Div([
            dcc.Link('Sankey', href='/tasks_sankey_gl'),
        ], className='two columns'),
        html.Div([
            dcc.Link('Sankey per User', href='/tasks_sankey_user'),
        ], className='two columns'),
        html.Div([
            dcc.Link('Streamline', href='/tasks_river'),
        ], className='two columns'),
    ], className="row"),
    ###########################################################################################
    html.Div([
        dcc.Graph(id='graphic-Task5_times',
                  config={'modeBarButtonsToRemove': ['sendDataToCloud'],
                          'displaylogo': False
                          },
                  style={'width': '100%',
                         'height': '50vh',
                         'display': 'inline-block'
                         }
                  ),
        dcc.Graph(id='graphic-Task6_times',
                  config={'modeBarButtonsToRemove': ['sendDataToCloud'],
                          'displaylogo': False
                          },
                  style={
                      'width': '100%',
                      'height': '50vh',
                      'display': 'inline-block'
                  }
                  ),
    ], style={'font-family': 'Glacial Indifference',
              'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto',
              'marginRight': 'auto',
              "width": "157vh",
              'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113, 0.4)'
              }
    ),
    html.Div(id='intermediate-value_tasks_times', style={'display': 'none'}),
    html.Div(id='display-DB-tasks-temps'),
    html.Div(id='display-time_tasks_times'),
], style={'font-family': 'Glacial Indifference',
          'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto',
          'marginRight': 'auto',
          "width": "160vh",
          'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113, 0.4)'
          }
)
# Closure Layout


# Cookies Related (First Half)
@app.callback(
    dash.dependencies.Output('intermediate-value_tasks_times', 'children'),
    [dash.dependencies.Input('H2_tasks_times', 'children')])
def update_db_chan_heat(_):
    try:
        cached_db = flask.request.cookies['DB']
    except:
        return list_db[0]
    else:
        return cached_db


# Cookies Related (Second Half)
@app.callback(
    dash.dependencies.Output('DB-task_times', 'value'),
    [dash.dependencies.Input('intermediate-value_tasks_times', 'children')])
def update_db_chan_heat_(db):
    return db


##########################
# Time Related function  #
##########################
@app.callback(
    dash.dependencies.Output('display-time_tasks_times', 'children'),
    events=[dash.dependencies.Event('interval_tasks_times', 'interval')])
def display_time():
    return str(datetime.datetime.now())


##########################
# DB related Function    #
##########################
@app.callback(
    dash.dependencies.Output('display-DB-tasks-temps', 'children'),
    [dash.dependencies.Input('DB-task_times', 'value')])
def update_db(db):
    general_configurations.Current_active_DB = db
    return db


#################################
# Graphics Related Functions    #
#################################
@app.callback(
    dash.dependencies.Output('graphic-Task5_times', 'figure'),
    [dash.dependencies.Input('interval_tasks_times', 'n_intervals'),
     dash.dependencies.Input('DB-task_times', 'value')])
def update_graph5(n, db):
    Templ = db_onnections.tasksDB(from_data=FROM, section=db)

    Templ = Templ.groupby('event_time')[['event_time']].count()

    Templ['Day'] = Templ.index
    Templ['Day'] = pd.to_datetime(Templ['Day'])
    alpha = Templ.resample('W-Mon', on='Day').sum()
    data = [{
        'x': alpha.index,
        'y': alpha[col],
        'name': col,
        'connectgaps': False,
        'fill': "tozeroy",
        "fillcolor": "rgb(217,217,217)",
        'line': {
            "shape": "linear",
            "color": "rgb(37, 52, 113)",
            "width": 2}
    } for col in alpha.columns]

    return {
        'data': data,
        'layout': go.Layout(
            title='Tasks over Time per Week',
            font={'color': colors['text'], 'family': 'Glacial Indifference'},
            xaxis=dict(
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
            yaxis={
                'title': 'Tasks per Week',
                'type': 'linear'
            }
        ),
    }


@app.callback(
    dash.dependencies.Output('graphic-Task6_times', 'figure'),
    [dash.dependencies.Input('interval_tasks_times', 'n_intervals'),
     dash.dependencies.Input('DB-task_times', 'value')])
def update_graph6(n, db):
    Templ = db_onnections.tasksDB(from_data=FROM, section=db)
    Templ['event_time'] = pd.to_datetime(Templ['event_time'])
    alpha = Templ.groupby('args.task_name').resample('W-Mon', on='event_time').count()
    alpha = alpha[['args.task_name']]
    alpha.columns = ["NumberEvents"]
    alpha = alpha.reset_index()

    alpha = alpha.pivot_table(index='event_time', columns='args.task_name', values='NumberEvents', aggfunc="sum")
    alpha = alpha.fillna(0)

    data = [{
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

        'data': data,
        'layout': go.Layout(
            title='Each Tasks over Time per Week',
            font={'color': colors['text'], 'family': 'Glacial Indifference'},
            xaxis=dict(
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
            yaxis={
                'title': 'Tasks per Week',
                'type': 'linear'
            }),
    }
