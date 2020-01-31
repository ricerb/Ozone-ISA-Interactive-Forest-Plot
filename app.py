from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

import forestplot
import animaltox


##Initialize app

app = dash.Dash(__name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"])
server = app.server
app.config.suppress_callback_exceptions = True
forestplot.startup(app)
animaltox.startup(app)
##Create app layout

app.layout = html.Div([
    
    html.H3('Ozone ISA Interactive Plot Prototype'),
    
    dcc.Tabs(id='tabs', value='forestplot', children=[
        dcc.Tab(label='Forest Plot', value ='forestplot'),
        dcc.Tab(label='Animal Tox Plot', value ='toxplot')
    ]),
    html.Div(id='tabcontent')
])


##Put callback options in here - 2 separate callbacks for each plot/tab?

@app.callback(Output(component_id = 'tabcontent', component_property = 'children'),
            [Input(component_id = 'tabs', component_property = 'value')])

def render_content(tab):
    if tab == 'forestplot':
        return forestplot.render("Emergency Department visits and Hospital Admissions for Asthma")
    if tab == 'toxplot':
        return animaltox.render("Ozone ISA Cardiovascular Effects")




if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)