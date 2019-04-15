from collections import OrderedDict

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from plotly.colors import DEFAULT_PLOTLY_COLORS

from base_app import app, df_2014, df_2009


def count_grads(x):
    num_grad = x[x.isin(["Graduate", "Doctorate", "Post Graduate", "Professional Graduate"])].count()
    return float(num_grad) / x.count() * 100.0


def short_name(party):
    words = party.split()
    if len(words) == 1:
        return party
    else:
        return ''.join([w[0] if w.isalnum() else w for w in words if w not in ('of', 'in')])


party_list = set(df_2014["Political party"].unique().tolist() + df_2009["Political party"].unique().tolist())

aggregations = OrderedDict([
    ("ID", "count"),
    ("Educational qualifications", count_grads),
    ("Age", "median"),
    ("Attendance", "mean"),
    ("Debates", "median"),
    ("Questions", "median")
])
ids = ["party-metric-graph-{}".format(i) for i in range(6)]
titles = ["No of members",
          "% members with bachelor+ degree",
          "Median Age of members",
          "Mean Attendance per member",
          "Median Debates Participated per member",
          "Median Questions Asked per member"
          ]

left_controls = dcc.Dropdown(
    id='parties',
    options=[{'label': opt, 'value': opt} for opt in party_list],
    value=['Indian National Congress', 'Bharatiya Janata Party'],
    multi=True,
)

main_content = dcc.Graph(id='compare-party-by-year')
main_content = [
    html.Div(className="row", children=[
        html.Div(dcc.Graph(id=i), className="col-sm-4")
        for i in ids[0:3]
    ]),
    html.Div(className="row", children=[
        html.Div(dcc.Graph(id=i), className="col-sm-4")
        for i in ids[3:]
    ])
]


@app.callback(
    [Output(x, 'figure') for x in ids],
    [Input('parties', 'value')])
def update_metrics(parties):
    if not parties:
        return [[] for x in ids]
    dff_2014 = df_2014[df_2014["Political party"].isin(parties)]
    dff_2009 = df_2009[df_2009["Political party"].isin(parties)]

    df_group_2014 = dff_2014.groupby("Political party").agg(aggregations)
    df_group_2009 = dff_2009.groupby("Political party").agg(aggregations)
    figs = []
    for i, attr in enumerate(aggregations.keys()):
        data = []
        for j, party in enumerate(parties):
            data_y = []
            try:
                data_y.append(df_group_2009.loc[party, attr])
            except KeyError:
                data_y.append(None)
            try:
                data_y.append(df_group_2014.loc[party, attr])
            except KeyError:
                data_y.append(None)
            data.append(go.Bar(
                y=data_y,
                x=["2009", "2014"],
                name=short_name(party),
                marker=go.bar.Marker(color=DEFAULT_PLOTLY_COLORS[j]),
            ))
        fig = {
            "data": data,
            "layout": {
                "xaxis": {
                    "type": "category"
                },
                "height": "350",
                "title": titles[i],
                "legend": dict(orientation="h")
            }
        }
        figs.append(fig)

    return figs
