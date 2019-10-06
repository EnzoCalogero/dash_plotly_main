# -*- coding: utf-8 -*-
import dash

app = dash.Dash("enzus", static_folder='static')
app.title = 'Analytics'
app.scripts.config.serve_locally = True
app.config.supress_callback_exceptions = True

#################################
# Refreshing Constant for       #
# the Dashboards                #
#################################
app.refresh_interval = 5*60*1000  # 5 minutes

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})
