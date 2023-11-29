import plotly_express as px
import pandas as pd
import numpy as np
import geojson
import geopandas
import folium

# create dataframe

dataFrame = pd.read_csv("pred-app-mef-dhup.csv", sep=";", encoding="latin-1")

# create histogram
dataFrame["loypredm2"] = dataFrame["loypredm2"].str.replace(",", ".").astype(float)
groupedData = dataFrame.groupby("DEP")["loypredm2"].mean().reset_index()

hist = px.histogram(groupedData, x="DEP", y="loypredm2")
# hist.show()


# create map

coords = (46.539758, 2.430331)
map = folium.Map(location=coords, tiles="OpenStreetMap", zoom_start=6)


folium.Choropleth(
    geo_data="departements.geojson",                              # geographical data
    name='choropleth',
    data=groupedData,                                  # numerical data
    columns=['DEP', 'loypredm2'],                     # numerical data key/value pair
    key_on='feature.properties.code',       # geographical property used to establish correspondance with numerical data
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Prix du loyer'
).add_to(map)

map.save(outfile="map.html")
