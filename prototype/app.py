import dash
import dash_core_components as dcc
import dash_html_components as html
import csv
from base64 import b64decode
from dash.dependencies import Input, Output, State
from textblob import TextBlob
import plotly.graph_objs as go



# Init Dash
app = dash.Dash('AlphabotSoup')

params = [
    'Word', 'DefinitionList'
]

# Bootstrap css

app.layout = html.Div([
    # create header row div
    html.Header(
     html.Div([
      html.Div([
          html.Div([
              html.Div([
                  html.H1('AlphabotSoup'),
              ], className="col-md-6"),
              # html.Div([
              #     html.P('Explore natural language processing.')
              # ], className="col-md-6"),
          ], className="row")
      ], className="container")
     ], style={'background': 'black', 'color': 'white', 'height': '100px', 'padding-top': '15px'})
    ),

    # create input row div
    html.Div([
        html.Div([
            # Create a textbox
            html.H4('Enter your text here'),
            dcc.Textarea(id='my-id2', rows='12', cols='50', value='This is a test. This is only a test.'),
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
                html.P('AlphabotSoup is an educational exploration in the power'
                       'of natural language processing. To get started, upload a '
                       'text file or type in the textbox to see the magic happen.')
            ], id="Introduction"),
        ], className="col-md-6"),

    ], className="row"),

    # create row
    html.Div([
        # create sankey div
        html.Div([
            # Output sankey diagram
            dcc.Graph(id='sankey-graph')
        ], className="col-md-6"),
        html.Div([
            # Create word frequency bar graph
            dcc.Graph(id='word-frequency'),
        ], className="col-md-6")
    ], className="row", style={'padding-top': '15px'}),

    # create row
    html.Div([
        # create pie div
        html.Div([
            # Output pie chart
            dcc.Graph(id='pie-chart')
        ], className="col-md-6"),
        html.Div([
            # Create definition sankey here
            dcc.Graph(id='length-graph'),
        ], className="col-md-6")
        # html.Div([
        # #     # Create word frequency bar graph
        #     dcc.Graph(id='something-something-else'),
        # ], className="col-md-4")
    ], className="row")
])


@app.callback(
    Output('length-graph', 'figure'), [Input('submit', 'n_clicks')],
    [State('my-id2', 'value')]
)
def update_length(n_clicks, new_text):
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

    word_length.sort()


    # Initialize scatter plot list
    traces = []
    traces2 = []
    word_tag_set = set(word_tags)
    for tag in word_tag_set:
        traces2.append(tag)

    # Add words from word list into Scatter plot dynamically
    # for w in word_tag_set:
    for t in word_list:
        traces.append(go.Scatter(
            x=word_length,
            y=word_frequency,
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 1, 'color': 'white'}
            }
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            title="Word Diversity",
            xaxis={'type': 'category', 'title':'Word Length'},
            yaxis={'type': 'linear', 'title': 'Word Frequency', 'range': [0, len(word_list) + 10]},
            showlegend=False,
            hovermode='closest'
        )
    }

# Callbacks (functionality)
@app.callback(
    # Output('output-box', 'children'),
    Output('my-id2', 'value'),
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
        # return html.Table(rows)

# Definition table
# @app.callback(
#     Output('definition-table', 'children'), [Input('submit', 'n_clicks')],
#         [State('my-id2', 'value')]
# )
# def update_definition(n_clicks, new_text):
#     # Turn value from TextArea into a TextBlob object
#     if new_text is not None:
#         blob = TextBlob(str(new_text).lower())
#     else:
#         blob = TextBlob('')
#
#     tokenized = blob.words.lower()
#
#     cols = ['Word', 'DefinitionList']
#     rows = []
#     defs = []
#     new_rows = []
#
#
#     for i in set(tokenized):
#         rows.append((i, Word(i).definitions))
#     for i in tokenized:
#         if Word(i).definitions is not []:
#             defs.append(Word(i).definitions)
#
#
#     for i in rows:
#         new_rows.append(html.Tr([html.Td(col) for col in rows]))
#
#     return html.Table(
#         # Header
#         [html.Th(col) for col in cols]
#         +
#         #Body
#         [html.Tr(
#             [html.Td(row[0]) for row[0] in rows]
#             +
#             [html.Td(row[1]) for row[1] in rows]
#         )]
#
#     )


# Pie chart
@app.callback(
    Output('pie-chart', 'figure'), [Input('submit', 'n_clicks')],
        [State('my-id2', 'value')]
)
def update_pie(n_clicks, new_text):
    # Turn value from TextArea into a TextBlob object
    if new_text is not None:
        blob = TextBlob(str(new_text).lower())
    else:
        blob = TextBlob('')

    tagged_words = blob.tags

    words_list = []
    tags_list = []
    tag_frequency = []

    # append words
    for i in tagged_words:
        words_list.append(i[0])

    # append tags
    for y in tagged_words:
        tags_list.append(y[1])

    temp_list = tags_list
    # append percentage of pos
    for x in words_list:
        tag_frequency.append(1)



    layout = go.Layout(
        title="Part Of Speech Breakdown",
        # margin=dict(l=0, r=0, b=0, t=4, pad=8),
        legend=dict(orientation="h")
        # paper_bgcolor="white",
        # plot_bgcolor="white",
    )

    trace = go.Pie(
        labels=tags_list,
        values=tag_frequency,
        # marker={"colors": ["#264e86", "#0074e4", "#74dbef", "#eff0f4"]},
    )

    return {"data": [trace], "layout": layout}


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
        title = "Part Of Speech Mapping"
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


if __name__ == '__main__':
    app.run_server(debug=True)
