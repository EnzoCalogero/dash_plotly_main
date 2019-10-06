from dash.dependencies import Input, Output
from datetime import datetime as dt
import plotly.figure_factory as ff
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd

import base64
import os


from app import app
from apps import anomality_models

df= anomality_models.checker_anomalitics()#from_data='2018-01-01', border_data= "2018-06-18", end_date= "2018-06-25")

dataMax= df['Time'].max()
dataMin= df['Time'].min()  # It is the border Date

# Dash Variables
colors = {
   'background': '#111111',
   'text': '#253471'
}


image_filename = os.getcwd() + '/pics//enzo_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#############################################################################################
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )
############################################################################################

layout = html.Div([
   html.Div([
    html.A(
       html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={
                    'height': '20px',
                    'float': 'left',
                    'position': 'relative',
                    'bottom': '-10px',
                    'width': '100px',
        }), href= '/', target="_self"),

    html.H1(
        children= "Connections and Anomality ",
        style= {
            'textAlign': 'center',
            'text': colors['text'],
            'font-family':'Glacial Indifference',
            'color': colors['text'],
            'bgcolor': colors['background']
        })
    ],className= 'row'),
 #####################################################################
    html.Div(
        [
            html.Div([
            dcc.DatePickerRange(
                id = 'DateRange',
                start_date= dataMin,
                end_date= dataMax,
                calendar_orientation= 'horizontal',
            ),
                ],className = 'three columns'),
            dcc.Link('3D-Version', href= '/uba3d')
        ], className= "row"),
#############################################################################

    html.Div(
        [
            dcc.Markdown(
                '#### Variables to plot:',
                className= 'two columns'
            ),
            dcc.Dropdown(
                id = 'x-axis',
                options= [{'label': i, 'value': i} for i in
                         ["Time", "Display Name", "Subnet", "Protocol", "Hostname","Probability"]],
                value = 'Time',
                className='two columns'
                ),
            dcc.Dropdown(
                id= 'y-axis',
                options= [{'label': i, 'value': i} for i in
                         ["Time", "Display Name", "Subnet", "Protocol", "Hostname", "Probability"]],
                value= 'Display Name',
                className='two columns'
            )
        ],className= "row",style= {'margin-top': '1'},),
#############################################################################
    html.Div([
         dcc.Graph(id='BAU01',
                   config={'modeBarButtonsToRemove': ['sendDataToCloud'],'displaylogo': False},
                   style= { 'display': 'inline-block','color': colors['text'],  "height": "120vh","width": "100vhS"},
         className="twelve columns")

    ], className= "row"),
##############################################################################
    html.Div([
        dcc.Link('Connections in tab format', href= '/anomalities/'),
    ], className= "row"),

    ],style={'font-family':'Glacial Indifference', 'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "160vh", 'color': colors['text'],
          'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)'})

# Callbacks Definitions
@app.callback(
    dash.dependencies.Output('BAU01', 'figure'),
    [dash.dependencies.Input('x-axis', 'value'),
     dash.dependencies.Input('y-axis', 'value'),
     dash.dependencies.Input("DateRange", 'start_date'),
     dash.dependencies.Input("DateRange", 'end_date')])
def update_BAU01(x,y,start_date,end_date):
    global dataMax
    global dataMin
    dataMin= start_date
    dataMax= end_date
    df = anomality_models.checker_anomalitics()#from_data='2018-01-01', border_data=dataMin,end_date=dataMax)

    data = [go.Scatter(
        x= df[x],
        y= df[y],
        mode= "markers",
        text="<B>" + df['Display Name'] + "</B>, Connected to <B>"+ df["Hostname"] + "</B>, Protocol: <B>"
             + df["Protocol"]+ "</B>, From Subnet: <B>" + df["Subnet"] +"</B>, at: <B>" + df["Time"].astype(str)
             + "</B>,  Probabilty: <B>" + df["Probability"].round(2).astype(str)+ "</B>.",
        marker= dict(
                size= (1 / df.Probability) * 3,
                color= (1 / df.Probability),
                colorscale= 'Reds',
                opacity= 0.5,
                line= dict(
                    width= 2,
                    color= 'rgb(0, 0, 0)',
                )
        ))]
    return{
             "data": data,
             'layout': go.Layout(
                margin=dict(
                    l= 100,
                    r= 100,
                    b= 50,
                    t= 0),
                font= {'family': 'Glacial Indifference', 'color': colors['text']}
                )
              }