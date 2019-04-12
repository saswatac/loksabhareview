from collections import OrderedDict

import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from plotly import tools
from plotly.colors import DEFAULT_PLOTLY_COLORS

from base_app import app, df_2014, df_2009


def count_grads(x):
    num_grad = x[x.isin(["Graduate", "Doctorate", "Post Graduate", "Professional Graduate"])].count()
    return float(num_grad) / x.count() * 100.0


party_list = set(df_2014["Political party"].unique().tolist() + df_2009["Political party"].unique().tolist())

aggregations = OrderedDict([
    ("ID", "count"),
    ("Educational qualifications", count_grads),
    ("Age", "median"),
    ("Attendance", "mean"),
    ("Debates", "median"),
    ("Questions", "median")
])

left_controls = dcc.Dropdown(
    id='parties',
    options=[{'label': opt, 'value': opt} for opt in party_list],
    value=['Indian National Congress', 'Bharatiya Janata Party'],
    multi=True,
)

main_content = dcc.Graph(id='compare-party-by-year', style={"height": "100%"})


@app.callback(
    Output('compare-party-by-year', 'figure'),
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
            data_y = []
            try:
                data_y.append(df_group_2009.loc[party, attr])
            except KeyError:
                data_y.append(None)
            try:
                data_y.append(df_group_2014.loc[party, attr])
            except KeyError:
                data_y.append(None)
            fig.append_trace(
                go.Bar(
                    y=data_y,
                    x=["2009", "2014"],
                    name=party,
                    legendgroup=party,
                    showlegend=True if i == 0 else False,
                    marker=go.bar.Marker(color=DEFAULT_PLOTLY_COLORS[j]),
                ), x, y)
        fig['layout']["xaxis{}".format(i + 1)]['type'] = "category"
    return fig
