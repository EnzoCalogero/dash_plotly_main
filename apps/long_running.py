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
df = elasticsearch_connections.search_long_run()

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
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={
                    'height': '20px',
                    'float': 'left',
                    'position': 'relative',
                    'bottom': '-10px',
                    'width': '100px',
                }), href='/', target="_self"),
            html.H2(
                children="Long Running Sessions (ELK source)",
                style={
                    'textAlign': 'center',
                    'text': colors['text'],
                    'font-family': 'Glacial Indifference',
                    'color': colors['text'],
                    'bgcolor': colors['background']
                })
        ], style={'height': '60px', 'width': '70%', }),
        html.Div([
            html.H3(
                children="No Available Data For The Long Running Sessions",

                style={
                    'textAlign': 'center',
                    'text': colors['text'],
                    'font-family': 'Glacial Indifference',
                    'color': colors['text'],
                    'bgcolor': colors['background']
                })
        ]),
    ], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto', 'marginRight': 'auto', "width": "160vh", 'color': colors['text'],
              'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)'})

else:
    available_Users = df['user'].unique()
    dataMax = df['@timestamp'].max()
    dataMin = df['@timestamp'].min()

    # Define Layout
    layout = html.Div([
        dcc.Interval(id='interval_longrun', interval=general_configurations.refresh_interval),
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
                         ), href='/', target="_self"),
            html.H2(
                children='Long Running Sessions (ELK source)',
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

        html.Div([
            dcc.Graph(id='longrun1',
                      config={'modeBarButtonsToRemove': ['sendDataToCloud'],
                              'displaylogo': False
                              },
                      style={'font-family': 'Glacial Indifference',
                             'width': '100%',
                             'height': '50vh',
                             'display': 'inline-block',
                             'bgcolor': colors['background'],
                             'color': colors['text']
                             }
                      ),
        ], style={'font-family': 'Glacial Indifference',
                  'padding': '0px 10px 15px 10px',
                  'marginLeft': 'auto',
                  'marginRight': 'auto',
                  "width": "157vh",
                  'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113, 0.4)',
                  'color': colors['text']
                  }
        ),
        #################################################################################################
        html.Div([
            html.Div([
                html.Div(children="Date Range Filter"),
            ], className='two columns'),
            html.Div([
                dcc.DatePickerRange(
                    id='date-picker-range_longrun',
                    min_date_allowed=dataMin,
                    max_date_allowed=dt.now(),
                    initial_visible_month=dataMin,
                    start_date=df['@timestamp'].min(),
                    end_date=dt.now()
                )], className='five columns'),
        ], className="row"),
        #################################################################################################
        html.Div([
            html.Div(id='slider-output-longrunning'),
            dcc.Slider(id="slider-longrunning",
                       marks={i: '{}'.format(i) for i in range(15)},
                       min=1,
                       max=15,
                       step=1,
                       value=1
                       ),
            dcc.Graph(id='longrun2',
                      config={'modeBarButtonsToRemove': ['sendDataToCloud'],
                              'displaylogo': False
                              },
                      style={'width': '100%',
                             'display': 'inline-block',
                             'color': colors['text']
                             }
                      ),
        ], style={'font-family': 'Glacial Indifference',
                  'padding': '0px 10px 15px 10px',
                  'marginLeft': 'auto',
                  'marginRight': 'auto',
                  "width": "157vh",
                  'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113, 0.4)',
                  'color': colors['text']
                  }
        ),
        html.Div(id='display-time_longrun'),
    ], style={'font-family': 'Glacial Indifference',
              'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto',
              'marginRight': 'auto',
              "width": "160vh",
              'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113, 0.4)'
              }
    )  # Clousure Layout


# Time Related function
@app.callback(
    dash.dependencies.Output('display-time_longrun', 'children'),
    events=[dash.dependencies.Event('interval_longrun', 'interval')])
def display_time_sessions():
    global df
    df = elasticsearch_connections.search_long_run()
    return str(datetime.datetime.now())


@app.callback(
    dash.dependencies.Output('slider-output-longrunning', 'children'),
    [dash.dependencies.Input('slider-longrunning', 'value')])
def update_output(value):
    return 'Minimum Number of Long Running Sessions to be Displayed {}'.format(value)


@app.callback(
    dash.dependencies.Output('longrun1', 'figure'),
    [dash.dependencies.Input('date-picker-range_longrun', 'start_date'),
     dash.dependencies.Input('interval_longrun', 'n_intervals')])
def update_failpswd5(start, n):

    reveal = df[['user', '@timestamp']].copy()
    reveal = reveal.groupby('@timestamp').count()
    reveal.columns = ['Revealed_Password']
    reveal['Day'] = reveal.index

    return {
        'data': [go.Scatter(
            name='Long Connections per Day',
            x=reveal['Day'],
            y=reveal['Revealed_Password'],
            connectgaps=False,
            fill="tozeroy",
            line={
                "color": "rgb(37, 52, 113)",
                "shape": "linear",
                "width": 3
            },
            fillcolor="rgb(217,217,217)")
        ],
        'layout': go.Layout(
            title="Long Running Connections Over Time",
            font={'family': 'Glacial Indifference',
                  'color': colors['text']
                  },
            xaxis={
                "tickangle": -25,
                "type": "category"
            },
            yaxis={"title": "Long Term Connections"}
        )
    }


@app.callback(
    dash.dependencies.Output('longrun2', 'figure'),
    [dash.dependencies.Input('slider-longrunning', 'value'),
     dash.dependencies.Input('date-picker-range_longrun', 'start_date'),
     dash.dependencies.Input('date-picker-range_longrun', 'end_date'),
     dash.dependencies.Input('interval_longrun', 'n_intervals')])
def update_failpswd4(value, start_date, end_date, n):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    reveal = df[['device', 'user', '@timestamp']].copy()
    reveal = reveal[reveal['@timestamp'] >= start_date]
    reveal = reveal[reveal['@timestamp'] <= end_date]
    Cross = pd.crosstab(reveal['user'], reveal['device'])
    Cross = Cross.loc[~(Cross < value).all(axis=1)]
    Cross = Cross.T[Cross.any()].T

    return {
        'data': [go.Heatmap(
            z=Cross.values.tolist(),
            x=Cross.columns,
            y=Cross.index,
            text=Cross.values.tolist(),

            hoverinfo='text',
            showscale=False,
            colorscale=[[0, 'rgb(217,217,217)'], [1, 'rgb(37,52,113)']],
            colorbar=dict(
                titleside='top',
                tickmode='array',
                tickvals=[0, 50, 100],
                ticks='outside')
        )
        ],
        'layout': go.Layout(
            title='Long Term Connections Users vs Devices, From {} To {}'.format(start_date, end_date),
            margin=dict(
                l=110,
                r=50,
                b=100,
                t=50),
            showlegend=False,
            height=550,
            boxgap=5,
            font={'family': 'Glacial Indifference', 'color': colors['text']},
            xaxis={'showgrid': True,
                   "tickangle": -25,
                   'linecolor': 'black'
                   },
            yaxis={'showgrid': True,
                   "tickangle": -25,
                   'linecolor': 'black'
                   }
        )
    }
