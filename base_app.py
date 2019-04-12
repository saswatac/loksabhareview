import dash
import pandas as pd
import dash_html_components as html

external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    },
]
external_scripts = ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)
server = app.server
app.config.suppress_callback_exceptions = True


# Load the datasets in memory

def strip_percent(x):
    try:
        return int(x.strip("%"))
    except:
        return None


df_2014 = pd.read_csv("mp_track_2014.csv", delimiter='\t', converters={"Attendance": strip_percent})
df_2009 = pd.read_csv("mp_track_2009.csv", delimiter='\t', converters={"Attendance": strip_percent})

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

base_layout = html.Div(
    className="container-fluid",
    children=[html.Div(className="row",
                       style={"margin-top": "20px"},
                       children=[
                           html.Div(id="left-sidebar", className="col-3"),
                           html.Div(id="main-content", className="col-9", style={"height": "700px"})
                       ]
            )]
)