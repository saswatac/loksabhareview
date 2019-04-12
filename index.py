import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import compare_members_app
import compare_party_app
import participation_app
from base_app import app

nav = html.Nav(
    # className="navbar navbar-expand-lg navbar-dark bg-dark fixed-top",
    className="navbar navbar-expand-lg navbar-dark sticky-top bg-dark flex-md-nowrap p-0",
    children=[
        html.A(
            # className="navbar-brand ",
            className="navbar-brand col-3  mr-0",
            children="The Lok Sabha Review",
            href="/"),
        # html.Button(
        #     className="navbar-toggler",
        #     type="button",
        #     children=html.Span(className="navbar-toggler-icon"),
        #     **{
        #         "data-toggle": "collapse",
        #         "data-target": "#navbarSupportedContent",
        #         "aria-controls": "navbarSupportedContent",
        #         "aria-expanded": "false",
        #         "aria-label": "Toggle navigation"
        #     }
        # ),
        html.Div(
            className="navbar-nav col",
            children=[
                html.A("Compare Members", className="nav-item nav-link", href="/apps/compare_members_app"),
                html.A("Compare Political Parties", className="nav-item nav-link",
                       href="/apps/compare_party_app"),
                html.A("Participation Trends", className="nav-item, nav-link",
                       href="/apps/compare_participation_app")
            ]
        )

    ])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content')
])


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/compare_members_app':
        return compare_members_app.layout
    elif pathname == '/apps/compare_participation_app':
        return participation_app.layout
    elif pathname == '/apps/compare_party_app':
        return compare_party_app.layout
    else:
        return "Welcome to the Lok Sabha Review!"


# @app.callback([Output('item-1', 'active'),
#                Output('item-2', 'active'),
#                Output('item-3', 'active'),
#                Output('item-4', 'active')],
#               [Input('url', 'pathname')])
# def update_active_menu(pathname):
#     if pathname == '/apps/compare_members_app':
#         return False, True, False, False
#     elif pathname == '/apps/participation_app':
#         return False, False, True, False
#     elif pathname == '/apps/compare_party_app':
#         return False, False, False, True
#     else:
#         return True, False, False, False


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
