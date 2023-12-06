import pandas as pd
from io import StringIO
import requests

def getDataFrame():
    """Fonction qui récupère les données depuis une URL, les lit grâce à StringIO et renvoie un dataFrame légèrement modifié
        avec le bon caractère de séparation décimal et le bon encodage.

    Returns:
        dataFrame: Objet panda qui contient toutes les données récupérées de manière dynamique
    """
    # fetching csv
    response = requests.get("https://www.data.gouv.fr/fr/datasets/r/bc9d5d13-07cc-4d38-8254-88db065bd42b").text

    # create dataframe
    csv_buffer = StringIO(response)
    dataFrame = pd.read_csv(csv_buffer, sep=";", encoding="latin-1")

    # Convertir la colonne 'loypredm2' en float
    dataFrame["loypredm2"] = dataFrame["loypredm2"].str.replace(",", ".").astype(float)

    return dataFrame