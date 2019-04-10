import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

df_2014 = pd.read_csv("mp_track_2014.csv", delimiter='\t')
df_2009 = pd.read_csv("mp_track_2009.csv", delimiter='\t')

color_options = ["Gender", "Educational qualifications", "Political party"]
color_option_filters = {option: df_2014[option].unique() for option in color_options}
political_party_default = ["Indian National Congress", "Bharatiya Janata Party"]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1(children='Participation Trends'),
        dcc.Graph(id='scatter-plot'),
        dcc.Dropdown(
            id='year',
            options=[{"label": "2014", "value": "2014"}, {"label": "2009", "value": "2009"}],
            value="2014",
            placeholder="Select a year",
            style={"width": "50%"}
        ),
        dcc.Dropdown(
            id='x-metric',
            options=[{"label": "Attendance", "value": "Attendance"}, {"label": "Age", "value": "Age"}],
            value="Attendance",
            placeholder="Select a metric for x axis",
            style={"width": "50%"}
        ),
        dcc.Dropdown(
            id='y-metric',
            options=[{"label": "Questions", "value": "Questions"},
                     {"label": "Debates", "value": "Debates"},
                     {"label": "Private Member Bills", "value": "Private Member Bills"}],
            value="Questions",
            placeholder="Select a metric for y axis",
            style={"width": "50%"}
        ),
        dcc.Dropdown(
            id='color-metric',
            options=[{"label": "Gender", "value": "Gender"},
                     {"label": "Educational qualifications", "value": "Educational qualifications"},
                     {"label": "Political party", "value": "Political party"}
                     ],
            value="Gender",
            placeholder="Select a metric for color",
            style={"width": "50%"}
        ),
        dcc.Dropdown(
            id='color-metric-values',
            options=[
                {'label': 'Male', 'value': 'Male'},
                {'label': 'Female', 'value': 'Female'},
            ],
            value=['Male', 'Female'],
            multi=True,
            style={"width": "50%"}
        ),
    ]
)


@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('year', 'value'),
     Input('x-metric', 'value'),
     Input('y-metric', 'value'),
     Input('color-metric', 'value'),
     Input('color-metric-values', 'value')])
def update_member(year, x_metric, y_metric, color_metric, color_metric_values):
    df = df_2014 if year == "2014" else df_2009
    figure = {
        'data': [
            go.Scatter(
                x=df[df[color_metric] == i][x_metric],
                y=df[df[color_metric] == i][y_metric],
                text=df[df[color_metric] == i]['MP Name'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in color_metric_values],
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
    values = political_party_default if color_metric == "Political party" else color_option_filters[color_metric]
    return [{"label": opt, "value": opt} for opt in color_option_filters[color_metric]], values


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
