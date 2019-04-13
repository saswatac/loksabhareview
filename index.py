import os

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import redirect

import base_app
import compare_members_app
import compare_party_app
import participation_app
from base_app import app, server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    base_app.base_layout
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
    else:
        return [], "Welcome to the Lok Sabha Review!"


@server.route('/')
def hello():
    print "Base"
    return redirect("apps/compare_party", 303)


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0')
