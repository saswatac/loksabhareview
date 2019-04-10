import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from plotly import tools
from dash.dependencies import Input, Output

df_2014 = pd.read_csv("mp_track_2014.csv", delimiter='\t')
df_2009 = pd.read_csv("mp_track_2009.csv", delimiter='\t')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    style={"width": "100%", "height": "100%"},
    children=[
        html.H1(children='Compare Members'),
        dcc.Dropdown(
            id='constituency',
            options=[
                {'label': constituency, 'value': constituency}
                for constituency in df_2014.Constituency
            ],
            placeholder="Select a constituency",
            style={"width": "50%"}
        ),
        # data div
        html.Div(
            style={"width": "50%", "margin-left": "25%", "height": "700px"},
            children=[
                dcc.Graph(id='compare-member-by-year', style={'height': '700px'})
            ]
        )
    ]
)


@app.callback(
    Output('compare-member-by-year', 'figure'),
    [Input('constituency', 'value')])
def update_member(constituency_name):
    if not constituency_name:
        return []
    data_2014 = df_2014[df_2014.Constituency == constituency_name].iloc[0]
    data_2009 = df_2009[df_2009.Constituency == constituency_name].iloc[0]

    attribs = ["Debates", "Private Member Bills", "Questions", "Attendance"]
    fig = tools.make_subplots(rows=2, cols=2, subplot_titles=attribs)
    shapes = []
    for i, attr in enumerate(attribs):
        x = i / 2 + 1
        y = i % 2 + 1
        fig.append_trace(
            go.Bar(
                x=["2014", "2009"],
                y=[data_2014[attr], data_2009[attr]],
                marker=go.bar.Marker(color=['rgb(213, 101, 77)', 'rgb(135, 206, 250)']),
                width=[0.4, 0.4],
                name=attr
            ), x, y)
    fig['layout']['shapes'] = shapes
    for i in range(1, 5):
        fig['layout']["xaxis{}".format(i)]['type'] = "category"
    fig['layout']['xaxis3']['automargin'] = True
    fig['layout']['margin'] = {"b": 200}
    fig['layout']['showlegend'] = False
    fig['layout']['title'] = {"text": "2014: {} ({}) <br> Vs <br> 2009: {} ({})".format(
        data_2014["MP Name"],
        data_2014["Political party"],
        data_2009["MP Name"],
        data_2009["Political party"]),
        "font": {
            "size": 24,
        },
        "y": 0.2
    }
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
