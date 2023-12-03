from io import StringIO
import folium
import numpy as np
import plotly_express as px


import dash
from dash import dcc
from dash import html
import pandas as pd
import requests

# faire le nombre de communes par tranche de loyer.

# Main

if __name__ == "__main__":
    app = dash.Dash(__name__)

    # fetching csv
    response = requests.get("https://www.data.gouv.fr/fr/datasets/r/bc9d5d13-07cc-4d38-8254-88db065bd42b").text

    # create dataframe
    csv_buffer = StringIO(response)
    dataFrame = pd.read_csv(csv_buffer, sep=";", encoding="latin-1")

    # Convertir la colonne 'loypredm2' en float
    dataFrame["loypredm2"] = dataFrame["loypredm2"].str.replace(",", ".").astype(float)

    # Créer des tranches de prix de loyer
    tranches_prix = [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 25, 30, 35]

    # Ajouter une colonne 'TrancheLoyer' au DataFrame
    dataFrame['TrancheLoyer'] = pd.cut(dataFrame['loypredm2'], bins=tranches_prix, right=False)

    # Trier les tranches par ordre croissant
    dataFrame.sort_values(by='TrancheLoyer', inplace=True)

    # Convertir les Intervalles en chaînes
    dataFrame['TrancheLoyer'] = dataFrame['TrancheLoyer'].astype(str)
    
    # Créer l'histogramme avec plotly_express
    hist = px.histogram(
        dataFrame,
        x='TrancheLoyer',
        labels={'TrancheLoyer': 'Tranche de loyer (€/m²)', 'count': 'Nombre de communes'},
        color='TrancheLoyer',
    )
    # Ajouter les étiquettes de texte
    hist.update_traces(texttemplate='%{y}', textposition='outside')

    # Ajuster la marge supérieure
    hist.update_layout(margin=dict(t=10))
    
    # Changer l'échelle de couleur
    hist.update_traces(marker=dict(colorscale='Viridis'))

    # CREATE MAP
    groupedData = dataFrame.groupby("DEP")["loypredm2"].mean().reset_index()
    groupedData['loypredm2_log'] = np.log1p(groupedData['loypredm2'])

    coords = (46.539758, 2.430331)
    map = folium.Map(location=coords, tiles="OpenStreetMap", zoom_start=6)

    

    folium.Choropleth(
        geo_data="departements.geojson",    # geographical data
        name='choropleth',
        data=groupedData,                   # numerical data
        columns=['DEP', 'loypredm2_log'],   # numerical data key/value pair
        key_on='feature.properties.code',   # geographical property used to establish correspondance with numerical data
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        log_scale=True,
        legend_name="Prix du loyer (en €/m²)"
    ).add_to(map)

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
