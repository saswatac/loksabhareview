import dash
import pandas as pd
import dash_bootstrap_components as dbc

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
