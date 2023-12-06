from io import StringIO


import dash
from dash import dcc
from dash import html
import pandas as pd
import requests

from Histogramme import getHistogramme
from Map import getMap

# faire le nombre de communes par tranche de loyer.

# Main

def getDataFrame():
    # fetching csv
    response = requests.get("https://www.data.gouv.fr/fr/datasets/r/bc9d5d13-07cc-4d38-8254-88db065bd42b").text

    # create dataframe
    csv_buffer = StringIO(response)
    dataFrame = pd.read_csv(csv_buffer, sep=";", encoding="latin-1")

    # Convertir la colonne 'loypredm2' en float
    dataFrame["loypredm2"] = dataFrame["loypredm2"].str.replace(",", ".").astype(float)

    return dataFrame

if __name__ == "__main__":
    app = dash.Dash(__name__)

    dataFrame = getDataFrame()
    
    hist = getHistogramme(dataFrame)
    map = getMap(dataFrame)

    # CREATE DASHBOARD

    app.layout = html.Div(
        children=[
            html.Div(
              children=[
                    html.H1(
                      children="DASHBOARD",
                    ),
                    html.H3(
                        children="Analyse des données de loyer",
                    ),
              ],
              style={"padding": "1em", "background": "#06668c", "color": "#ebf2fa"},
            ),
            html.Div(
                children=[
                    html.H2(
                        children="Histogramme du nombre de communes par tranche de loyer moyen",
                        style={"color": "#2b2b2b"},
                    ), 
                    dcc.Graph(id="graph1", figure=hist),
                    html.Div(
                        children="Ce graphe montre le nombre de communes par tranche de loyer moyen.",
                        style={"color": "#2b2b2b", "padding": "0.5em"},
                    ),
                ],
                style={"background":"white", "margin": "1em", "padding": "1em", "border-radius": "5px"},
            ),
            html.Div(
                children=[
                    html.H2(
                        children="Carte du prix du loyer par département",
                        style={"color": "#2b2b2b"},
                    ), 
                    html.Iframe(
                        id='map1',
                        srcDoc=map._repr_html_(),
                        style={'width': '100%', 'height': '100vh'}
                    ),
                ],
                style={"background":"white", "margin": "1em", "padding": "1em", "border-radius": "5px"},
            )
        ],
        style={"fontFamily": "Verdana, sans-serif", "background": "#f7f7f7"}
    )

    # RUN APP

    app.run_server(debug=True)
