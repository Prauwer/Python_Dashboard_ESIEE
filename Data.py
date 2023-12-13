import pandas as pd
from io import StringIO
import requests
import re

def getDataFrame(url: str):
    """Récupération des données CSV, nettoyage des données reçues et création du dataFrame

    Args:
        url (str): URL pour récupérer les données en CSV.

    Returns:
        DataFrame: dataFrame des prix moyen du loyer par département
    """
    # Récupération du csv
    response = requests.get(url).text

    # création du DataFrame
    csv_buffer = StringIO(response)
    dataFrame = pd.read_csv(csv_buffer, sep=";", encoding="latin-1")

    # Nettoyer le dataframe
    # Supprimer les IDs dupliqués
    if not (dataFrame['INSEE_C'].is_unique):
        dataFrame.drop_duplicates(subset='INSEE_C')

    # Supprimer les noms dupliqués
    dataFrame['LIBGEO'] = dataFrame['LIBGEO'].apply(lambda x: re.sub(r'[éèêëàâäôöûüçÉÈÊËÀÂÄÔÖÛÜÇ\s-_]', '', x))
    if not (dataFrame['LIBGEO'].is_unique):
        dataFrame.drop_duplicates(subset='LIBGEO')


    # Convertir la colonne 'loypredm2' (prix moyen du loyer) en float
    dataFrame["loypredm2"] = dataFrame["loypredm2"].str.replace(",", ".").astype(float)

    return dataFrame