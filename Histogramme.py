import pandas as pd
import plotly_express as px


def getHistogramme(dataFrame):

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

    # Renommer la légende "count" sur l'axe y
    hist.update_layout(yaxis_title_text='Nombre de communes')

    # Ajuster la marge supérieure
    hist.update_layout(margin=dict(t=10))
    
    # Changer l'échelle de couleur
    hist.update_traces(marker=dict(colorscale='Viridis'))
    
    return hist