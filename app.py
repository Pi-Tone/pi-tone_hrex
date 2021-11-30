# Import required libraries
import pickle
import os
import copy
from pathlib import Path
import urllib.request
import dash
import math
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash import html
from dash import dcc
import plotly.express as px
from dash import dash_table
import dash_bootstrap_components as dbc
from datetime import datetime
import dash_deck
import pydeck as pdk

# get relative data folder
PATH = Path.cwd()
DATA_PATH = os.path.join(PATH, 'data\\')

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.SUPERHERO],
    routes_pathname_prefix='/dash-hrex-pct/'
)
app.title = "加拿大锦程-企业坞"
server = app.server

mapbox_access_token = "pk.eyJ1Ijoia2ZvcnJpcyIsImEiOiJja2J5a2hpMXUxMHBmMnFwYzBwNDU3andjIn0.o6CXRtTETx5soEEuCQZQ1w"

# Fake data for Gantt table
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})
ganttchart_example = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")


layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    legend=dict(font=dict(size=10), orientation="h"),
    title="业务地图",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-171.028072, lat=38.653508),
        zoom=7,
    ),
)
excel_table = pd.read_csv(DATA_PATH + 'orderhrex.csv')

def gen_data_for_excel(df, max_rows=10):
    cols = [['Shipper Name', 'Order No.'], ['Shipping Status', 'Order Date'], ['Is Paid', 'Paid Amount']]
    for col in cols:
        df[col[0]] = df[col].apply(lambda row: '\n'.join(row.values.astype(str)), axis=1)
    df = df[['Shipper Name', 'Shipping Status', 'Is Paid', 'Sale Amount']]
    return dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        style_cell={"whiteSpace": "pre-line", 'minWidth': 95, 'maxWidth': 95, 'width': 95},
        fixed_rows={'headers': True},
        page_action='none',
        style_table={'height': '500px', 'overflowY': 'auto'}
    )


def drawHeader():
    return html.Div(
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            [
                dbc.Row(
                [
                    dbc.Col(html.Img(src=app.get_asset_url("hrexicon.png"),
                                     id="dashboard-logo",
                                     style={
                                         "height": '7vh',
                                         "width": 'auto',
                                         "margin-bot": '50px',
                                     }, width='45%')),

                    dbc.Col(html.H6('Last Updated:' + str(excel_table['Order Date'].iloc[-1])),
                            style={
                                'text-align': 'right',
                                "width": 'auto',
                                'color': 'Navy'}, width='40%'),
                ],style={
                    'height': 'auto',
                    'text-align': 'auto',
                    'item-align': 'center',
                    "width": 'auto',
                    "margin-bbot": '50px'}, align='center'),
                dbc.Row(html.H2(children='加拿大锦程快递',
                                style={
                                    'text-align': 'center',
                                    'color': 'Navy',
                                    'margin-bot': '30px',
                                }), ),
                dbc.Row(
                    (html.H5(children='业务总览-Ontology',
                             style={
                                 'text-align': 'center',
                                 'color': 'Black',
                                 'margin-bot': '30px',
                             }),)),
                dbc.Row(
                    dbc.Button('了解更多',href='https://www.hr-ex.com', color='success',class_name='me-md-5 col-auto mx-auto'),
                ),]),style={'margin-bot':'30%'})

#Create Maingraph
mapbox_key = "pk.eyJ1Ijoia2ZvcnJpcyIsImEiOiJja2J5a2hpMXUxMHBmMnFwYzBwNDU3andjIn0.o6CXRtTETx5soEEuCQZQ1w"


DATA_URL = "https://raw.githubusercontent.com/Pi-Tone/pi-tone_hrex/master/data/df_geo111111.csv"
# A bounding box for downtown San Francisco, to help filter this commuter data

df_1 = pd.read_csv(DATA_URL)

GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]

# Specify a deck.gl ArcLayer
arc_layer = pdk.Layer(
    "ArcLayer",
    data=df_1,
    get_width="S000 * 2",
    get_source_position=["lng_s", "lat_s"],
    get_target_position=["lng_d", "lat_d"],
    get_tilt=15,
    get_source_color=RED_RGB,
    get_target_color=GREEN_RGB,
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(
    latitude=38.653508, longitude=-171.028072, bearing=0, pitch=0, zoom=3,
)


TOOLTIP_TEXT = {
    "html": "{S000} shipments <br /> View details under table"
}
r = pdk.Deck(arc_layer, initial_view_state=view_state, tooltip=TOOLTIP_TEXT, map_provider='mapbox')



def mainGraph():
    return ()

#create Graphs
def drawFigure():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(

                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    ),
                    config={
                        'displayModeBar': False
                    }
                ),
            ]),style={
                'text-align': 'center',
                'width': 'auto',
                'color':' white',}
        ),
    ])

#create Ganttchart
def ganttchart_graph():
    ()


# Create app layout
app.layout = html.Div(
    html.Div(
        [# empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        dbc.Row([
                    dbc.Col([
                        drawHeader(),
                    ], style={"margin-bot":"50px"},width='100%'),
                ], align='center', style={"margin-bot":"500px"}),
        dbc.Card(
            dbc.CardBody([
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.Div(dash_deck.DeckGL(r.to_json(),
                                                  id="deck-gl",
                                                  tooltip=TOOLTIP_TEXT,
                                                  mapboxKey=r.mapbox_key,
                                                  style={"width":"73vw","height":"35vh","display":"inline"},
                                                  ))], width=10,
                        style={"height":"100%"}),
                    dbc.Col([
                        drawFigure()
                    ], width=2,style={"height": '100%'},)
                ], align='center'),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(figure=ganttchart_example),
                    ], width=3),
                    dbc.Col([
                        html.Div(gen_data_for_excel(excel_table)),], width=7),
                    dbc.Col([
                        drawFigure()
                    ], width=2),
                ], align='center'),
            ]), color='white',),
        ],))




#Main
if __name__ == "__main__":
    app.run_server(debug=True)
