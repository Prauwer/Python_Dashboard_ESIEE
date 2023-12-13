import dash
from dash import dcc, html
from dash.dependencies import Input, Output

from Histogramme import getHistogramme
from Map import getMap

app = dash.Dash(__name__)

# URLs utilisé pour les données de loyers (maison, appartement T3 et plus, appartement T1 et T2, tous les appartements).
DATA_URL = {
    "maison": "https://www.data.gouv.fr/fr/datasets/r/dfb542cd-a808-41e2-9157-8d39b5c24edb",
    "appartementT3et+": "https://www.data.gouv.fr/fr/datasets/r/b398ede4-75f9-47ac-bfc5-d912c0012880",
    "appartementT1etT2": "https://www.data.gouv.fr/fr/datasets/r/7141612b-8029-44a4-a048-921a85a47b1f",
    "appartement": "https://www.data.gouv.fr/fr/datasets/r/bc9d5d13-07cc-4d38-8254-88db065bd42b",
}

# Création du layout du dashboard.
# Ici, on créer un objet Graph (l'histogramme ) et un objet Iframe (la carte), mais on les laisse vides.
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
            style={
                "padding": "1em",
                "background": "#06668c",
                "color": "#ebf2fa",
            },
        ),
        dcc.RadioItems(
            id="data-source",
            options=[
                {"label": "Maison", "value": "maison"},
                {"label": "Appartement T3 et plus", "value": "appartementT3et+"},
                {"label": "Appartement T1 et T2", "value": "appartementT1etT2"},
                {"label": "Appartement", "value": "appartement"},
            ],
            value="maison",  # Valeur par défaut
            labelStyle={"cursor": "pointer"},
            style={"display": "flex", "justify-content": "space-around", "padding": "1em", "background": "#427AA1", "color": "#ebf2fa", "cursor": "pointer"},
        ),
        html.Div(
            children=[
                html.H2(
                    children="Histogramme du nombre de communes par tranche de loyer moyen",
                    style={"color": "#2b2b2b"},
                ),
                dcc.Graph(id="graph1"),
                html.Div(
                    children="Ce graphe montre le nombre de communes par tranche de loyer moyen.",
                    style={"color": "#2b2b2b", "padding": "0.5em"},
                ),
            ],
            style={
                "background": "white",
                "margin": "1em",
                "padding": "1em",
                "border-radius": "5px",
            },
        ),
        html.Div(
            children=[
                html.H2(
                    children="Carte du prix du loyer par département",
                    style={"color": "#2b2b2b"},
                ),
                html.Iframe(id="map1", style={"width": "100%", "height": "100vh"}),
            ],
            style={
                "background": "white",
                "margin": "1em",
                "padding": "1em",
                "border-radius": "5px",
            },
        ),
    ],
    style={"fontFamily": "Verdana, sans-serif", "background": "#f7f7f7"},
)

@app.callback(
    [
        Output("graph1", "figure"), # on remplit l'attribut figure de l'objet d'id graph1 avec la première valeur retournée (ici histogram_figure)
        Output("map1", "srcDoc"),   # on remplit l'attribut srcDoc de l'objet d'id map1 avec la deuxième valeur retournée (ici map_src_doc)
    ],
    [Input("data-source", "value")], # On récupère la valeur sélectionné dans l'objet d'id data-source (un radio bouton)
)
def update_data_source(selected_source):
    """Récupère la source de données choisis (appartement, maison, T1 et T2, T3 et +) et on remplit les objets Graph et Iframe.

    Args:
        selected_source (str): source de données choisit dans le radio bouton

    Returns:
        histogram_figure Figure: histogramme généré
        map_src_doc Map : carte généré
    """
    histogram_figure = getHistogramme(DATA_URL[selected_source])
    map_src_doc = getMap(DATA_URL[selected_source])._repr_html_()
    return histogram_figure, map_src_doc

# Main
if __name__ == "__main__":
    app.run_server(debug=True)