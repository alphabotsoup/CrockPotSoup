import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from textblob import TextBlob
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div'),

    dcc.Textarea(id='my-id2'),
    html.Div(id='my-div2'),


    dcc.Graph(id='my-graph')
])


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    new_value = TextBlob(input_value)
    words = new_value.words
    return 'Tokenized words: {}'.format(words)



@app.callback(
    Output('my-graph', 'figure'),
    [Input('my-id2', 'value')]
)
def update_graph(new_text):
    new_value = TextBlob(str(new_text))
    tokenized_word = new_value.words.lower()

    word_list = []
    word_frequency = []
    word_length = []
    word_set = set(tokenized_word)

    # Turn TextBlob object into list
    for obj in word_set:
        word_list.append(obj.lower())
        word_frequency.append(new_value.word_counts[obj.lower()])
        word_length.append(len(obj))

    traces = []

    for w in word_list:
        traces.append(go.Scatter(
            x=word_list,
            y=word_frequency,
            text= w,
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 1, 'color': 'white'}
            },
            name=w
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'category', 'title':'Unique Words'},
            yaxis={'type': 'linear', 'title': 'Word Frequency', 'range': [0, len(word_list) + 1]},
            legend={'x': -1, 'y': 0},
            hovermode='closest'
        )
    }




if __name__ == '__main__':
    app.run_server(debug=True)