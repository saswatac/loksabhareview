import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import compare_members_app
import compare_party_app
import participation_app
import base_app
from base_app import app


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    base_app.nav,
    base_app.base_layout
])


@app.callback(
    [Output('left-sidebar', 'children'),
     Output('main-content', 'children')],
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/compare_members_app':
        return compare_members_app.left_controls, compare_members_app.main_content
    elif pathname == '/apps/compare_participation_app':
        return participation_app.left_controls, participation_app.main_content
    elif pathname == '/apps/compare_party_app':
        return compare_party_app.left_controls, compare_party_app.main_content
    else:
        return [], "Welcome to the Lok Sabha Review!"


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
