import folium
import numpy as np


def getMap(dataFrame):
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