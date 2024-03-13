from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

theta = ["UpAccZ","UpDelta","UpSPARC","UpRoll","UpPitch","MiddleDelta","MiddleAccZ","MiddleSPARC"]
r = [0.813,0.574,0.641,0.422,0.879,0.884,0.661,0.278]


df = pd.read_csv('FrailtyParameters.csv', parse_dates=True)

app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data and a Graph'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=px.line_polar(df, r=r, theta=theta, line_close=True))
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)