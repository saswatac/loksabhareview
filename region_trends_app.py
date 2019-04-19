import dash_core_components as dcc
import plotly
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from base_app import app

mapbox_access_token = "pk.eyJ1Ijoic2Fzd2F0YWMiLCJhIjoiY2p1bDR4Nm1vMDByOTN5bXVmOG1pYXB4dyJ9.y9jbd2V_NpUV1UHkl5x3Lw"

left_controls = [dcc.Dropdown(
    id='region-metric',
    options=[{"label": "Questions Asked", "value": "Questions"}, {"label": "Debates Participated", "value": "Debates"}],
    value="Questions",
    placeholder="Select a metric",
)]

main_content = dcc.Graph(id='india-map', style={"height": "70vh"})

colorscale = plotly.colors.n_colors('rgb(0,32,76)', 'rgb(255,233,69)', 7, colortype='rgb')
colorscale.reverse()

question_bucket = [10, 50, 100, 200, 400, 600]
debate_bucket = [10, 30, 60, 90, 120, 150]

question_sources = "https://s3-eu-west-1.amazonaws.com/lok-sabha-geo/geo_data_questions_{}.geojson"
debate_sources = "https://s3-eu-west-1.amazonaws.com/lok-sabha-geo/geo_data_debates_{}.geojson"


@app.callback(
    Output('india-map', 'figure'),
    [Input('region-metric', 'value')])
def get_map_data(region_metric):
    if not region_metric:
        return []
    if region_metric == 'Questions':
        bucket = question_bucket
        sources = question_sources
        title = "Number of questions asked"
    else:
        bucket = debate_bucket
        sources = debate_sources
        title = "Number of debates participated"

    data = [
        go.Scattermapbox(
            lat=['45.5017'],
            lon=['-73.5673'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                color=colorscale[i]
            ),
            name="<{}".format(bucket[i]) if i == 0 else ">{}".format(bucket[i-1]) if i == 6 else "{}-{}".format(
                bucket[i - 1], bucket[i])
        )
        for i in range(7)
    ]
    layout = go.Layout(
        height=600,
        autosize=True,
        legend=dict(orientation="h"),
        title=title,
        hovermode='closest',
        mapbox=dict(
            layers=[
                dict(
                    sourcetype='geojson',
                    source=sources.format(i),
                    type='fill',
                    color=colorscale[i]
                ) for i in range(7)
            ],
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=23,
                lon=82.5
            ),
            pitch=0,
            zoom=3.0,
            style='light'
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    fig = dict(data=data, layout=layout)
    return fig
