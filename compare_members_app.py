import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from plotly.colors import DEFAULT_PLOTLY_COLORS

from base_app import app, df_2014, df_2009

CONSTITUENCY = sorted(df_2014["Constituency"].dropna())
attribs = ["Debates", "Private Member Bills", "Questions", "Attendance"]
ids = ["member-metric-graph-{}".format(i) for i in range(4)]

left_controls = dcc.Dropdown(
    id='constituency',
    options=[
        {'label': constituency, 'value': constituency}
        for constituency in CONSTITUENCY
    ],
    placeholder="Select a constituency",
    value=CONSTITUENCY[0]
)

main_content = [
    dcc.Markdown(id="title", dangerously_allow_html=True),
    html.Div(className="row", children=[
        html.Div(dcc.Graph(id=i), className="col-sm-6")
        for i in ids[0:2]
    ]),
    html.Div(className="row", children=[
        html.Div(dcc.Graph(id=i), className="col-sm-6")
        for i in ids[2:]
    ])
]


@app.callback(
    [Output(i, 'figure') for i in ids] + [Output("title", 'children')],
    [Input('constituency', 'value')])
def update_member(constituency_name):
    if not constituency_name:
        return [[] for x in ids]
    data_2014 = df_2014[df_2014.Constituency == constituency_name].iloc[0]
    data_2009 = df_2009[df_2009.Constituency == constituency_name].iloc[0]

    figs = []
    for attr in attribs:
        fig = {
            "data": [go.Bar(
                x=["2009", "2014"],
                y=[data_2009[attr], data_2014[attr]],
                marker=go.bar.Marker(color=DEFAULT_PLOTLY_COLORS[:2]),
                width=[0.4, 0.4],
                name=attr,
                text=["{} ({})".format(data_2009["MP Name"], data_2009["Political party"]),
                      "{} ({})".format(data_2014["MP Name"], data_2014["Political party"])]
            )],
            "layout": {
                "xaxis": {
                    "type": "category"
                },
                "title": attr,
                "height": "350"
            }
        }
        figs.append(fig)
    title = "##### 2009: {} ({})\n".format(data_2009["MP Name"], data_2009["Political party"]) + \
            "##### 2014: {} ({})\n".format(data_2014["MP Name"], data_2014["Political party"])
    return figs + [title]
