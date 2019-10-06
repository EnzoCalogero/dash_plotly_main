# -*- coding: utf-8 -*-
from flask import render_template, make_response, request
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from app import app
server = app.server


############################################
#   Initialize the Active DB               #
############################################
from apps import db_onnections, general_configurations, neo4j_connections

list_db = db_onnections.list_dbs()

#  Initial value for the Active DB.
general_configurations.Current_active_DB = list_db[0]


from apps import home, networkbase, graph_base
#from apps import channelsbase_percentage, channelsbase_sankey, channelsbase_heatmap # , channelsbase_heatmap
from apps import sessionbase_global, sessionbase_peruser, sessionbase_distribution
from apps import sparklines_builder, sunburst, revealed_pswd, long_running, themeriver

from apps import templatesbase_percentage, templatesbase_timeseries, templatesbase_sunburst
from apps import taskbase_timeseries, taskbase_sankey_gl, taskbase_sankey_user, taskbase_river
from apps import failpassword_main, failpassword_percent
#######################################################################
#from apps import anomality_models, anomalitybase, anomalitybase3d
######################################################################
from apps import connections_base
from apps import channelsbase_percentage, channelsbase_sankey, channelsbase_heatmap_neo # channelsbase_heatmap
    #, channelsbase_heatmap_neo # ,
############################################
# Direct Exposition to the Flask  Library  #
#    for cookies integration               #
############################################


@server.route('/setdb')
def defaultdb():
    list_db = pd.DataFrame(db_onnections.list_dbs())
    pd.set_option('display.max_colwidth', -1)
    list_db.columns = ['DB']

    begin = '<form action = "/setcookie" method = "POST"><input type="hidden" name = "nm" value="'
    end = '" readonly> <input type = "submit" value = "Select DB" ></form>'

    list_db['Build'] = begin + list_db['DB'] + end
    list_db.set_index(['DB'], inplace=True)
    list_db.columns = ['Build']
    list_db.index.name = None

    return render_template('setdb.html', tables=[list_db.to_html(classes='Databases', escape=False)], titles=['DB'])


@server.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        db = request.form['nm']
        print(db)
    resp = make_response(render_template('readcookie.html'))
    resp.set_cookie('DB', db)

    return resp


# This function is only for debug purpose
@server.route('/getcookie')
def getcookie():
    name = request.cookies.get('DB')
    if name is None:
        return '<h1> no db selected </h1>'

    print("The Winner is  >{}<".format(name))
    return '<h1>Focus DB is ' + name + '</h1>'

############################################
# Direct Exposition to the Flask  Library  #
# for Javascript Library integration       #
############################################


@server.route('/sparkline')
def sparkline():
    if request.cookies.get('DB'):
        db = request.cookies.get('DB')
    else:
        list_db = db_onnections.list_dbs()
        db = list_db[0]

    # DB based
    task_events, task_max = sparklines_builder.tasksparkline(from_data='2017-01-01', db=db)
    session_events, session_max, channel_events, channel_max \
        = sparklines_builder.session_chanelsparkline(from_data='2017-01-01', db=db)
    # ELK based
    failed_events, failed_max = sparklines_builder.failpsw_sparkline()
    revealed_events, revealed_max = sparklines_builder.Reveal_psw_sparkline()
    longrun_events, longrun_max = sparklines_builder.long_running_sparkline()

    return render_template('sparkline.html',
                           task_ts=task_events,
                           session_ts=session_events,
                           channel_ts=channel_events,
                           failed_ts=failed_events,
                           revealed_ts=revealed_events,
                           longrun_ts=longrun_events)


@server.route('/sunbursttemplates')
def sunbursttemplates():
    if request.cookies.get('DB'):
        db = request.cookies.get('DB')
    else:
        list_db = db_onnections.list_dbs()
        db = list_db[0]

    data = sunburst.templates_sunburts(db=db)
    return render_template('sunburstTemplates.html', data=data)


@server.route('/themeriver')
def themerivertemplate():
    if request.cookies.get('DB'):
        db = request.cookies.get('DB')
    else:
        list_db = db_onnections.list_dbs()
        db = list_db[0]

    tstasks = themeriver.themeriverbuildertasks(db=db)
    return render_template('themerivertemplate.html',
                           tstasks=tstasks,
                           title_='Streamline Tasks Over Time (last 3 Weeks)')


@server.route('/themeriverusers')
def themerivertemplateusers():
    tstasks = themeriver.themeriverbuilderusers()
    return render_template('themerivertemplate.html',
                           tstasks=tstasks,
                           title_='Streamline Users Over Time'
                           )


@server.route('/anomalities/')
def anomalities_():
    data = anomality_models.checker_anomalitics()
    data = data.sort_values("Probability")
    data = data[["Time", "Display Name", "Subnet", "Protocol", "Hostname", "Probability"]]
    return render_template('anomality.html',
                           tables=[data.to_html(classes='Databases',
                                                escape=False)],
                           titles=['Probability']
                           )


# Dash Variables
colors = {
    'background': '#111111',
    'text': '#253471'
}

#######################################################
###   Starting the Layout                          ####
#######################################################
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div(id='my-div'),
], style={
    'font-family': 'Glacial Indifference',
    'width': '12%',
    'display': 'inline-block',
    'color': colors['text']
}
)  # End Layout


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/channel_sankey':
        return channelsbase_sankey.layout
    elif pathname == '/channel_heatmap':
        return channelsbase_heatmap_neo.layout
    elif pathname == '/channel_percent':
        return channelsbase_percentage.layout
    elif pathname == '/connections':
        return connections_base.layout
    elif pathname == '/network':
        return networkbase.layout
    elif pathname == '/failpasswords':
        return failpassword_main.layout
    elif pathname == '/failpasswords_perc':
        return failpassword_percent.layout
    elif pathname == '/session_distribution':
        return sessionbase_distribution.layout
    elif pathname == '/session_user':
        return sessionbase_peruser.layout
    elif pathname == '/session_global':
        return sessionbase_global.layout
    elif pathname == '/templates_timeseries':
        return templatesbase_timeseries.layout
    elif pathname == '/templates_sunburst':
        return templatesbase_sunburst.layout
    elif pathname == '/templates_percentage':
        return templatesbase_percentage.layout
    elif pathname == '/tasks_river':
        return taskbase_river.layout
    elif pathname == '/tasks_sankey_user':
        return taskbase_sankey_user.layout
    elif pathname == '/tasks_sankey_gl':
        return taskbase_sankey_gl.layout
    elif pathname == '/tasks_timeseries':
        return taskbase_timeseries.layout
    elif pathname == '/revealed':
        return revealed_pswd.layout
    elif pathname == '/longrun':
        return long_running.layout
    #    elif pathname == '/uba':
    #       return anomalitybase.layout
    #    elif pathname == '/uba3d':
    #       return anomalitybase3d.layout
    elif pathname == '/graphcharts':
        return graph_base.layout
    elif pathname == '/anomalities/':
        anomalities_()
    else:
        return '404'


if __name__ == '__main__':
    #import time
   # print("Before Sleeping")
#    time.sleep(30)
    #print("After Sleeping")
    app.run_server(debug=True, host='0.0.0.0', port=5000)
