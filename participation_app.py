import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly
from base_app import app, df_2009, df_2014

color_options = ["Gender", "Educational qualifications", "Political party", "Number of terms"]
color_option_filters = {option: df_2014[option].unique() for option in color_options}
political_party_default = ["Indian National Congress", "Bharatiya Janata Party"]

term_order = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eight", "Ninth"]

left_controls = [
    dcc.Dropdown(
        id='year',
        options=[{"label": "2014", "value": "2014"}, {"label": "2009", "value": "2009"}],
        value="2014",
        placeholder="Select a year",
    ),
    dcc.Dropdown(
        id='x-metric',
        options=[{"label": "Attendance", "value": "Attendance"},
                 {"label": "Age", "value": "Age"}],
        value="Attendance",
        placeholder="Select a metric for x axis",
    ),
    dcc.Dropdown(
        id='y-metric',
        options=[{"label": "Questions", "value": "Questions"},
                 {"label": "Debates", "value": "Debates"},
                 {"label": "Private Member Bills", "value": "Private Member Bills"}],
        value="Questions",
        placeholder="Select a metric for y axis",
    ),
    dcc.Dropdown(
        id='color-metric',
        options=[{"label": opt, "value": opt} for opt in color_options],
        value="Gender",
        placeholder="Select a metric for color",
    ),
    dcc.Dropdown(
        id='color-metric-values',
        options=[
            {'label': 'Male', 'value': 'Male'},
            {'label': 'Female', 'value': 'Female'},
        ],
        value=['Male', 'Female'],
        multi=True,
    ),
]

main_content = dcc.Graph(id='scatter-plot')


@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('year', 'value'),
     Input('x-metric', 'value'),
     Input('y-metric', 'value'),
     Input('color-metric', 'value'),
     Input('color-metric-values', 'value')])
def update_participation_graph(year, x_metric, y_metric, color_metric, color_metric_values):
    if not all([year, x_metric, y_metric, color_metric]):
        return []
    df = df_2014 if year == "2014" else df_2009
    colors = None
    if color_metric == 'Number of terms':
        color_metric_values = [term for term in term_order if term in color_metric_values]
        colors = plotly.colors.n_colors('rgb(0,32,76)', 'rgb(255,233,69)', len(color_metric_values),
                                        colortype='rgb')
        colors.reverse()
    data = []
    for i, color_metric_value in enumerate(color_metric_values):
        marker = {
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'},
        }
        if colors:
            marker['color'] = colors[i]
        data.append(go.Scatter(
            x=df[df[color_metric] == color_metric_value][x_metric],
            y=df[df[color_metric] == color_metric_value][y_metric],
            text=df[df[color_metric] == color_metric_value]['MP Name'],
            mode='markers',
            opacity=0.7,
            marker=marker,
            name=color_metric_value
        ))
    figure = {
        'data': data,
        'layout': go.Layout(
            xaxis={'title': x_metric},
            yaxis={'title': y_metric},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }
    return figure


@app.callback(
    [Output('color-metric-values', 'options'),
     Output('color-metric-values', 'value')],
    [Input('color-metric', 'value')])
def set_color_metric_values(color_metric):
    if not color_metric:
        return [], []
    values = political_party_default if color_metric == "Political party" else color_option_filters[color_metric]
    return [{"label": opt, "value": opt} for opt in color_option_filters[color_metric]], values
