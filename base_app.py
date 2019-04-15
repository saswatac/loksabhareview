import dash
import pandas as pd
import dash_html_components as html
import flask

external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]
external_scripts = ['https://code.jquery.com/jquery-3.2.1.slim.min.js',
                    'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js']

server = flask.Flask(__name__)
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                external_scripts=external_scripts,
                server=server,
                url_base_pathname='/apps/')
app.config.suppress_callback_exceptions = True


# Load the datasets in memory

def strip_percent(x):
    try:
        return int(x.strip("%"))
    except:
        return None


df_2014 = pd.read_csv("mp_track_2014.csv", delimiter='\t', converters={"Attendance": strip_percent})
df_2009 = pd.read_csv("mp_track_2009.csv", delimiter='\t', converters={"Attendance": strip_percent})

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
