from collections import OrderedDict

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from plotly import tools
from plotly.colors import DEFAULT_PLOTLY_COLORS
from dash.dependencies import Input, Output


def strip_percent(x):
    try:
        return int(x.strip("%"))
    except:
        return None


def count_grads(x):
    num_grad = x[x.isin(["Graduate", "Doctorate", "Post Graduate", "Professional Graduate"])].count()
    return  float(num_grad)/ x.count() * 100.0


df_2014 = pd.read_csv("mp_track_2014.csv", delimiter='\t', converters={"Attendance": strip_percent})
df_2009 = pd.read_csv("mp_track_2009.csv", delimiter='\t', converters={"Attendance": strip_percent})

party_list = set(df_2014["Political party"].unique().tolist() + df_2009["Political party"].unique().tolist())

aggregations = OrderedDict([
    ("ID", "count"),
    ("Educational qualifications", count_grads),
    ("Age", "median"),
    ("Attendance", "mean"),
    ("Debates", "median"),
    ("Questions", "median")
])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    style={"width": "100%", "height": "100%"},
    children=[
        html.H1(children='Compare Political Parties'),
        # data div
        html.Div(
            style={"width": "50%", "margin-left": "25%", "height": "700px"},
            children=[
                dcc.Graph(id='compare-member-by-year', style={'height': '700px'})
            ]
        ),
        dcc.Dropdown(
            id='parties',
            options=[{'label': opt, 'value': opt} for opt in party_list],
            value=['Indian National Congress', 'Bharatiya Janata Party'],
            multi=True,
            style={"width": "50%"}
        ),
    ]
)


@app.callback(
    Output('compare-member-by-year', 'figure'),
    [Input('parties', 'value')])
def update_member(parties):
    if not parties:
        return []
    dff_2014 = df_2014[df_2014["Political party"].isin(parties)]
    dff_2009 = df_2009[df_2009["Political party"].isin(parties)]

    fig = tools.make_subplots(rows=2, cols=3, subplot_titles=["No of members",
                                                              "% members with bachelor+ degree",
                                                              "Median Age",
                                                              "Mean Attendance",
                                                              "Median Debates Participated", "Median Questions Asked"
                                                              ])
    df_group_2014 = dff_2014.groupby("Political party").agg(aggregations)
    df_group_2009 = dff_2009.groupby("Political party").agg(aggregations)

    for i, attr in enumerate(aggregations.keys()):
        x = i / 3 + 1
        y = i % 3 + 1
        for j, party in enumerate(parties):
            fig.append_trace(
                go.Bar(
                    y=[df_group_2009.loc[party, attr], df_group_2014.loc[party, attr]],
                    x=["2009", "2014"],
                    name=party,
                    legendgroup=party,
                    showlegend=True if i == 0 else False,
                    marker=go.bar.Marker(color=DEFAULT_PLOTLY_COLORS[j]),
                ), x, y)
        fig['layout']["xaxis{}".format(i + 1)]['type'] = "category"
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
