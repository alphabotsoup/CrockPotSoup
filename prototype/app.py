import dash
import dash_core_components as dcc
import dash_html_components as html
import csv
from base64 import b64decode
from dash.dependencies import Input, Output
from textblob import TextBlob
import plotly.graph_objs as go


# Init Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(id="header"),
    html.H1('AlphabotSoup'),

    # dcc.Input(id='my-id', value='initial value', type='text'),
    # html.Div(id='my-div'),

    # Create a textbox
    dcc.Textarea(id='my-id2'),
    html.Div(id='my-div2'),

    dcc.Upload(
        html.Button('Upload'),
        id='input-box'
    ),
    html.Div(id='output-box'),

    # Create a graph
    dcc.Graph(id='my-graph')

])

# Populate "my-div" with tokenized values from the text box
# @app.callback(
#     Output(component_id='my-div', component_property='children'),
#     [Input(component_id='my-id', component_property='value')]
# )
# def update_output_div(input_value):
#     new_value = TextBlob(input_value)
#     words = new_value.words
#     return 'Tokenized words: {}'.format(words)


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

# Populate graph "my-graph" with word frequency statistics
@app.callback(
    Output('my-graph', 'figure'),
    [Input('my-id2', 'value')]
)
def update_graph(new_text):
    # Turn value from TextArea into a TextBlob object
    if new_text is not None:
        blob = TextBlob(str(new_text))
    else:
        blob = TextBlob('')
    # Tokenize words and lowercase
    tokenized_word = blob.words.lower()

    word_list = []
    word_frequency = []
    word_length = []
    word_dict_list = []

    # Turn word list into set to remove duplicates
    word_set = set(tokenized_word)

    # Turn set object into list to allow for graph processing
    for obj in word_set:
        word_dict = {
            'word': obj.lower(),
            'frequency': blob.word_counts[obj.lower()],
            'length': str(len(obj))
        }

        word_dict_list.append(word_dict)

        word_list.append(obj.lower())
        word_frequency.append(blob.word_counts[obj.lower()])
        word_length.append(len(obj))

    # Initialize scatter plot list
    traces = []

    # Add words from word list into Scatter plot dynamically
    for w in word_list:
        traces.append(go.Scatter(
            x=word_list,
            y=word_frequency,
            text=word_length,
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 1, 'color': 'white'},
                'color': 'red'
            },
            name=w

        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'category', 'title':'Unique Words'},
            yaxis={'type': 'linear', 'title': 'Word Frequency', 'range': [0, len(word_list) + 10]},
            # legend={'x': -1, 'y': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
