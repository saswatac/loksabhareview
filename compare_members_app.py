import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from plotly import tools
from plotly.colors import DEFAULT_PLOTLY_COLORS


from base_app import app, df_2014, df_2009

CONSTITUENCY = sorted(df_2014["Constituency"].dropna())

left_controls = dcc.Dropdown(
    id='constituency',
    options=[
        {'label': constituency, 'value': constituency}
        for constituency in CONSTITUENCY
    ],
    placeholder="Select a constituency",
    value=CONSTITUENCY[0]
)

main_content = dcc.Graph(id='compare-member-by-year', style={"height": "100%"})


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
                x=["2009", "2014"],
                y=[data_2009[attr], data_2014[attr]],
                marker=go.bar.Marker(color=DEFAULT_PLOTLY_COLORS[:2]),
                width=[0.4, 0.4],
                name=attr
            ), x, y)
    fig['layout']['shapes'] = shapes
    for i in range(1, 5):
        fig['layout']["xaxis{}".format(i)]['type'] = "category"
    fig['layout']['xaxis3']['automargin'] = True
    fig['layout']['margin'] = {"b": 200}
    fig['layout']['showlegend'] = False
    fig['layout']['title'] = {"text": "2009: {} ({}) <br> Vs <br> 2014: {} ({})".format(
        data_2009["MP Name"],
        data_2009["Political party"],
        data_2014["MP Name"],
        data_2014["Political party"]),
        "font": {
            "size": 24,
        },
        "y": 0.2
    }
    return fig
