import pandas as pd
from io import StringIO
import requests


def getDataFrame():
    """Récupération des données CSV et création du dataFrame

    Args:
        url (str): URL pour récupérer les données en CSV.

    Returns:
        DataFrame: dataFrame des prix moyen du loyer par département
    """
    # Récupération du csv
    response = requests.get("https://www.data.gouv.fr/fr/datasets/r/bc9d5d13-07cc-4d38-8254-88db065bd42b").text

    # création du DataFrame
    csv_buffer = StringIO(response)
    dataFrame = pd.read_csv(csv_buffer, sep=";", encoding="latin-1")

    # Convertir la colonne 'loypredm2' (prix moyen du loyer) en float
    dataFrame["loypredm2"] = dataFrame["loypredm2"].str.replace(",", ".").astype(float)

    return dataFrame