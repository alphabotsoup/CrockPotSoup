import nltk
from nltk import *
from nltk.tree import *
import dash
import dash_core_components as dcc
import dash_html_components as html
import csv
from base64 import b64decode
from dash.dependencies import Input, Output, State
from textblob import TextBlob
import plotly.graph_objs as go
import plotly
import math
import plotly.plotly as py
import pandas as pd

# Init Dash
app = dash.Dash(__name__)


app.layout = html.Div([
    html.Div(id="header"),
    html.H1('AlphabotSoup'),

    # Create a textbox
    dcc.Textarea(id='my-id2'),
    html.Div(id='my-div-2'),
    html.Button(id='submit', type='submit', children='ok'),

    dcc.Upload(
        html.Button('Upload'),
        id='input-box'
    ),
    html.Div(id='output-box'),

    # Output sankey diagram
    dcc.Graph(id='sankey-graph'),

    # Create word frequency bar graph
    dcc.Graph(id='word-frequency'),

    # Create a graph
    dcc.Graph(id='my-graph'),



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

# Sankey graph
@app.callback(
    Output('sankey-graph', 'figure'), [Input('submit', 'n_clicks')],
           [State('my-id2', 'value')]
)
def update_sankey(n_clicks, new_text):
    # Turn value from TextArea into a TextBlob object
    if new_text is not None:
        blob = TextBlob(str(new_text).lower())
    else:
        blob = TextBlob('')

    tagged_words = blob.tags

    words_list = []

    # append words
    for i in tagged_words:
        words_list.append(i[0])

    # append tags
    for y in tagged_words:
        words_list.append(y[1])

    # create a dict with source (index of the word from the word list)
    source_dict = []
    target_dict = []
    word_count = []
    for i in words_list[0:len(words_list)//2]:
        source_dict.append(words_list.index(i))

    # create a dict with target (index of the pos tag from the word list
    for i in words_list[len(words_list)//2: len(words_list)]:
        target_dict.append(words_list.index(i))

    # create a dict with value (word frequency of word at index
    for i in words_list:
        word_count.append(1)


    data = dict(
        type='sankey',
        node=dict(
            pad=15,
            thickness=20,
            line=dict(
                color="black",
                width=0.5
            ),
            label=words_list,
            # color=["blue", "blue", "blue", "blue" "blue", "blue"]
        ),
        link=dict(
            source=source_dict,
            target= target_dict,
            value=word_count
        ))

    layout = dict(
        title = "Part Of Speech Mapping",
        font = dict(
            size = 10
        )
    )

    fig = dict(data=[data], layout=layout)
    return fig

# Populate graph "bar-graph" with word frequency statistics
@app.callback(
    Output('word-frequency', 'figure'), [Input('submit', 'n_clicks')],
    [State('my-id2', 'value')]
)
def update_bar_graph(n_clicks, new_text):
    # Turn value from TextArea into a TextBlob object
    if new_text is not None:
        blob = TextBlob(str(new_text).lower())
    else:
        blob = TextBlob('')
    # Tokenize words and lowercase
    tokenized_word = blob.words.lower() # remove this lower

    word_list = []
    word_frequency = []
    word_length = []
    word_tags = []
    word_dict = {}

    # Turn word list into set to remove duplicates
    word_set = set(tokenized_word)

    # Turn set object into list to allow for graph processing
    for obj in word_set:
        single_word_blob = TextBlob(obj)
        pos_tag = single_word_blob.tags

        word_list.append(obj.lower())
        word_frequency.append(blob.word_counts[obj.lower()])
        word_length.append(len(obj))
        word_tags.append(pos_tag[0][1])
        word_dict = {
            'Words': word_list,
            'Frequency': word_frequency,
            'Length': word_length,
            'Tags': word_tags
        }

    word_tags_set = set(word_tags)

    # Initialize scatter plot list
    traces = []

    # Add words from word list into Scatter plot dynamically
    for w in word_tags_set:
        traces = (go.Bar(
            x=word_dict['Words'],
            y=word_dict['Frequency'],
            name=w
        ))

    return {
        'data': [traces],
        'layout': go.Layout(
            title='Word Frequency',
            xaxis={'type': 'category', 'title': 'Unique Words'},
            yaxis={'type': 'linear', 'title': 'Word Frequency', 'range': [0, len(word_list) + 10]},
            barmode='group'
        )
    }

# Populate graph "my-graph" with word frequency statistics
@app.callback(
    # Output('my-graph', 'figure'),
    # [Input('my-id2', 'value')]
    Output('my-graph', 'figure'), [Input('submit', 'n_clicks')],
    [State('my-id2', 'value')]
)
def update_graph(n_clicks, new_text):
    # Turn value from TextArea into a TextBlob object
    if new_text is not None:
        blob = TextBlob(str(new_text).lower())
    else:
        blob = TextBlob('')
    # Tokenize words and lowercase
    tokenized_word = blob.words.lower() # remove this lower

    word_list = []
    word_frequency = []
    word_length = []
    word_tags = []
    word_tags2 = blob.tags
    word_dict = {}


    # Turn word list into set to remove duplicates
    word_set = set(tokenized_word)

    # Turn set object into list to allow for graph processing
    for obj in word_set:
        single_word_blob = TextBlob(obj)
        pos_tag = single_word_blob.tags

        word_dict = {
            str(obj): {
                "frequency": blob.word_counts[obj.lower()],
                "length": len(obj),
                "pos": pos_tag[0][1]
            }
        }

        word_list.append(obj.lower())
        word_frequency.append(blob.word_counts[obj.lower()])
        word_length.append(len(obj))
        word_tags.append(pos_tag[0][1])


    # Initialize scatter plot list
    traces = []
    traces2 = []
    word_tag_set = set(word_tags)
    for tag in word_tag_set:
        traces2.append(tag)

    # Add words from word list into Scatter plot dynamically
    # for w in word_tag_set:
    for t in traces2:
        traces.append(go.Scatter(
            x=word_list,
            y=word_frequency,
            text=word_tags,
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 1, 'color': 'white'}
            },
            name=t
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'category', 'title':'Unique Words'},
            yaxis={'type': 'linear', 'title': 'Word Frequency', 'range': [0, len(word_list) + 10]},
            legend={'x': -1, 'y': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
