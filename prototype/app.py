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
import math
import statistics


# Init Dash
app = dash.Dash('AlphabotSoup')
app.config['suppress_callback_exceptions']=True

# Bootstrap css

app.layout = html.Div([
    # create header row div
    html.Header(
     html.Div([
      html.Div([
          html.Div([
              html.Div([
                  html.H1('AlphabotSoup'),
              ], className="col-md-6", style={"margin-left": "0px","text-align": "left", "padding-right": "15px"}),
          ], className="row")
      ], className="container")
     ], className="header-dark")
    ),

    # create input row div
    html.Div([
        html.Div([
            # Create a textbox
            html.H4('Enter your text here'),
            dcc.Textarea(id='text', rows='12', cols='50', value='This is a test. This is only a test.'),
                html.Div([
                html.Button(id='submit', type='submit', children='ok'),

                dcc.Upload(
                html.Button('Upload'),
                id='input-box'),
                html.Div(id='output-box')
            ]),
        ], className="col-md-6"),

        html.Div([
            html.Div([
                html.H3('Introduction:'),
                html.P('AlphabotSoup is an educational exploration in the power '
                       'of natural language processing. To get started, upload a '
                       'text file or type in the textbox to see the magic happen.')
            ], id="Introduction"),
        ], className="col-md-6"),

    ], className="row"),

    dcc.Loading(id="loading-top-1",
        children=[html.Div([
            # create total word count tile
            html.Div([

            ],id='word-count', className="col-md-4"),

            # create total unique word count tile
            html.Div([

            ], id='unique-words', className="col-md-4"),

            # create word complexity score
            html.Div([

            ], id='word-complexity', className="col-md-4")
        ], className="row")
    ]),

    # create row
    dcc.Loading(id="loading-bottom-1",
                children=[html.Div([

                    # create pie div
                    html.Div([
                        html.Div([
                            # Output pie chart
                            dcc.Graph(id='pie-chart')
                        ], className="col-md-12"),
                    ], className="row"),

                    # create row
                    html.Div([
                        html.Div([
                            # Create word frequency bar graph
                            dcc.Graph(id='word-frequency'),
                        ], className="col-md-12"),
                        # create sankey div
                        html.Div([
                            # Output sankey diagram
                            dcc.Graph(id='sankey-graph')
                        ], className="col-md-12")
                    ], className="row", style={'padding-top': '15px'}),

                    # create hidden div for data processing
                    html.Div(id='intermediate-value', hidden=True, children=dcc.Input(id="hidden-input"))])
    ]),

])


