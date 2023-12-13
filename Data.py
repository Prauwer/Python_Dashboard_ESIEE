import pandas as pd
from io import StringIO
import requests

def getDataFrame(url: str):
    # fetching csv
    response = requests.get(url).text

    # create dataframe
    csv_buffer = StringIO(response)
    dataFrame = pd.read_csv(csv_buffer, sep=";", encoding="latin-1")

    # Convertir la colonne 'loypredm2' en float
    dataFrame["loypredm2"] = dataFrame["loypredm2"].str.replace(",", ".").astype(float)

    return dataFrame