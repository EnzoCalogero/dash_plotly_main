
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

df=elasticsearch_connections.search_UserFailedLoginOdc()

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
            html.H1(
                children="ODC Failed Passwords",

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
                children="No Available Data for The ODC Failed Passwords",

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
    available_Users=df['user'].unique()
    dataMax=df['@timestamp'].max()
    dataMin=df['@timestamp'].min()


    # Define Layout
    layout = html.Div([
        dcc.Interval(id='interval_failpswd', interval=general_configurations.refresh_interval),
        html.Div([
            html.A(
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={
                    'height': '20px',
                    'float': 'left',
                    'position': 'relative',
                    'bottom': '-10px',
                    'width': '100px',
                }), href='/', target="_self"),
        html.H1(
            children='ODC Failed Passwords',
            style={
                'textAlign': 'center',
                'font-family':'Glacial Indifference',
                'color': colors['text'],
                'bgcolor': colors['background']
            }),
        ],style={'font-family':'Glacial Indifference','height': '60px','width': '100%',}),
        html.Div([
            dcc.Graph(id='FailPassword5', config={'modeBarButtonsToRemove': ['sendDataToCloud'],'displaylogo':False },
                      style={'font-family':'Glacial Indifference','width': '100%', 'display': 'inline-block', 'bgcolor': colors['background'],'color': colors['text']}),
        ],style={'font-family':'Glacial Indifference','padding': '0px 10px 15px 10px',
              'marginLeft': 'auto', 'marginRight': 'auto', "width": "157vh",
              'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)','color': colors['text']}),
           html.Div([
             dcc.Graph(id='FailPassword1',config={'modeBarButtonsToRemove': ['sendDataToCloud'],'displaylogo':False },style={'width': '50%', 'display': 'inline-block','color': colors['text']}),
             dcc.Graph(id='FailPassword2',config={'modeBarButtonsToRemove': ['sendDataToCloud'],'displaylogo':False },style={'width': '50%', 'display': 'inline-block','color': colors['text']}),
           ],style={'font-family':'Glacial Indifference','padding': '0px 10px 15px 10px',
              'marginLeft': 'auto', 'marginRight': 'auto', "width": "157vh",
              'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)','color': colors['text']}),

           html.Div([

               dcc.DatePickerRange(
                   id='my-date-picker-range',
                   min_date_allowed=dataMin,
                   max_date_allowed=dt.now(),
                   initial_visible_month=dataMin,
                   start_date=df['@timestamp'].min(),
                   end_date=dt.now()
               ),], style={'width': '35%','color': colors['text']}
           ),
           html.Div([
               dcc.Dropdown(
                    id='Users-FailPswd',
                    options=[{'label': i, 'value': i} for i in available_Users],
                    value=available_Users[0],
                     ),
           ], style={'width': '25%','color': colors['text']}
                ),
        html.Div([
            dcc.Graph(id='FailPassword3',config={'modeBarButtonsToRemove': ['sendDataToCloud'],'displaylogo': False}),
        ], style={'font-family':'Glacial Indifference','width': '35%', 'display': 'inline-block', 'bgcolor': colors['background'],'color': colors['text']}),
        html.Div([
            html.Div(id='slider-output-container'),
            dcc.Slider(id="slider-FailPswd",

               marks={i: '{}'.format(i) for i in range(15)},
               min=1,
               max=15,
               step=1,
               value=1
                       ),

            dcc.Graph(id='FailPassword4',config={'modeBarButtonsToRemove': ['sendDataToCloud'],'displaylogo':False },style={'width': '100%', 'display': 'inline-block','color': colors['text']}),
        ],style={'font-family':'Glacial Indifference','padding': '0px 10px 15px 10px',
              'marginLeft': 'auto', 'marginRight': 'auto', "width": "157vh",
              'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)','color': colors['text']}),
        html.Div(id='display-time_failpswd'),
        ],     style={'font-family':'Glacial Indifference','padding': '0px 10px 15px 10px',
                 'marginLeft': 'auto', 'marginRight': 'auto', "width": "160vh",
                 'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)'}
     ) # Clousure Layout


# Time Related function
@app.callback(
    dash.dependencies.Output('display-time_failpswd', 'children'),
    events=[dash.dependencies.Event('interval_failpswd', 'interval')])
def display_time_sessions():
    global df
    df = elasticsearch_connections.search_UserFailedLoginOdc()

    return str(datetime.datetime.now())


@app.callback(
    dash.dependencies.Output('FailPassword1', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date'),
     dash.dependencies.Input('interval_failpswd', 'n_intervals')])

def update_failpswd1(start_date,end_date,n):
    start_date=pd.to_datetime(start_date)
    start_date=dt.date(start_date)
    end_date=pd.to_datetime(end_date)
    end_date = dt.date(end_date)
    Failed = df[['client_address', '@timestamp']].copy()
    Failed=Failed[Failed['@timestamp']>= start_date]
    Failed = Failed[Failed['@timestamp'] <= end_date]

    Failed = Failed.groupby('client_address').count()
    Failed.columns = ['NumberEvents']
    Failed['Name'] = Failed.index

    return {

        'data': [go.Pie(labels = Failed.Name,
        values = Failed.NumberEvents,
                        pull=.1,
                        hole=.1
                        )
                  ],
        'layout': go.Layout(
                 title='IPs From Failed Password Attempts',
                 font={'family':'Glacial Indifference','color': colors['text']}
    )}

