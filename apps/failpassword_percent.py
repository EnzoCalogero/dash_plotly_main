# -*- coding: utf-8 -*-
import base64
from app import app

import pandas as pd
from datetime import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import os
import datetime

from apps import elasticsearch_connections, general_configurations

df = elasticsearch_connections.search_UserFailedLoginOdc()

colors = {
    'background': '#111111',
    'text': '#253471',
}

image_filename = os.getcwd() + '/pics//enzo_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#####################################################
# Dual Layouts:                                     #
# The first if no data is available (ELK is down)   #
# The second when data is available                 #
#####################################################
if df.empty:
    layout = html.Div([
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
                children="ODC Failed Passwords",
                style={
                    'textAlign': 'center',
                    'text': colors['text'],
                    'font-family': 'Glacial Indifference',
                    'color': colors['text'],
                    'bgcolor': colors['background']
                }
            )
        ], style={'height': '60px',
                  'width': '70%'
                  }
        ),
        html.Div([
            html.H3(
                children="No Available Data for The ODC Failed Passwords",
                style={
                    'textAlign': 'center',
                    'text': colors['text'],
                    'font-family': 'Glacial Indifference',
                    'color': colors['text'],
                    'bgcolor': colors['background']
                }
            )
        ]),
    ], style={'font-family': 'Glacial Indifference',
              'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto',
              'marginRight': 'auto',
              "width": "160vh",
              'color': colors['text'],
              'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113, 0.4)'
              }
    )

else:
    available_Users = df['user'].unique()
    dataMax = df['@timestamp'].max()
    dataMin = df['@timestamp'].min()

    # Define Layout
    layout = html.Div([
        dcc.Interval(id='interval_failpswd_perc', interval=general_configurations.refresh_interval),
        html.Div([
            html.A(
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                         style={
                             'height': '20px',
                             'float': 'left',
                             'position': 'relative',
                             'bottom': '-10px',
                             'width': '100px',
                         }), href='/', target="_self"),
            html.H2(
                children='Failed Passwords Percentages (ELK source)',
                style={
                    'textAlign': 'center',
                    'font-family': 'Glacial Indifference',
                    'color': colors['text'],
                    'bgcolor': colors['background']
                }),
        ], style={'font-family': 'Glacial Indifference',
                  'height': '60px',
                  'width': '100%'
                  }
        ),

        ##############################################################################################
        html.Div([
            html.Div([
                html.Div(children="Date Range Filter"),
            ], className='two columns'),
            html.Div([
                dcc.DatePickerRange(
                    id='my-date-picker-range_perc',
                    max_date_allowed=dt.now(),
                    initial_visible_month=dataMin,
                    start_date=df['@timestamp'].min(),
                    end_date=dt.now()
                ),
            ], className='five columns'),

            html.Div([
                html.Div(children="User Filter:"),
            ], className='two columns'),
            html.Div([
                dcc.Dropdown(
                    id='Users-FailPswd_perc',
                    options=[{'label': i, 'value': i} for i in available_Users],
                    value=available_Users[0],
                )], className='two columns'),
            html.Div([
                dcc.Link('Main', href='/failpasswords'),
            ], className='one columns'),
        ], className="row"),
        ##################################################################################
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='FailPassword1_perc',
                              config={'modeBarButtonsToRemove': ['sendDataToCloud'],
                                      'displaylogo':False
                                      },
                              style={'width': '100%',
                                     'display': 'inline-block',
                                     'color': colors['text']
                                     }
                              ),
                ], className='four columns'),
                html.Div([
                    dcc.Graph(id='FailPassword2_perc',
                              config={'modeBarButtonsToRemove': ['sendDataToCloud'],
                                      'displaylogo':False
                                      },
                              style={'width': '100%',
                                     'display': 'inline-block',
                                     'color': colors['text']
                                     }
                              ),
                ], className='four columns'),
                html.Div([
                    dcc.Graph(id='FailPassword3_perc',
                              config={'modeBarButtonsToRemove': ['sendDataToCloud'],
                                      'displaylogo': False
                                      },
                              style={'width': '100%',
                                     'display': 'inline-block',
                                     'color': colors['text']
                                     }
                              ),
                ], className='four columns'),
            ], className="row"),
        ], style={'font-family': 'Glacial Indifference',
                  'padding': '0px 10px 15px 10px',
                  'marginLeft': 'auto',
                  'marginRight': 'auto',
                  "width": "157vh",
                  'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)',
                  'color': colors['text']
                  }
        ),
        ######################################################################################

        html.Div(id='display-time_failpswd_perc'),
    ], style={'font-family': 'Glacial Indifference',
              'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto',
              'marginRight': 'auto',
              "width": "160vh",
              'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113, 0.4)'
              }
    )
    # Clousure Layout


