from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


df = pd.read_csv('FrailtyParameters.csv')

theta = df.columns.tolist()[1:]
r1 = df.loc[0, :].values.flatten().tolist()[1:]
r2 = df.loc[1, :].values.flatten().tolist()[1:]


def comparison():
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
          r=r1,
          theta=theta,
          fill='toself',
          name='Left'
    ))
    fig.add_trace(go.Scatterpolar(
          r=r2,
          theta=theta,
          fill='toself',
          name='Right'
    ))

    fig.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 1]
        )),
      showlegend=True
    )

    app = Dash(__name__)

    # App layout
    app.layout = html.Div([
        html.Div(children='My First App with Data and a Graph'),
        dash_table.DataTable(data=df.to_dict('records'), page_size=10),
        dcc.Graph(figure=fig)
    ])

    if __name__ == '__main__':
        app.run(debug=True)

def selector():

    app = Dash(__name__)

    # App layout
    app.layout = html.Div([
        html.Div(children='My First App with Data, Graph, and Controls'),
        html.Hr(),
        dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item'),
        dash_table.DataTable(data=df.to_dict('records'), page_size=6),
        dcc.Graph(figure={}, id='controls-and-graph')
    ])

    # Add controls to build the interaction
    @callback(
        Output(component_id='controls-and-graph', component_property='figure'),
        Input(component_id='controls-and-radio-item', component_property='value')
    )
    def update_graph(col_chosen):
        fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
        return fig

    # Run the app
    if __name__ == '__main__':
        app.run(debug=True)

# Run the app

comparison()