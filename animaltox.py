from pathlib import Path
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

###Import and process data

ROOT = Path(__file__).resolve().parent
dataset = str(ROOT / 'Ozone_ISA_CVD_effects.csv')
assert Path(dataset).exists()

df = pd.read_csv(dataset)
df['SUBJECT_NOTES'] = df['SUBJECT_NOTES'].fillna('NR')

##Create and arrange selectors

dcol1 = ['STUDY', 'STUDY_TYPE', 'DURATION_TYPE', 'SUBJECT_GROUP', 'SUBJECT_DETAILS']
dcol2 = ['SUBJECT_NOTES', 'EXPOSURE_DETAILS']
dcol3 = ['TIMING_OF_MEASUREMENT', 'ENDPOINT_CATEGORY']

dimensions = dcol1 + dcol2 + dcol3

def createselector(dimensions):
    return [html.P([d + ":", dcc.Dropdown(id=d,
            options=[dict(label=x, value=x) for x in df[d].unique()],
            value=[x for x in df[d].unique()],
            multi=True)]) 
            for d in dimensions]

selectors = [createselector(dcol1), createselector(dcol2), createselector(dcol3)]
'''
##Create sort by dropdown

selectors.append(
     html.P(["Sort by:", dcc.Dropdown(id="sort-by",
                    options=[dict(label="Study Name", value='name'),
                        dict(label="Study Year", value='year'),
                        dict(label="Exposure Level", value='mean ppb')],
                    value="name",
                    multi=False)])
)
'''
##Create callback and make plot

listeners = [Input(component_id=d, component_property='value') for d in dimensions]
#listeners.append(Input(component_id="sort-by", component_property='value'))

def startup(app):
    
    @app.callback([Output(component_id='output-graph2', component_property='figure'),
                Output(component_id='output-graph3', component_property='figure'),
                Output(component_id='output-table2', component_property='data'),
                Output(component_id='output-table2', component_property='columns')],
                listeners)

    def update_data2(STUDY, STUDY_TYPE, DURATION_TYPE, SUBJECT_GROUP,
        SUBJECT_DETAILS, SUBJECT_NOTES, EXPOSURE_DETAILS, TIMING_OF_MEASUREMENT, ENDPOINT_CATEGORY):

        ##Create filters
        
        filterables = [STUDY, STUDY_TYPE, DURATION_TYPE, SUBJECT_GROUP,
        SUBJECT_DETAILS, SUBJECT_NOTES, EXPOSURE_DETAILS, TIMING_OF_MEASUREMENT, ENDPOINT_CATEGORY]
        
        gdf = df
        print(gdf.columns)
        for i, f in enumerate(filterables):
            if type(f) != list:
                f = ['']
            gdf = gdf[(gdf.iloc[:,i].isin(f))]
        '''
        ##Deal with sorting
        if SortBy=='year':
            gdf = gdf.sort_values(['Study Year', 'Study Name'], ascending = False)
        elif SortBy == 'name':
            gdf = gdf.sort_values(['Study Name', 'Study Year'], ascending = False)
        elif SortBy == 'mean ppb':
            gdf = gdf.sort_values(['mean ppb est'], ascending = True)
        '''
        ###create figure
        fig = px.sunburst(gdf, path=['STUDY_TYPE','ENDPOINT_CATEGORY', 'ENDPOINT', 'STUDY', 'SUBJECT_GROUP', 'SUBJECT_DETAILS', 
                            'EXPOSURE_DETAILS', 'TIMING_OF_MEASUREMENT', 'RESPONSE'],
                          color = 'Increasing (Red) Decreasing (Blue)',
                          color_continuous_scale = px.colors.diverging.RdBu[::-1],
                            #['darkblue', 'white', 'darkred'],
                          color_continuous_midpoint = np.average(df['Increasing (Red) Decreasing (Blue)']) )
        fig.update_layout(height = 1000)

        ##create second figure:
        fig2 = px.treemap(gdf, path = ['STUDY_TYPE','ENDPOINT_CATEGORY', 'ENDPOINT', 'STUDY', 'SUBJECT_TEXT', 
                            'EXPOSURE_DETAILS', 'TIMING_OF_MEASUREMENT', 'RESPONSE'],
                      color = 'Increasing (Red) Decreasing (Blue)',
                      color_continuous_scale = px.colors.diverging.RdBu[::-1],
                      color_continuous_midpoint = np.average(df['Increasing (Red) Decreasing (Blue)']) )
        fig2.update_layout(height = 1000)

        ###create table fields

        data = gdf.to_dict('records')
        cols = [{"name": i, "id": i} for i in gdf.columns]

        return fig, fig2, data, cols


def render(title):

    ## Create Divs
    return  html.Div([
        html.H1(''),
        html.H5(title),
        html.H1(''),
        html.Div([
            html.Div(
                    s,
                    style={"width": "33%", "float": "left", "display": "inline-block"},
            ) for s in selectors
        ]),
        dcc.Graph(id='output-graph2', style={"width": "100%", "display": "inline-block"}),
        dcc.Graph(id='output-graph3', style={"width": "100%", "display": "inline-block"}),
        html.H5('Input Data:'),
        dash_table.DataTable(
            id='output-table2',
            style_table={'overflowX': 'scroll',
                'overflowY': 'scroll',
                'maxHeight': '500px'})
    ])