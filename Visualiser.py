from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

theta = ["Date", "UpAccZ","UpDelta","UpSPARC","UpRoll","UpPitch","MiddleDelta","MiddleAccZ","MiddleSPARC"]
r = [1,0.813,0.574,0.641,0.422,0.879,0.884,0.661,0.278]
r2 = [2,0.413,0.274,0.141,0.622,0.279,0.184,0.161,0.178]

df = pd.read_csv('FrailtyParameters.csv')

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
      r=r[1:],
      theta=theta[1:],
      fill='toself',
      name='Left'
))
fig.add_trace(go.Scatterpolar(
      r=r2[1:],
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
    html.Div(children='My First App with Data and a Graph'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=fig)
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)