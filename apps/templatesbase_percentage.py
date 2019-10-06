# -*- coding: utf-8 -*-
import base64
import flask
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import timedelta
from datetime import datetime as dt
import os
import datetime

from app import app
from apps import db_onnections, general_configurations
FROM = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=45)).strftime("%Y-%m-%d")

df = db_onnections.templateDB(from_data=FROM, section=general_configurations.Current_active_DB)
list_db = db_onnections.list_dbs()

# Enable the DB selector
if len(list_db) == 1:
    enable_db_selector = True
else:
    enable_db_selector = False

df['created_at']=pd.to_datetime(df['created_at'])
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
    html.Div([
        dcc.Interval(id='interval_templates_perc', interval=general_configurations.refresh_interval),
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
                children="Templates Percentages",
                id='H2_temp_perc',
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
    ########################################################################################
    html.Div([
        html.Div(
            [
                html.Div(children="Source Database"),
            ], className='two columns'),
        html.Div([
            dcc.Dropdown(
                id="DB-template_perc",
                clearable=False,
                options=[{'label': i, 'value': i} for i in list_db],
                disabled=enable_db_selector,
                value=general_configurations.Current_active_DB)
        ], className='three columns'),
        html.Div([
            dcc.Link('Timeseries', href='/templates_timeseries'),
        ], className='two columns'),
        html.Div([
            dcc.Link('Sunburst', href='/templates_sunburst'),
        ], className='two columns'),
    ], className="row"),
    ########################################################################################
    html.Div([
        html.Div([
            html.Div(children="Date Range Filter"),
        ], className='two columns'),
        html.Div([
            dcc.DatePickerRange(
                id='date-picker-range-templ_perc',
                start_date=dataMin,
                end_date=dataMax),
        ], className='five columns'),
    ], className="row"),
    ############################################################################################
    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id='templates-graphic1_perc',
                          config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo': False},
                          style={'width': '100%', 'display': 'inline-block'}),
            ], className='four columns'),
            html.Div([
                dcc.Graph(id='templates-graphic2_perc',
                          config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo': False},
                          style={'width': '100%', 'display': 'inline-block'}),
            ], className='four columns'),
            html.Div([
                dcc.Graph(id='templates-graphic3_perc',
                          config={'modeBarButtonsToRemove': ['sendDataToCloud'], 'displaylogo': False},
                          style={'width': '100%', 'display': 'inline-block'}),
            ], className='four columns'),
        ], className="row"),
    ], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto', 'marginRight': 'auto', "width": "157vh",
              'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113, 0.4)'}),
    html.Div(id='intermediate-value_templates_perce', style={'display': 'none'}),
    html.Div(id='display-DB-template_perc'),
    html.Div(id='display-time_templates_perce'),
], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "160vh",
          'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113, 0.4)'}
)
# Closure Layout


# Cookies Related (First Half)
@app.callback(
    dash.dependencies.Output('intermediate-value_templates_perce', 'children'),
    [dash.dependencies.Input('H2_temp_perc', 'children')])
def update_db_chan_heat(_):
    try:
        cached_db = flask.request.cookies['DB']
    except:
        return list_db[0]
    else:
        return cached_db


# Cookies Related (Second Half)
@app.callback(
    dash.dependencies.Output('DB-template_perc', 'value'),
    [dash.dependencies.Input('intermediate-value_templates_perce', 'children')])
def update_db_chan_heat_(db):
    return db


@app.callback(dash.dependencies.Output('date-picker-range-templ_perc', 'end_date'),
              [dash.dependencies.Input('DB-template_perc', 'value')])
def update_db_(db):
    FROM = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=140)).strftime("%Y-%m-%d")
    df = db_onnections.templateDB(from_data=FROM, section=db)

    df['created_at'] = pd.to_datetime(df['created_at'])

    return df['created_at'].max()


@app.callback(dash.dependencies.Output('date-picker-range-templ_perc', 'start_date'),
              [dash.dependencies.Input('DB-template_perc', 'value')])
def update_db_(db):
    FROM = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=140)).strftime("%Y-%m-%d")
    df = db_onnections.templateDB(from_data=FROM, section=db)

    df['created_at'] = pd.to_datetime(df['created_at'])
    datamax = df['created_at'].max()

    return datamax - timedelta(days=15)


##########################
# Time Related function  #
##########################
@app.callback(
    dash.dependencies.Output('display-time_templates_perc', 'children'),
    events=[dash.dependencies.Event('interval_templates_perc', 'interval')])
