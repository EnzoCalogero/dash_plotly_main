# -*- coding: utf-8 -*-
import base64

import dash_html_components as html
import os

colors = {
    'background': '#111111',
    'text': '#253471',
}

image_filename = os.getcwd() + '/pics//enzo_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Define Layout
layout = html.Div([
    html.A(
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={
            'height': '20px',
            'float': 'left',
            'position': 'relative',
            'bottom': '-10px',
            'width': '100px',
        }), href='/', target="_self"),
    html.H1(
        children='Graph Chart Users vs Devices',
        style={
            'textAlign': 'center',
            'font-family': 'Glacial Indifference',
            'color': colors['text'],
            'bgcolor': colors['background']
        }),
    html.Iframe(src='/graphs/', height="1580px", width="100%", style={'border': '0', 'float': 'center'}),
], style={'font-family': 'Glacial Indifference', 'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "160vh", 'color': colors['text'],
          'boxShadow': '0px 0px 5px 5px rgba(37, 52, 113, 0.4)'}
)
