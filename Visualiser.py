from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px


df = pd.read_csv('FrailtyParameters.csv')

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children='Frailty Data'),
    html.Hr(),
    dcc.RadioItems(options=['value', 'score'], value='value', id='buttons'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=6),
    dcc.Graph(figure={}, id='graph')
])


@callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='buttons', component_property='value')
)
def update_graph(col_chosen):
    fig = px.line_polar(df, r = 'score', theta = 'Parameter', line_close = True)
    return fig


if __name__ == '__main__':
    app.run(debug=True)
