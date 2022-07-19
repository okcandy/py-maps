# Load libraries
import pandas as pd
import json
from urllib.request import urlopen
import geojson
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output 

with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
    Brazil = json.load(response) 


app = Dash(__name__)

# Load the data
url = 'https://raw.githubusercontent.com/okcandy/py-maps/main/amazon.csv'
brazil_df = pd.read_csv(url, sep=",", encoding='latin1')
print(brazil_df)

state_id_map = {}
for Feature in Brazil['features']:
 Feature['id'] = Feature['properties']['name']
 state_id_map[Feature['properties']['sigla']] = Feature['id']

# App layout
app.layout = html.Div([

    html.H1("Visualizing Brazil Wildfires from 1998 - 2017", style={'text-align': 'center', "fontSize": "40px", "background-color": 'black', "color": "#FED8B1", "padding": "15px", "border-radius": "45px"}),

    dcc.Dropdown(id="select_year",
                 options=[
                     {"label": "1998", "value": 1998},
                     {"label": "1999", "value": 1999},
                     {"label": "2000", "value": 2000},
                     {"label": "2001", "value": 2001},
                     {"label": "2002", "value": 2002},
                     {"label": "2003", "value": 2003},
                     {"label": "2004", "value": 2004},
                     {"label": "2005", "value": 2005},
                     {"label": "2006", "value": 2006},
                     {"label": "2007", "value": 2007},
                     {"label": "2008", "value": 2008},
                     {"label": "2009", "value": 2009},
                     {"label": "2010", "value": 2010},
                     {"label": "2011", "value": 2011},
                     {"label": "2012", "value": 2012},
                     {"label": "2013", "value": 2013},
                     {"label": "2014", "value": 2014},
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017}],
                 multi=False,
                 value=1998,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='brazil_map', figure={})

])

# Joining plotly graphs with dash
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='brazil_map', component_property='figure')],
    [Input(component_id='select_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Selected Year : {}".format(option_slctd)

    wildfires = brazil_df.copy()
    wildfires = wildfires[wildfires["year"] == option_slctd]
  

    # Plotly Express
    fig = px.choropleth_mapbox(
        data_frame=wildfires,
        locations = 'state',
        geojson = Brazil,
        color='number',
        hover_data=['state', 'number'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        mapbox_style = "carto-positron",
        labels={'number': 'Number of Wildfires', 'state' : 'State'},
        center={"lat":-14, "lon": -55},
        zoom = 3,
        opacity = 0.7,
        animation_frame = 'year',
        template='plotly_dark',       
    )
    
    fig.update_geos(fitbounds = 'geojson', visible = False, scope = "south america")
    
    fig.update_layout(
                  height=540,
                  width=1500,
                  margin={"r":0,"t":0,"l":0,"b":0},
                 )

    fig.add_trace(go.Scattermapbox(
        text = "state"))

    return container, fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='0.0.0.0')