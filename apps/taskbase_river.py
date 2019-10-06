# -*- coding: utf-8 -*-
import flask
import base64
import os

import dash
import dash_core_components as dcc
import dash_html_components as html


from app import app
from apps import db_onnections, general_configurations

colors = {
    'background': '#111111',
    'text': '#253471',
}

list_db = db_onnections.list_dbs()

# Enable the DB selector
if len(list_db) == 1:
    enable_db_selector = True
else:
    enable_db_selector = False

image_filename = os.getcwd() + '/pics//enzo_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

Data = db_onnections.tasksDB(section=general_configurations.Current_active_DB)
# if Data.empty:
#     layout = html.Div([
#         html.Div([
#             html.A(
#                 html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={
#                     'height': '20px',
#                     'float': 'left',
#                     'position': 'relative',
#                     'bottom': '-10px',
#                     'width': '100px',
#                 }), href='/', target="_self"),
#             html.H1(
#                 children="Analytics Menu",
#
#                 style={
#                     'textAlign': 'center',
#                     'text': colors['text'],
#                     'font-family': 'Glacial Indifference',
#                     'color': colors['text'],
#                     'bgcolor': colors['background']
#                 })
#             ], style={
#                 'height': '60px',
#                 'width': '70%'
#                  }
#         ),
#         html.Div([
#             html.H3(
#                 children="No Available Data for the Analytics Tasks ",
#
#                 style={
#                     'textAlign': 'center',
#                     'text': colors['text'],
#                     'font-family': 'Glacial Indifference',
#                     'color': colors['text'],
#                     'bgcolor': colors['background']
#                     }
#                 )
#         ]),
#     ], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
#               'marginLeft': 'auto', 'marginRight': 'auto', "width": "160vh", 'color': colors['text'],
#               'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)'})
#
# else:
# Dash Variables

image_filename = os.getcwd() + '/pics//enzo_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

layout = html.Div([
    html.Div([
        html.Div([
            html.A(
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                         style={
                             'height': '20px',
                             'float': 'left',
                             'position': 'relative',
                             'bottom': '-10px',
                             'width': '100px'}
                         ), href='/', target="_self"),
            html.H2(
                children='Tasks Streamline',
                id="H2_task_river",
                style={
                    'textAlign': 'center',
                    'color': colors['text'],
                    'font-family':'Glacial Indifference',
                    'bgcolor': colors['background']
                }
            ),
        ], className='ten columns'),
        html.Div([
            html.A('Set the Default DB', href='/setdb', target="_blank")
        ], className='two columns'),
    ], className="row"),
    ##########################################################################################################
    html.Div([
        html.Div(
            [
                html.Div(children="Source Database"),
            ], className='two columns'),
        html.Div([
            dcc.Dropdown(
                id="DB-task_river",
                clearable=False,
                options=[{'label': i, 'value': i} for i in list_db],
                disabled=True,
                value=general_configurations.Current_active_DB)
        ], className='three columns'),
        html.Div([
            dcc.Link('Timeseries', href='/tasks_timeseries'),
        ], className='two columns'),
        html.Div([
            dcc.Link('Sankey', href='/tasks_sankey_gl'),
        ], className='two columns'),
        html.Div([
            dcc.Link('Sankey per User', href='/tasks_sankey_user'),
        ], className='two columns'),
    ], className="row"),
    html.Div(id='intermediate-value_tasks_river', style={'display': 'none'}),
    ############################################################################################################
    html.Div([
        html.Iframe(
            src='/themeriver',
            height="600",
            width="100%",
            style={
                'border': '0',
                'align': 'middle'
            }
        )
    ], style={
        'font-family': 'Glacial Indifference',
        'padding': '0px 10px 15px 10px',
        'marginLeft': 'auto',
        'marginRight': 'auto',
        "width": "157vh",
        "boxShadow": "0px 0px 5px 5px rgba(37,52,113,0.4)"
    }
    ),
], style={
    'font-family': 'Glacial Indifference',
    'padding': '0px 10px 15px 10px',
    'marginLeft': 'auto',
    'marginRight': 'auto',
    "width": "160vh",
    "boxShadow": "0px 0px 5px 5px rgba(37,52,113,0.4)"
}
)
# Closure Layout


# Cookies Related (First Half)
@app.callback(
    dash.dependencies.Output('intermediate-value_tasks_river', 'children'),
    [dash.dependencies.Input('H2_task_river', 'children')])
def update_db_chan_heat(_):
    try:
        cached_db = flask.request.cookies['DB']
    except:
        return list_db[0]
    else:
        return cached_db


# Cookies Related (Second Half)
@app.callback(
    dash.dependencies.Output('DB-task_river', 'value'),
    [dash.dependencies.Input('intermediate-value_tasks_river', 'children')])
def update_db_chan_heat_(db):
    return db
