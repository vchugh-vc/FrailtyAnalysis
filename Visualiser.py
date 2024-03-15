from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px


df = pd.read_csv('FrailtyParameters.csv', index_col=0)

print(df)

theta = df.columns.tolist()

rows = df.head()
dates = list(rows.index)

print(dates)

def comparison():
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
          r=df.iloc[0],
          theta=theta,
          fill='toself',
          name='Left'
    ))
    fig.add_trace(go.Scatterpolar(
          r=df.iloc[1],
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
        html.Div(children='Left vs Right FrailtyScore Data'),
        dash_table.DataTable(data=df.to_dict('records'), page_size=10),
        dcc.Graph(figure=fig)
    ])

    if __name__ == '__main__':
        app.run(debug=True)

def selector():

    app = Dash(__name__)

    app.layout = html.Div(id='parent', children=[

        # creating a slider within a html componen

        # creating a dropdown within a html component
        html.Div(id='dropdown-div', children=
        [dcc.Dropdown(id='continent-dropdown',
                      options=dates,
                      value=dates[0]
                      )], style={'width': '50%', 'display': 'inline-block'}),
        # inline-block : to show slider and dropdown in the same line

        # setting the graph component
        dcc.Graph(id='scatter-plot')
    ])

    # Add controls to build the interaction
    @callback(Output(component_id='scatter-plot', component_property='figure'),
                  [Input(component_id='continent-dropdown', component_property='value')])

    def graph_update(continent_value):
        # filtering based on the slide and dropdown selection

        # the figure/plot created using the data filtered above
        fig = px.line_polar(df.transpose(), r=continent_value, theta=theta, line_close=True)

        return fig

    # Run the app
    if __name__ == '__main__':
        app.run(debug=True)

# Run the app

selector()