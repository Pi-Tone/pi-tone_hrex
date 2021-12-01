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
    external_stylesheets=[dbc.themes.CYBORG],
    routes_pathname_prefix='/dash-hrex-pct/'
)
app.title = "加拿大锦程-企业坞"
server = app.server

#Create HeaderSection
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
    wrapLongitude=True,
)

view_state = pdk.ViewState(
    latitude=38.653508, longitude=-171.028072, bearing=0, pitch=0, zoom=3,
)


TOOLTIP_TEXT = {
    "html": "{S000} shipments <br /> View details under table"
}
r = pdk.Deck(arc_layer,initial_view_state=view_state, tooltip=TOOLTIP_TEXT, map_provider='mapbox', map_style="mapbox://styles/kforris/ckwncfb0s4fwi14nxtx6or8tu")


#Create Status_Overview_Chart
def Status_Overview():
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

#Create GanttChart
df = pd.DataFrame([
    dict(Task="Freight Tracking & Management", Start='2021-01-01', Finish='2021-11-12', Staff='Terry Zhang'),
    dict(Task="Front Desk Inquiry", Start='2021-02-22', Finish='2021-12-01', Staff="Ivy"),
    dict(Task="Website Maintenance", Start='2021-01-05', Finish='2021-05-22', Staff="Tony Wong")
])
ganttchart_example = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Staff")


excel_table = pd.read_csv(DATA_PATH + 'orderhrex.csv')

def gen_excel_table_chart(df, max_rows=10):
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

#Create RiskTrend_Chart
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



# Create app layout
app.layout = html.Div(
    html.Div(
        [# empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        dbc.Row([
                    dbc.Col([
                        drawHeader(),
                    ], style={"margin-bot":"50px"},width='100%', md=12),
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
                                                  style={"width":"73vw","height":"35vh","display":"inline-block"},
                                                  ))], width=12,
                        style={"height":"100%", "display":"inline"}, md=10, align="start"),
                    dbc.Col([
                        Status_Overview()
                    ], width=12,style={"height": '100%'}, md=2, align="end")
                ],align="center"),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(figure=ganttchart_example, config={
                        'displayModeBar': False}),], width=12, md=3),
                    dbc.Col([
                        html.Div(gen_excel_table_chart(excel_table)),], width=12, md=7),
                    dbc.Col([
                        drawFigure()
                    ], width=12, md=2),
                ], align='center'),
            ]), color='white',),
        ],))




#Main
if __name__ == "__main__":
    app.run_server(debug=True)
