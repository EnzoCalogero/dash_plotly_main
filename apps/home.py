# -*- coding: utf-8 -*-
import flask
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import base64
import os

from app import app
colors = {
    'background': '#111111',
    'text': '#253471'}
# Dash Variables

image_filename = os.getcwd() + '/pics//enzo_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

layout = html.Div([
    html.Div([
        html.Div([
            html.A(
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={
                    'height': '20px',
                    'float': 'left',
                    'position': 'relative',
                    'bottom': '-10px',
                    'width': '100px'}
                         ), href='/', target="_self"),
            html.H2(
                children="Dashboard Menu",
                id="h2_come",
                style={
                    'textAlign': 'center',
                    'text': colors['text'],
                    'font-family':'Glacial Indifference',
                    'color': colors['text'],
                    'bgcolor': colors['background']}
            )
        ], className='ten columns'),
        html.Div([
            html.A('Set the Focus DB', href='/setdb', target="_blank")
        ], className='two columns'),
    ], className="row"),
    ###########################################################################################################
    html.Div([
        html.P(id='intermediate-value_home', style={'float': 'right'}),
    ], className="row"),
    html.Div([
        html.P(dcc.Link('Go to Sessions Analytics', href='/session_global'), ),
        html.Iframe(src='/sparkline', height="450", width="35%", style={'border': '3', 'float': 'right'}),
        html.P(dcc.Link('Go to Channels Analytics', href='/channel_heatmap')),
        html.P(dcc.Link('Go to Connections Analytics', href='/connections')),
        html.P(dcc.Link('Go to Network Analytics', href='/network')),
        html.P(dcc.Link('Go to Templates Analytics', href='/templates_timeseries')),
        html.P(dcc.Link('Go to Tasks Analytics', href='/tasks_timeseries')),
        html.P(dcc.Link('Go to Failed Password Analytics (ELK)', href='/failpasswords')),
        html.P(dcc.Link('Go to Revealed Password Analytics (ELK)', href='/revealed')),
        html.P(dcc.Link('Go to Long Running Sessions Analytics (ELK)', href='/longrun')),
        #html.P(dcc.Link('Go to User Behavior Analytics', href='/uba')),
        html.P(html.A("Go to Graphs Charts", href='/graphcharts', target="_blank")),
        html.A("Neo4j Console", href='http://localhost:7474/browser/', target="_blank"),
    ]),
], style={
    'font-family': 'Glacial Indifference',
    'padding': '0px 10px 15px 10px',
    'marginLeft': 'auto',
    'marginRight': 'auto',
    'width': '160vh',
    'color': colors['text'],
    'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)'}
)


@app.callback(Output('intermediate-value_home', 'children'),
              [Input('h2_come', 'children')])
def cookies_db_(_):
    if flask.request.cookies['DB']:
        cached_db = flask.request.cookies['DB']
        print(flask.request.cookies['DB'])
        return "Fucus DB:  [ " + cached_db + " ]"
    else:
        return "NO Focus DB Selected"