# -*- coding: utf-8 -*-
import base64
import flask
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import timedelta
import os
import datetime

from app import app
from apps import db_onnections, general_configurations

FROM = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=300)).strftime("%Y-%m-%d")

df = db_onnections.templateDB(from_data=FROM, section=general_configurations.Current_active_DB)
list_db = db_onnections.list_dbs()

# Enable the DB selector
if len(list_db) == 1:
    enable_db_selector = True
else:
    enable_db_selector = False

df['created_at'] = pd.to_datetime(df['created_at'])
dataMax = df['created_at'].max()
dataMin = df['created_at'].min()

colors = {
    'background': '#111111',
    'text': '#253471'
}

# Layout Variables
image_filename = os.getcwd() + '/pics//enzo_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

layout = html.Div([
    dcc.Interval(id='interval_templates_times', interval=general_configurations.refresh_interval),
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
                children="Templates Used over Time",
                id='H2_temp_times',
                style={
                    'textAlign': 'center',
                    'text': colors['text'],
                    'font-family':'Glacial Indifference',
                    'color': colors['text'],
                    'bgcolor': colors['background']
                })
        ], className='ten columns'),
        html.Div([
            html.A('Set the Default DB', href='/setdb', target="_blank")
        ], className='two columns'),
    ], className="row"),
    ##################################################################################
    html.Div([
        html.Div(
            [
                html.Div(children="Source Database"),
            ], className='two columns'),
        html.Div([
            dcc.Dropdown(
                id="DB-template_times",
                clearable=False,
                options=[{'label': i, 'value': i} for i in list_db],
                disabled=enable_db_selector,
                value=general_configurations.Current_active_DB)
        ], className='three columns'),
        html.Div([
            dcc.Link('Percentages', href='/templates_percentage'),
        ], className='two columns'),
        html.Div([
            dcc.Link('Sunburst', href='/templates_sunburst'),
        ], className='two columns'),
    ], className="row"),
    html.Div([
        html.Div([
            dcc.RadioItems(
                id='yaxis-column_times',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='templates-graphic4_times',
                  config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo': False},
                  style={'width': '100%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='templates-graphic5_times',
                  config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo': False},
                  style={'width': '100%', 'height': '50vh', 'display': 'inline-block'}),
    ], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto', 'marginRight': 'auto', "width": "157vh",
              'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113, 0.4)'}),
    html.Div(id='intermediate-value_templates_times', style={'display': 'none'}),
    html.Div(id='display-time_templates_times'),
    html.Div(id='display-DB-template_times'),
], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "160vh",
          'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113, 0.4)'}
)
# Clousure Layout


# Cookies Related (First Half)
@app.callback(
    dash.dependencies.Output('intermediate-value_templates_times', 'children'),
    [dash.dependencies.Input('H2_temp_times', 'children')])
def update_db_chan_heat(_):
    try:
        cached_db = flask.request.cookies['DB']
    except:
        return list_db[0]
    else:
        return cached_db


# Cookies Related (Second Half)
@app.callback(
    dash.dependencies.Output('DB-template_times', 'value'),
    [dash.dependencies.Input('intermediate-value_templates_times', 'children')])
def update_db_chan_heat_(db):
    return db


##########################
# Time Related function  #
##########################
@app.callback(
    dash.dependencies.Output('display-time_templates_times', 'children'),
    events=[dash.dependencies.Event('interval_templates_times', 'interval')])
def display_time():
    return str(datetime.datetime.now())


# DB related Function
@app.callback(
    dash.dependencies.Output('display-DB-template_times', 'children'),
    [dash.dependencies.Input('DB-template_times', 'value')])
def update_db(db):
    general_configurations.Current_active_DB = db
    return db


#################################
# Graphics Related Functions    #
#################################
@app.callback(
    dash.dependencies.Output('templates-graphic4_times', 'figure'),
    [dash.dependencies.Input('yaxis-column_times', 'value'),
     dash.dependencies.Input('interval_templates_times', 'n_intervals'),
     dash.dependencies.Input('DB-template_times', 'value')])
def update_graph4(yaxis_type, n, db):

    Templ = db_onnections.templateDB(from_data=FROM, section=db)
    Templ['created_at'] = pd.to_datetime(Templ['created_at'])
    Templ['created_at'] = Templ['created_at'].dt.date

    alpha = Templ.pivot_table(index='created_at', columns='dispalynametemp', values='vendor', aggfunc="count")
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
            title='Templates Used per Days',
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
                'title': 'Templates Usage',
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            }),
    }


@app.callback(
    dash.dependencies.Output('templates-graphic5_times', 'figure'),
    [dash.dependencies.Input('yaxis-column_times', 'value'),
     dash.dependencies.Input('interval_templates_times', 'n_intervals'),
     dash.dependencies.Input('DB-template_times', 'value')])
def update_graph5(yaxis_type, n, db):
    templ = db_onnections.templateDB(from_data=FROM, section=db)
    templ['created_at'] = pd.to_datetime(templ['created_at'])
    alpha = templ.groupby('dispalynametemp').resample('W-Mon', on='created_at').count()
    alpha = alpha[['vendor']]
    alpha.columns = ["NumberEvents"]
    alpha = alpha.reset_index()

    alpha = alpha.pivot_table(index='created_at', columns='dispalynametemp', values='NumberEvents', aggfunc="sum")
    alpha = alpha.fillna(0)

    data = [{
        'x': alpha.index,
        'y': alpha[col],
        'name': col,
        'connectgaps': False,
        'fill': "tozeroy",
        'opacity': 0.1,
        'line': {
            "shape": "linear",
            "width": 2}
    } for col in alpha.columns]

    return {

        'data': data,
        'layout': go.Layout(
            title='Templates used per Weeks',
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
                'title': 'Templates Usage',
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
        )
    }