@app.callback(Output('intermediate-value', 'value'),  [Input('submit', 'n_clicks')],
              [State('text', 'value')]
)
def jsonify_data(n_clicks, new_text):
    # Take text and remove unwanted values
    new_text = str(new_text)
    new_text = new_text.replace(",", "")
    new_text = new_text.replace("'", "")
    new_text = new_text.replace("...", "")
    new_text = new_text.replace("-", "")
    new_text = new_text.replace("`", "")


    # Turn value from TextArea into a TextBlob object
    if new_text is not None:
        blob = TextBlob(str(new_text).lower())
    else:
        blob = TextBlob('')

    tokenized_word = blob.words.lower()  # remove this lower
    tagged_words = blob.tags

    word_list = []
    word_frequency = []
    word_length = []
    unique_tags = []

    words_list = []
    tags_list = []
    tag_frequency = []
    pie_chart_words_list = []

    # append words to pie_chart_words_list
    for i in tagged_words:
        pie_chart_words_list.append(i[1])


    # append words
    for i in tagged_words:
        words_list.append(i[0])

    # append tags
    for y in tagged_words:
        words_list.append(y[1])


    # append tags
    for y in tagged_words:
        tags_list.append(y[1])

    # append percentage of pos
    for x in pie_chart_words_list:
        tag_frequency.append(1)

    # Turn word list into set to remove duplicates
    word_set = set(tokenized_word)

    # Turn set object into list to allow for graph processing
    for obj in word_set:
        single_word_blob = TextBlob(obj)
        pos_tag = single_word_blob.tags

        word_list.append(obj.lower())
        word_frequency.append(blob.word_counts[obj.lower()])
        word_length.append(len(obj))
        unique_tags.append(pos_tag[0][1])

    word_length.sort()

    # create a dict with source (index of the word from the word list)
    source_dict = []
    target_dict = []
    word_count = []
    for i in words_list[0:len(words_list) // 2]:
        source_dict.append(words_list.index(i))

    # create a dict with target (index of the pos tag from the word list
    for i in words_list[len(words_list) // 2: len(words_list)]:
        target_dict.append(words_list.index(i))

    # create a dict with value (word frequency of word at index
    for i in words_list:
        word_count.append(1)

    # create dictionary
    word_dict = {'word_list': word_list,
                 'word_frequency': word_frequency,
                 'word_length': word_length,
                 'unique_tags': unique_tags,
                 'tags_list': tags_list,
                 'tag_frequency': tag_frequency,
                 'words_list': words_list,
                 'word_count': word_count,
                 'source_dict': source_dict,
                 'target_dict': target_dict,
                 }

    return word_dict

@app.callback(
    Output('word-count', 'children'), [Input('intermediate-value', 'value')],
    [State('intermediate-value', 'value')]
)
def update_word_count(value, word_dict):
    total = 0
    for w in word_dict['word_frequency']:
        total = total + w
    return html.Div([html.H1(total),
                     html.H3("Word Total")
                     ], className="tile")

@app.callback(
    Output('unique-words', 'children'), [Input('intermediate-value', 'value')],
    [State('intermediate-value', 'value')]
)
def update_unique_count(value, word_dict):
    return html.Div([html.H1(len(word_dict['word_frequency'])),
                     html.H3("Unique Word Total")
                     ], className="tile")


@app.callback(
    Output('word-complexity', 'children'), [Input('intermediate-value', 'value')],
    [State('intermediate-value', 'value')]
)
def update_word_count(value, word_dict):
    complexity=0
    total = 0
    for w in word_dict['word_frequency']:
        total = total + w

    # word_dict['word_length'].sort()
    if len(word_dict['word_length']) > 0:
        # average = round((word_dict['word_length'][0] + word_dict['word_length'][-1])/2,2)
        average = round(statistics.mean(word_dict['word_length']),2)
    else:
        average = 0

    return html.Div([html.H1(average),
                     html.H3("Average Word Length")
                     ], className="tile")


@app.callback(
    Output('text', 'value'),
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

        return file_contents


# Pie chart
@app.callback(Output('pie-chart', 'figure'), [Input('intermediate-value', 'value')],
    [State('intermediate-value', 'value')]
)
def update_pie(n_clicks, word_dict):
    layout = go.Layout(
        title="Part Of Speech Breakdown",
        legend=dict(orientation="h")
    )

    trace = go.Pie(
        labels=word_dict['tags_list'],
        values=word_dict['tag_frequency'],
    )

    return {"data": [trace], "layout": layout}


# Sankey graph
@app.callback(Output('sankey-graph', 'figure'), [Input('intermediate-value', 'value')],
    [State('intermediate-value', 'value')]
)
def update_sankey(n_clicks, word_dict):
    if len(word_dict['word_list']) <= 10:
        size = 450
    else:
        size = len(word_dict['word_list']) * 15

    data = dict(
        type='sankey',
        node=dict(
            pad=15,
            thickness=20,
            line=dict(
                color="black",
                width=0.5
            ),
            label=word_dict['words_list'],
        ),
        link=dict(
            source=word_dict['source_dict'],
            target=word_dict['target_dict'],
            value=word_dict['word_count']
        ))

    layout = dict(
        autosize=True,
        height=size,
        title="Part Of Speech Mapping"
    )

    fig = dict(data=[data], layout=layout)
    return fig

# Populate graph "bar-graph" with word frequency statistics
@app.callback(Output('word-frequency', 'figure'), [Input('intermediate-value', 'value')],
    [State('intermediate-value', 'value')]
)
def update_bar_graph(n_clicks, word_dict):
    word_tags_set = set(word_dict['unique_tags'])

    # Initialize scatter plot list
    traces = []

    # Add words from word list into Scatter plot dynamically
    for w in word_tags_set:
        traces = (go.Bar(
            x=word_dict['word_list'],
            y=word_dict['word_frequency'],
            name=w
        ))

    return {
        'data': [traces],
        'layout': go.Layout(
            title='Word Frequency',
            xaxis={'type': 'category', 'title': 'Unique Words'},
            yaxis={'type': 'linear', 'title': 'Word Frequency', 'range': [0, int(math.ceil(max(word_dict['word_frequency'])/10.0)) * 10]},
            barmode='group'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=False)
