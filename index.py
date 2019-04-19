import os

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import redirect

import compare_members_app
import compare_party_app
import participation_app
import region_trends_app
from base_app import app, server

base_layout = html.Div(
    className="container-fluid",
    children=[html.Div(className="row",
                       style={"margin-top": "20px"},
                       children=[
                           html.Div(id="left-sidebar", className="col-sm-3 bg-light sidebar"),
                           html.Div(id="main-content", className="col-sm-9")
                       ]
                       )
              ]
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    base_layout
])

with open(os.path.join(app._assets_folder, "index.html")) as f:
    app.index_string = f.read()


@app.callback(
    [Output('left-sidebar', 'children'),
     Output('main-content', 'children')],
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/compare_members':
        return compare_members_app.left_controls, compare_members_app.main_content
    elif pathname == '/apps/compare_participation':
        return participation_app.left_controls, participation_app.main_content
    elif pathname == '/apps/compare_party':
        return compare_party_app.left_controls, compare_party_app.main_content
    elif pathname == '/apps/compare_regions':
        return region_trends_app.left_controls, region_trends_app.main_content
    else:
        return [], "Welcome to Lok Sabha Review!"


@server.route('/')
def hello():
    return redirect("apps/compare_party", 303)


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0')