def display_time():
    return str(datetime.datetime.now())


# DB related Function
@app.callback(
    dash.dependencies.Output('display-DB-template_perc', 'children'),
    [dash.dependencies.Input('DB-template_perc', 'value')])
def update_db(db):
    # print(general_configurations.Current_active_DB)
    general_configurations.Current_active_DB = db
    # print(general_configurations.Current_active_DB)
    return db


#################################
# Graphics Related Functions    #
#################################
@app.callback(
    dash.dependencies.Output('templates-graphic1_perc', 'figure'),
    [dash.dependencies.Input('date-picker-range-templ_perc', 'start_date'),
     dash.dependencies.Input('date-picker-range-templ_perc', 'end_date'),
     dash.dependencies.Input('interval_templates_perc', 'n_intervals'),
     dash.dependencies.Input('DB-template_perc', 'value')])
def update_graph1(start_date, end_date, n, db):

    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    Templ = db_onnections.templateDB(from_data=start_date, to_data=end_date, section=db)

    Templ = Templ[['dispalynametemp', 'protocol']].copy()
    Templ = Templ.groupby('dispalynametemp').count()
    Templ.columns = ['NumberEvents']
    Templ['Template'] = Templ.index
    return {
        'data': [go.Pie(
            labels=Templ.Template,
            values=Templ.NumberEvents,
            pull=.1,
            hole=.1,
            hoverinfo='label+percent',
            textinfo='label',
            showlegend=False,
            marker=dict(colors=colors,
                        line=dict(color='#000000', width=1))
        )
        ],
        'layout': go.Layout(
            title='Templates',
            autosize=True,

            font={'color': colors['text'], 'family': 'Glacial Indifference'}
        )}


@app.callback(
    dash.dependencies.Output('templates-graphic2_perc', 'figure'),
    [dash.dependencies.Input('date-picker-range-templ_perc', 'start_date'),
     dash.dependencies.Input('date-picker-range-templ_perc', 'end_date'),
     dash.dependencies.Input('interval_templates_perc', 'n_intervals'),
     dash.dependencies.Input('DB-template_perc', 'value')])
def update_graph2(start_date, end_date, n, db):

    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    Templ = db_onnections.templateDB(from_data=start_date, to_data=end_date, section=db)

    Templ = Templ[['vendor', 'protocol']].copy()
    Templ = Templ.groupby('vendor').count()
    Templ.columns = ['NumberEvents']
    Templ['Vendor'] = Templ.index
    return {

        'data': [go.Pie(
            labels=Templ.Vendor,
            values=Templ.NumberEvents,
            pull=.1,
            hole=.1,
            hoverinfo='label+percent',
            textinfo='label',
            showlegend=False,
            marker=dict(colors=colors,
                        line=dict(color='#000000',
                                  width=1))
        )
        ],
        'layout': go.Layout(
            title='Vendor',
            autosize=True,
            font={
                'color': colors['text'],
                'family': 'Glacial Indifference'
            }
        )
    }


@app.callback(
    dash.dependencies.Output('templates-graphic3_perc', 'figure'),
    [dash.dependencies.Input('date-picker-range-templ_perc', 'start_date'),
     dash.dependencies.Input('date-picker-range-templ_perc', 'end_date'),
     dash.dependencies.Input('interval_templates_perc', 'n_intervals'),
     dash.dependencies.Input('DB-template_perc', 'value')])
def update_graph3(start_date, end_date, n, db):
    start_date = pd.to_datetime(start_date)
    start_date = dt.date(start_date)
    end_date = pd.to_datetime(end_date)
    end_date = dt.date(end_date)

    Templ = db_onnections.templateDB(from_data=start_date, to_data=end_date, section=db)

    Templ = Templ[['typesdisplayname', 'protocol']].copy()
    Templ = Templ.groupby('typesdisplayname').count()
    Templ.columns = ['NumberEvents']
    Templ['type'] = Templ.index
    return {
        'data': [go.Pie(
            labels=Templ.type,
            values=Templ.NumberEvents,
            pull=.1,
            hole=.1,
            hoverinfo='label+percent',
            textinfo='label',
            showlegend=False,
            marker=dict(colors=colors,
                        line=dict(color='#000000',
                                  width=1))
        )],
        'layout': go.Layout(
            title='Templates Types',
            autosize=True,
            font={
                'color': colors['text'],
                'family': 'Glacial Indifference'
            }
        )
    }
