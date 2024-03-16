from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd

import plotly.express as px



df = pd.read_csv('FrailtyParameters.csv')
headers = list(df.columns.values)
parameters = headers[1:]

df['Date'] = pd.to_datetime(df['Date'])


app = Dash(__name__)


app.layout = html.Div([

    html.Div([
        html.H2('Left vs Right FrailtyScore Data', className='title'),
        html.Img(src="/assets/logo.png"),
    ], className='banner'),

    html.Div([
        dcc.Graph(id="graph"),
        html.P("Variable:"),
        dcc.Dropdown(id="parameter", options=parameters,value="FrailtyScore",clearable=False)
    ]),
])


@app.callback(
    Output("graph", "figure"),
    Input("parameter", "value"))

def display_time_series(parameter):

    fig = px.line(df, x='Date', y=parameter, markers=True)

    if parameter == 'FrailtyScore':
        yrange = [0, 100]
    else:
        yrange = [0, 1]

    fig.update_layout(yaxis_range=yrange)

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    return fig


app.run_server(debug=True)