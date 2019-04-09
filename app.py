import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

df_2014 = pd.read_csv("mp_track_2014.csv", delimiter='\t')
df_2009 = pd.read_csv("mp_track_2009.csv", delimiter='\t')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    style={"width": "100%"},
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
            style={"width": "80%", "margin-left": "10%"},
            children=[
                # Row container div
                html.Div(
                    style={"display": "flex"},
                    children=[
                        html.Div(
                            style={"width": "50%"},
                            children=[
                                html.H3(children='2014', style={"text-align": "center"}),
                                html.Div(id="name-2014", style={"text-align": "center"})
                            ]
                        ),
                        html.Div(
                            style={"flex-grow": 1, "width": "50%"},
                            children=[
                                html.H3(children='2009', style={"text-align": "center"}),
                                html.Div(id="name-2009", style={"text-align": "center"})
                            ]
                        ),
                    ]
                ),
                dcc.Graph(id='compare-member-by-year')
            ]
        )
    ]
)


@app.callback(
    [Output('name-2014', 'children'),
     Output('name-2009', 'children'),
     Output('compare-member-by-year', 'figure')],
    [Input('constituency', 'value')])
def update_member(constituency_name):
    if not constituency_name:
        return None, None, {"data": []}
    attributes = ["MP Name", "Political party", "Debates", "Private Member Bills", "Questions", "Attendance"]
    data_2014 = df_2014[df_2014.Constituency == constituency_name].get(attributes).values[0]
    data_2009 = df_2009[df_2009.Constituency == constituency_name].get(attributes).values[0]

    fig = {"data": [
        go.Bar(
            x=attributes[2:],
            y=data_2014[2:],
            name='2014',
            marker=go.bar.Marker(
                color='rgb(26, 118, 255)'
            )
        ),
        go.Bar(
            x=attributes[2:],
            y=data_2009[2:],
            name='2009',
            marker=go.bar.Marker(
                color='rgb(55, 83, 109)'
            )
        )
        ],
        "layout": go.Layout(
            showlegend=True,
            legend=go.layout.Legend(
                x=0,
                y=1.0
            ),
            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
        )
    }

    ret= "{} ({})".format(data_2014[0], data_2014[1]), "{} ({})".format(data_2009[0], data_2009[1]), fig
    print ret
    return ret

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
