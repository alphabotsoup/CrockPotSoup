#!/usr/bin/python3
from base64 import b64decode
import csv

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc


# Init
app = dash.Dash(__name__)

# Page layout
app.layout = html.Div([
    dcc.Upload(
        html.Button('Upload'),
        id='input-box'
    ),
    html.Div(id='output-box')
])


# Callbacks (functionality)
@app.callback(
    Output('output-box', 'children'),
    [Input('input-box', 'contents')]
)
def post_file(file_contents):
    """
    Basic routine to accept a file upload, decode it, and interpret it as CSV.
    Examples at: `dash.plot.ly/dash-core-components/upload`
    File contents come in the form of "content_type,content_string" and are Base 64 encoded.
    base64.b64decode() returns type 'bytes', which must then be decoded into Unicode.
    """
    if file_contents:
        file_contents = b64decode(file_contents.split(',')[1], validate=True).decode('utf-8')

        rows = []
        for line in csv.reader(iter(file_contents.splitlines())):
            rows.append(html.Tr([html.Td(col) for col in line]))
        return html.Table(rows)


# Debug mode when this script is invoked directly
if __name__ == '__main__':
    app.run_server(debug=True)
