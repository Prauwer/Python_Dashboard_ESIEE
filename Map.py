import folium
import numpy as np


def getMap(dataFrame):
    """
    Crée une carte choroplèthe interactive à partir d'un DataFrame de données de loyer.

    Paramètres :
    -----------
    dataFrame : pd.DataFrame
        Un DataFrame Pandas contenant les données de loyer.

    Retour :
    --------
    folium.folium.Map
        Une carte choroplèthe interactive créée avec Folium.

    Notes :
    ------
    La fonction groupe les données par département, calcule la moyenne du loyer par département,
    puis crée une carte choroplèthe interactive avec Folium. La couleur des départements est basée sur
    le logarithme naturel du loyer moyen par mètre carré. La légende affiche le prix du loyer en €/m².

    Exemple :
    --------
    >>> map = getMap(dataFrame)

    """
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
    return map