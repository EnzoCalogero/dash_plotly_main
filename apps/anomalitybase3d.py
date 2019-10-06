from dash.dependencies import Input, Output
from datetime import datetime as dt
import plotly.figure_factory as ff
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

import base64
import os


from app import app
from apps import anomality_models
############################################################
## To be added the variability for the date               ##
############################################################
df=anomality_models.checker_anomalitics()

df = df.sort_values("Probability")
df = df[["Time", "Display Name", "Subnet", "Protocol", "Hostname","Probability"]]
colors = {
   'background': '#111111',
   'text': '#253471'
}
# Dash Variables

image_filename = os.getcwd() + '/pics//enzo_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


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
        children="Connections and  Anomality ",
        style={
            'textAlign': 'center',
            'text': colors['text'],
            'font-family':'Glacial Indifference',
            'color': colors['text'],
            'bgcolor': colors['background']
        })
    ],className='row'),
 #####################################################################

    html.Div(
        [
            html.Div([
            dcc.DatePickerRange(
                start_date_placeholder_text="Start Period",
                end_date_placeholder_text="End Period",
                calendar_orientation='vertical',
            ),
                ],className='three columns'),
            dcc.Link('2D-Version', href= '/uba'),
        ], className="row"),
#############################################################################

    html.Div(
        [
            dcc.Markdown(
                '#### Variables to plot:',
                className='two columns'
            ),
            dcc.Dropdown(
                id = 'x-axis3d',
                options=[{'label': i, 'value': i} for i in ["Time", "Display Name", "Subnet", "Protocol", "Hostname","Probability"]],
                value = 'Time',
                className='two columns'
                ),
            dcc.Dropdown(
                id='y-axis3d',
                options=[{'label': i, 'value': i} for i in
                         ["Time", "Display Name", "Subnet", "Protocol", "Hostname", "Probability"]],
                value='Display Name',
                className='two columns'
            ),
            dcc.Dropdown(
                id='z-axis3d',
                options=[{'label': i, 'value': i} for i in
                         ["Time", "Display Name", "Subnet", "Protocol", "Hostname", "Probability"]],
                value='Hostname',
                disabled=False,
                className='two columns'
            )
        ],className="row",style={'margin-top': '1'},),

#############################################################################

    html.Div([
         dcc.Graph(id='BAU013d',
                   config={'modeBarButtonsToRemove': ['sendDataToCloud'],'displaylogo': False},
                   style= { 'display': 'inline-block','color': colors['text'],  "height": "110vh","width": "100vhS"},
         className="twelve columns")

    ], className="row"),
##############################################################################

    html.Div([
        dcc.Link('Connections in tab format', href= '/anomalities/'),
    ], className="row"),

    ],style={'font-family':'Glacial Indifference', 'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "160vh", 'color': colors['text'],
          'boxShadow': '0px 0px 5px 5px rgba(37,52,113,0.4)'})


# Definitions for the callbacks

@app.callback(
    dash.dependencies.Output('BAU013d', 'figure'),
    [dash.dependencies.Input('x-axis3d', 'value'),
     dash.dependencies.Input('y-axis3d', 'value'),
     dash.dependencies.Input('z-axis3d', 'value')])
def update_BAU01(x,y,z):
        data=[go.Scatter3d(
            x=df[x],
            y=df[y],
            z=df[z],
            text="<B>" + df['Display Name'] + "</B>, Connected to <B>" + df["Hostname"] + "</B>, Protocol: <B>"
                 + df["Protocol"] + "</B>, From Subnet: <B>" + df["Subnet"] + "</B>, at: <B>" + df["Time"].astype(
                str) + "</B>,  Probabilty: <B>" + df["Probability"].round(2).astype(str) + "</B>.",

            mode='markers',
            marker=dict(
                size=(1 / df.Probability) * 3,
                color=(1 / df.Probability),
                colorscale='Reds',
                opacity=0.5,
                line=dict(
                    width=2,
                    color='rgb(0, 0, 0)'
                )
            ))]
        return{
             "data": data,
             'layout': go.Layout(
                 margin=dict(
                     l=0,
                     r=0,
                     b=0,
                     t=0
                 ),
                font={'family':'Glacial Indifference','color': colors['text']}
          )}