# Time Related function
@app.callback(
    dash.dependencies.Output('display-time_failpswd_perc', 'children'),
    events=[dash.dependencies.Event('interval_failpswd_perc', 'interval')])
def display_time_sessions():
    global df
    df = elasticsearch_connections.search_UserFailedLoginOdc()

    return str(datetime.datetime.now())


@app.callback(
    dash.dependencies.Output('FailPassword1_perc', 'figure'),
    [dash.dependencies.Input('my-date-picker-range_perc', 'start_date'),
     dash.dependencies.Input('my-date-picker-range_perc', 'end_date'),
     dash.dependencies.Input('interval_failpswd_perc', 'n_intervals')])
def update_failpswd1(start_date, end_date, n):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)
    Failed = df[['client_address', '@timestamp']].copy()
    Failed = Failed[Failed['@timestamp'] >= start_date]
    Failed = Failed[Failed['@timestamp'] <= end_date]

    Failed = Failed.groupby('client_address').count()
    Failed.columns = ['NumberEvents']
    Failed['Name'] = Failed.index

    return {

        'data': [go.Pie(labels=Failed.Name,
                        values=Failed.NumberEvents,
                        pull=.1,
                        hole=.1,
                        hoverinfo='label+percent',
                        textinfo='label',
                        showlegend=False,
                        marker=dict(colors=colors,
                                    line=dict(color='#000000',
                                              width=1
                                              )
                                    )
                        )
                 ],
        'layout': go.Layout(
            title='IPs From Failed Password Attempts',
            autosize=True,
            font={'family': 'Glacial Indifference',
                  'color': colors['text']
                  }
        )
    }


@app.callback(
    dash.dependencies.Output('FailPassword2_perc', 'figure'),
    [dash.dependencies.Input('my-date-picker-range_perc', 'start_date'),
     dash.dependencies.Input('my-date-picker-range_perc', 'end_date'),
     dash.dependencies.Input('interval_failpswd_perc', 'n_intervals')])
def update_failpswd2(start_date, end_date, n):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)
    Failed = df[['user', '@timestamp']].copy()
    Failed = Failed[Failed['@timestamp'] >= start_date]
    Failed = Failed[Failed['@timestamp'] <= end_date]

    Failed = Failed.groupby('user').count()
    Failed.columns = ['NumberEvents']
    Failed['Name'] = Failed.index

    return {
        'data': [go.Pie(labels=Failed.Name,
                        values=Failed.NumberEvents,
                        pull=.1,
                        hole=.1,
                        hoverinfo='label+percent',
                        textinfo='label',
                        showlegend=False,
                        marker=dict(colors=colors,
                                    line=dict(color='#000000',
                                              width=1
                                              )
                                    )
                        )
                 ],
        'layout': go.Layout(
            title='Users from Failed Password Attempts',
            autosize=True,
            font={'family': 'Glacial Indifference',
                  'color': colors['text']
                  }
        )
    }


@app.callback(
    dash.dependencies.Output('FailPassword3_perc', 'figure'),
    [dash.dependencies.Input('Users-FailPswd_perc', 'value'),
     dash.dependencies.Input('my-date-picker-range_perc', 'start_date'),
     dash.dependencies.Input('my-date-picker-range_perc', 'end_date'),
     dash.dependencies.Input('interval_failpswd_perc', 'n_intervals')])
def update_failpswd3(user, start_date, end_date, n):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    Failed = df[['client_address', 'user', '@timestamp']].copy()
    Failed = Failed[Failed['@timestamp'] >= start_date]
    Failed = Failed[Failed['@timestamp'] <= end_date]

    Failed = Failed[Failed['user'] == user]
    Failed = Failed.groupby('client_address').count()
    Failed.columns = ['NumberEvents', '2']
    Failed['Name'] = Failed.index

    return {
        'data': [go.Pie(labels=Failed.Name,
                        values=Failed.NumberEvents,
                        pull=.1,
                        hole=.1,
                        hoverinfo='label+percent',
                        textinfo='label',
                        showlegend=False,
                        marker=dict(colors=colors,
                                    line=dict(color='#000000',
                                              width=1
                                              )
                                    )
                        )
                 ],
        'layout': go.Layout(
            title='IPs Failed Password For {}'.format(user),
            autosize=True,
            font={'family': 'Glacial Indifference',
                  'color': colors['text']
                  }
        )
    }
