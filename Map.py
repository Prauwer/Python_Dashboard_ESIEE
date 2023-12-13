import folium
import numpy as np

from Data import getDataFrame


def getMap(url):
    """Génère la carte des départements français, coloré par prix moyen du loyer.

    Args:
        url (str): URL pour récupérer les données en CSV.

    Returns:
        Map : carte généré.
    """
    # Récupérer le DataFrame
    dataFrame = getDataFrame(url)
    
    
    # Regrouper les valeurs par communes en valeurs par département de France métropolitaine
    groupedData = dataFrame.groupby("DEP")["loypredm2"].mean().reset_index()
    
    # Appliquer la fonction logarithme aux valeurs afin de compenser la trop grande différence 
    # entre l'île de France et le reste de la france métropolitaine.
    groupedData['loypredm2_log'] = np.log1p(groupedData['loypredm2'])

    # Mettre le centre de la carte au centre de la France
    coords = (46.539758, 2.430331)
    
    # Créer la carte
    map = folium.Map(location=coords, tiles="OpenStreetMap", zoom_start=6)

    

    folium.Choropleth(
        geo_data="departements.geojson",    # Limites des départements
        name='choropleth',
        data=groupedData,                   # Données des loyers par départements
        columns=['DEP', 'loypredm2_log'],   # Paire clé/valeur des données numériques
        key_on='feature.properties.code',   # propriété géographique utilisée pour établir une correspondance avec des données numériques (ici le code département)
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        log_scale=True,                     # Utilisation de l'échelle de couleur logarithmique
        legend_name="Prix du loyer (en €/m²)"
    ).add_to(map)
    
    return map