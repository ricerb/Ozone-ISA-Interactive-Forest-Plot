from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


ROOT = Path(__file__).resolve().parent
dataset = str(ROOT / 'forest_plot_epi_resp_data.csv')
assert Path(dataset).exists()

df = pd.read_csv(dataset)
columns = list(df.columns.values)
dimensions = columns[0:9]


app = dash.Dash(__name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"])
server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([html.H3('Ozone ISA Interactive Forest Plot Prototype'),

    html.Div([
        html.Div(
                [
                    html.P([d + ":", dcc.Dropdown(id=d,
                    options=[dict(label=x, value=x) for x in df[d].unique()],
                    value=[x for x in df[d].unique()],
                    multi=True)])
                    for d in dimensions
                ],
                style={"width": "100%", "float": "left", "display": "inline-block"},
        )
    ]),
    dcc.Graph(id='output-graph', style={"width": "100%", "display": "inline-block"})

  ]
)

@app.callback(
  Output(component_id='output-graph', component_property='figure'),
  [Input(component_id=d, component_property='value') for d in dimensions])

def update_graph(Health_Outcome_Measure, Exposure_Timing, Study_Name, Study_Year, Study_Type,
Location, Age, Mean_ppb, Lag):

    filterables = [Health_Outcome_Measure, Exposure_Timing, Study_Name, Study_Year, Study_Type,
    Location, Age, Mean_ppb, Lag]

    for f in filterables:
        if type(f) != list:
            f = ['']

    gdf = df[(df.iloc[:,0].isin(filterables[0]))&
    (df.iloc[:,1].isin(filterables[1]))&
    (df.iloc[:,2].isin(filterables[2]))&
    (df.iloc[:,3].isin(filterables[3]))&
    (df.iloc[:,4].isin(filterables[4]))&
    (df.iloc[:,5].isin(filterables[5]))&
    (df.iloc[:,6].isin(filterables[6]))&
    (df.iloc[:,7].isin(filterables[7]))&
    (df.iloc[:,8].isin(filterables[8]))]

    gdf['ID'] = gdf['Study Name'].astype(str) + ' (' + gdf['Age'].astype(str) + ')'

    fig = px.scatter(gdf, y='ID', x='OR',
    error_x='Upper_Error', error_x_minus='Lower_Error',
    hover_data = ['Health Outcome Measure', 'Exposure Timing','Study Type', 'Location', 'Age',
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
    fig.update_layout(height=1000)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)
