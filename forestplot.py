from pathlib import Path

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
dataset = str(ROOT / 'forest_plot_epi_resp_data.csv')
assert Path(dataset).exists()

df = pd.read_csv(dataset)
df['Exposure Quartile'] = df['Exposure Quartile'].str.strip('](')
df['Exposure Quartile'] = df['Exposure Quartile'].replace('18.398999999999997, 32.65', '18.4. 32.65')

##Create and arrange selectors

dcol1 = ['Health Outcome Measure', 'Study Name']
dcol2 = ['Study Year','Study Type', 'City',]
dcol3 = ['Age Group', 'Exposure Quartile', 'Lag']

dimensions = dcol1 + dcol2 + dcol3

def createselector(dimensions):
    return [html.P([d + ":", dcc.Dropdown(id=d,
            options=[dict(label=x, value=x) for x in df[d].unique()],
            value=[x for x in df[d].unique()],
            multi=True)]) 
            for d in dimensions]

selectors = [createselector(dcol1), createselector(dcol2), createselector(dcol3)]

selectors.append(
     html.P(["Sort by:", dcc.Dropdown(id="sort-by",
                    options=[dict(label="Study Year", value='year'),
                        dict(label="Study Name", value='name'),
                        dict(label="Exposure Level", value='mean ppb')],
                    value="b",
                    multi=False)])
)

##Create callback and make plot

listeners = [Input(component_id=d, component_property='value') for d in dimensions]
listeners.append(Input(component_id="sort-by", component_property='value'))


def startup(app):
    
    @app.callback([Output(component_id='output-graph', component_property='figure'),
                Output(component_id='output-table', component_property='data'),
                Output(component_id='output-table', component_property='columns')],
                listeners)

    def update_data(Health_Outcome_Measure, Study_Name, Study_Year, Study_Type,
    City, Age_Group, Exposure_Quartile, Lag, SortBy):

        filterables = [Health_Outcome_Measure, Study_Name, Study_Year, Study_Type,
        City, Age_Group, Exposure_Quartile, Lag]
        
        gdf = df
        for i, f in enumerate(filterables):
            if type(f) != list:
                f = ['']
            gdf = gdf[(gdf.iloc[:,i].isin(f))]


        if SortBy=='year':
            gdf = gdf.sort_values(['Study Year', 'Study Name'], ascending = False)
        elif SortBy == 'name':
            gdf = gdf.sort_values(['Study Name', 'Study Year'], ascending = False)
        elif SortBy == 'mean ppb':
            gdf = gdf.sort_values(['mean ppb est'], ascending = True)
        
        gdf['ID'] = gdf['Study Name'].astype(str) + ' (' + gdf['Result Detail'].astype(str) + ')' +' (' + gdf['Age'].astype(str) + ')'
        gdf['ID'].replace('\s\(nan\)', '', inplace = True, regex = True)


        fig = px.scatter(gdf, y='ID', x='OR',
        error_x='Upper_Error', error_x_minus='Lower_Error',
        hover_data = ['Study Year', 'Health Outcome Measure', 'Exposure Timing','Study Type', 'Country', 'City', 'Age', 'Age Group',
        'Mean ppb', 'Location in 2019 Ozone ISA'])

        fig.add_shape(
                # Line Vertical
                go.layout.Shape(
                    layer='below',
                    type="line",
                    x0=1,
                    y0=-0.5,
                    x1=1,
                    y1=(len(gdf.index)-0.5),
                    line=dict(
                        color="LightSlateGrey",
                        width=1.5,
                        dash = "dashdot"
                    )))

        fig.update_xaxes(showgrid = False, zeroline = False)
        fig.update_yaxes(showgrid=False)
        fig.update_traces(marker=dict(color='DarkSlateGrey', size=12, line=dict(width=2, color='black')))
        fig.update_layout(height=1000, yaxis_title="")

        data = gdf.to_dict('records')
        cols = [{"name": i, "id": i} for i in gdf.columns]

        return fig, data, cols



def render(title):

    ## Create Divs
    return  html.Div([
         html.H5(title),
        html.Div([
            html.Div(
                    s,
                    style={"width": "33%", "float": "left", "display": "inline-block"},
            ) for s in selectors
        ]),
        dcc.Graph(id='output-graph', style={"width": "100%", "display": "inline-block"}),
        html.H5('Input Data:'),
        dash_table.DataTable(
            id='output-table',
            style_table={'overflowX': 'scroll',
                'overflowY': 'scroll',
                'maxHeight': '500px'})
    ])