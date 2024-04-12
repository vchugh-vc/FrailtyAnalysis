from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv('LongData.csv')
headers = list(df.columns.values)
parameters = headers[1:]
IMUParameters = headers[5:]
BiologyParameters = headers[2:5]

df['Date'] = pd.to_datetime(df['Date'])

df2 = pd.read_csv('LongData.csv')

app = Dash(__name__)

app.layout = html.Div([

    html.Div([
        html.H2('Frailty Data Trends'),
        html.Img(src="/assets/logo.png"),
    ], className='banner'),

    html.Div([
        dcc.Dropdown(id="parameter", options=parameters, value="FrailtyScore", clearable=False),
        dcc.Graph(id="time_graph"),
        html.H2('FrailtyScore Day Comparison'),
        dcc.Dropdown(id='snapshot_1', options=df2['Date'], value=df2.iloc[0]['Date']),
        dcc.Dropdown(id='snapshot_2', options=df2['Date'], value=df2.iloc[1]['Date']),
        dcc.Graph(id='radar-graph'),
        dcc.Graph(id='biology-graph')
    ], className='banner')

])


@app.callback(
    Output("time_graph", "figure"),
    Input("parameter", "value"))
def display_time_series(parameter):
    fig = px.scatter(df, x='Date', y=parameter, template='plotly', trendline="lowess")

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


@app.callback(
    Output('radar-graph', "figure"),
    Input('snapshot_1', "value"),
    Input('snapshot_2', 'value')
)
def display_radar(snapshot_1, snapshot_2):

    dff = df[df['Date'] == snapshot_1]
    dff_values = dff.values.tolist()

    dff_2 = df[df['Date'] == snapshot_2]
    dff_values_2 = dff_2.values.tolist()

    fig2 = px.line_polar(dff, r=dff_values[0][5:], theta=IMUParameters, line_close=True, range_r=[0, 1])

    fig3 = px.line_polar(dff_2, r=dff_values_2[0][5:], theta=IMUParameters, line_close=True, range_r=[0, 1])

    fig3.data[-1].name = f'{snapshot_2}'
    fig3.data[-1].showlegend = True

    fig2.data[-1].name = f'{snapshot_1}'
    fig2.data[-1].showlegend = True
    fig2.data[-1].line.color = 'red'

    fig2.add_trace(fig3.data[0])

    fig2.update_layout(showlegend=True)
    fig2.update()

    return fig2


@app.callback(
    Output('biology-graph', "figure"),
    Input('snapshot_1', "value"),
    Input('snapshot_2', 'value')
)
def display_biology(snapshot_1, snapshot_2):

    dff = df[df['Date'] == snapshot_1]
    dff_values = dff.values.tolist()

    dff_2 = df[df['Date'] == snapshot_2]
    dff_values_2 = dff_2.values.tolist()

    fig4 = px.line_polar(dff, r=dff_values[0][2:5], theta=BiologyParameters, line_close=True, range_r=[0, 1])
    fig5 = px.line_polar(dff_2, r=dff_values_2[0][2:5], theta=BiologyParameters, line_close=True, range_r=[0, 1])

    fig5.data[-1].name = f'{snapshot_2}'
    fig5.data[-1].showlegend = True

    fig4.data[-1].name = f'{snapshot_1}'
    fig4.data[-1].showlegend = True
    fig4.data[-1].line.color = 'red'

    fig4.add_trace(fig5.data[0])

    fig4.update_layout(showlegend=True)
    fig4.update()

    return fig4


app.run_server(debug=True, use_reloader=True)