@app.callback(
    dash.dependencies.Output('FailPassword2', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date'),
     dash.dependencies.Input('interval_failpswd', 'n_intervals')])

def update_failpswd2(start_date,end_date,n):
    start_date=pd.to_datetime(start_date)
    start_date=dt.date(start_date)
    end_date=pd.to_datetime(end_date)
    end_date = dt.date(end_date)
    Failed = df[['user', '@timestamp']].copy()
    Failed=Failed[Failed['@timestamp']>= start_date]
    Failed = Failed[Failed['@timestamp'] <= end_date]

    Failed = Failed.groupby('user').count()
    Failed.columns = ['NumberEvents']
    Failed['Name'] = Failed.index

    return {

        'data': [go.Pie(labels = Failed.Name,
        values = Failed.NumberEvents,
                        pull=.1,
                        hole=.1
                        )
                  ],
        'layout': go.Layout(
                 title='Users from Failed Password Attempts',
                 font={'family':'Glacial Indifference','color': colors['text']}
    )}

@app.callback(
    dash.dependencies.Output('FailPassword3', 'figure'),
    [dash.dependencies.Input('Users-FailPswd', 'value'),
     dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date'),
     dash.dependencies.Input('interval_failpswd', 'n_intervals')])

def update_failpswd3(user,start_date,end_date,n):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    Failed = df[['client_address','user','@timestamp']].copy()
    Failed = Failed[Failed['@timestamp'] >= start_date]
    Failed = Failed[Failed['@timestamp'] <= end_date]

    Failed=Failed[Failed['user']==user]
    Failed = Failed.groupby('client_address').count()
    Failed.columns = ['NumberEvents','2']
    Failed['Name'] = Failed.index

    return {

        'data': [go.Pie(labels = Failed.Name,
        values = Failed.NumberEvents,
                        pull=.1,
                        hole=.1
                        )
                  ],
        'layout': go.Layout(
                 title='IPs Failed Password For {}'.format(user),
                 font={'family':'Glacial Indifference','color': colors['text']}
    )}


@app.callback(
    dash.dependencies.Output('FailPassword4', 'figure'),

    [dash.dependencies.Input('slider-FailPswd', 'value'),
     dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date'),
     dash.dependencies.Input('interval_failpswd', 'n_intervals')])
def update_failpswd4(value,start_date,end_date,n):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)
    Failed = df[['client_address','user','@timestamp']].copy()
    Failed = Failed[Failed['@timestamp'] >= start_date]
    Failed = Failed[Failed['@timestamp'] <= end_date]
    Cross = pd.crosstab(Failed['user'], Failed['client_address'])

    Cross=Cross.loc[~(Cross < value).all(axis=1)]
    Cross = Cross.T[Cross.any()].T

    return {

        'data': [go.Heatmap(
                z=Cross.values.tolist(),
                x=Cross.columns,
                y=Cross.index,
                colorscale=[[0, 'rgb(217,217,217)'],  [1, 'rgb(37,52,113)']],
                colorbar = dict(
                titleside='top',
                tickmode='array',
                tickvals=[ 0, 100],
                ticks='outside'))
                  ],
        'layout': go.Layout(
                 title='Heatmap Failed Passwords Users vs IPs, from {} to {}'.format(start_date,end_date),
                 margin=dict(
                        l=110,
                        r=50,
                        b=100,
                        t=50),
                 showlegend=False,
                 height=550,
                 boxgap=5,
                 font= {'family':'Glacial Indifference','color': colors['text']},
                 xaxis={'showgrid' : True,
                        "tickangle": -45,
                    'linecolor' : 'black'},
                 yaxis={'showgrid': True,
                        "tickangle": -45,
                    'linecolor': 'black'}
    )}

@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('slider-FailPswd', 'value')])
def update_output(value):
    return 'Minimum Number of Failed Passwords to be Displayed {}'.format(value)

@app.callback(
    dash.dependencies.Output('FailPassword5', 'figure'),
    [dash.dependencies.Input('Users-FailPswd', 'value'),
     dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date'),
     dash.dependencies.Input('interval_failpswd', 'n_intervals')])

def update_failpswd5(user,start_date,end_date,n):
    Failed = df[['client_address', '@timestamp']].copy()
    Failed = Failed.groupby('@timestamp').count()
    Failed.columns = ['Failed_Password']
    Failed['Day'] = Failed.index

    return {

        'data': [go.Scatter(name='Failed Password Per Day',
                   x=Failed['Day'], y=Failed['Failed_Password'],
                   connectgaps= False,
                   fill= "tozeroy",
                   line= {
                         "color": "rgb(37, 52, 113)",
                         "shape": "linear",
                         "width": 3 },
                   fillcolor="rgb(217,217,217)")
                  ],
        'layout': go.Layout(
            title="Failed Password Over Time",
            font={'family':'Glacial Indifference','color': colors['text']},
            xaxis={
                "tickangle": -25,
                "type":"category"
            },
            yaxis={"title": "Failed Passwords"}
    )}
