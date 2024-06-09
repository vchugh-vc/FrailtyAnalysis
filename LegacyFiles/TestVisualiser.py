from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px


df = pd.read_csv('../FrailtyParameters.csv', index_col=0)

theta = df.columns.tolist()

rows = df.head()
date = list(rows.index)
dates = np.array(date)


def comparison():
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=df.iloc[0][1:],
        theta=theta[1:],
        fill='toself',
        name='Left'
    ))
    fig.add_trace(go.Scatterpolar(
        r=df.iloc[1][1:],
        theta=theta[1:],
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
        fig = px.line_polar(df.transpose(), r=continent_value, theta=theta, line_close=True, range_r=[0, 1])

        return fig

    # Run the app
    if __name__ == '__main__':
        app.run(debug=True)


# Run the app

def linear():
    fig = go.Figure()

    # Set title
    fig.update_layout(
        title_text="Time series with range slider and selectors"
    )

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True,
            ),
            type="date",
            ticks='inside',
            showticklabels=True
        )
    )

    app = Dash(__name__, assets_folder='assets')

    # App layout
    app.layout = html.Div([

        html.Div([
            html.H2('Left vs Right FrailtyScore Data', className='title'),
            html.Img(src="/assets/logo.png"),
        ], className='banner'),
        html.Div([
            dash_table.DataTable(data=df.reset_index().to_dict(orient='records'), page_size=10),
            dcc.Dropdown(theta, 'FrailtyScore', id='frailtyparameter'),
            dcc.Graph(figure=fig, id="graph")
        ]),
    ])

    @callback(
        Output('graph', 'figure'),
        Input('frailtyparameter', 'value'))
    def update_graph(frailtyparameter):

        fig.data = []
        fig.add_trace(
            go.Scatter(x=list(df.index), y=df[frailtyparameter], mode='markers'))
        if frailtyparameter == 'FrailtyScore':
            yrange = [0, 100]
        else:
            yrange = [0, 1]

        fig.update_layout(yaxis_range=yrange,     font=dict(size=18))

        return fig

    if __name__ == '__main__':
        app.run(debug=True)


linear()
