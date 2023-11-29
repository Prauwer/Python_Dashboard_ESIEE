import plotly_express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

# Main

if __name__ == "__main__":
    app = dash.Dash(__name__)

    # create dataframe

    dataFrame = pd.read_csv("pred-app-mef-dhup.csv", sep=";", encoding="latin-1")

    # create histogram
    dataFrame["loypredm2"] = dataFrame["loypredm2"].str.replace(",", ".").astype(float)
    groupedData = dataFrame.groupby("DEP")["loypredm2"].mean().reset_index()

    hist = px.histogram(groupedData, x="DEP", y="loypredm2")

    app.layout = html.Div(
        children=[
            html.H1(
                children="Prix du loyer par département",
                style={"textAlign": "center", "color": "#7FDBFF"},
            ), 
            dcc.Graph(id="graph1", figure=hist),
            html.Div(
                children="Ce graphe montre le prix du loyer par département."
            )
        ]
    )

    # RUN APP

    app.run_server(debug=True)
