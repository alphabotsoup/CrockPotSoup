# Front-end imports
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output,Input,State
# Back-end imports
from pattern.en import parse, pprint, parsetree, Chunk, number
from pattern.search import search

### Init front-end
css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=css)
# Page layout
app.layout([
    # Input box
    html.Div([
        dcc.Textarea(placeholder='Paste input "program" here', id='input'),
        html.Button('Compile', id='submit')
    ]),
    # Compilation options
    html.Div([],id="compile"),
    # Output
    html.Div([],id="out")
])


### Init back-end
pseudocode = ""   # Container for pseudocode (Sprint 3 demonstration of function calls)

# Declare contextual variables (inspired by Perl speclal/default variables)
# Nouns are basically copied here when referenced so that pronouns / implicit references can access them
context_vars = {
#    "male": None,   # "he", "his", etc     Excluded from prototype
#    "female": None, # "she", "her", etc    Excluded from prototype
    "var": None,    # "that", "its", etc -- also includes male *or* female references
    "array": []     # "they", "their", "those", etc -- no gendered plural pronouns as far as I'm aware
}

### Functions (intrinsic operations, "standard" functions)
# Arithmetic
# This section right here is a fantastic candidate for the "runtime generated code" concept I presented about in class
def add(*args):
    n = 0
    for arg in args:
        if isinstance(arg, list):
            # If an argument is a list of numbers, unpack and make recursive call
            n += add(*arg)
        elif not isinstance(arg, numbers.Number):
            continue
        else:
            n += arg
    return n
def sub(*args):
    n = args[0]
    for arg in args[1:]:
        if isinstance(arg, list):
            # If an argument is a list of numbers, unpack and make recursive call
            n -= sub(*arg)
        elif not isinstance(arg, numbers.Number):
            continue
        else:
            n -= arg
    return n
def mul(*args):
    n = args[0]
    for arg in args[1:]:
        if isinstance(arg, list):
            # If an argument is a list of numbers, unpack and make recursive call
            n *= mul(*arg)
        elif not isinstance(arg, numbers.Number):
            continue
        else:
            n *= arg
    return n
def div(*args):
    n = args[0]
    for arg in args[1:]:
        if isinstance(arg, list):
            # If an argument is a list of numbers, unpack and make recursive call
            n /= div(*arg)
        elif not isinstance(arg, numbers.Number):
            continue
        else:
            n /= arg
    return n
def mod(*args):
    n = args[0]
    for arg in args[1:]:
        if isinstance(arg, list):
            # If an argument is a list of numbers, unpack and make recursive call
            n %= mod(*arg)
        elif not isinstance(arg, numbers.Number):
            continue
        else:
            n %= arg
    return n
# Placeholder "arg": positional arguments go subj,obj; only obj used here
def inc(arg, num, *args):
    return num+1 if isinstance(num, numbers.Number) else 0
def dec(arg, num, *args):
    return num-1 if isinstance(num, numbers.Number) else 0

# Assignment
OBJECTS = {}    # Runtime table of declared objects

def exist(var,val,*args):
    OBJECTS[var] = val
def has(var,*args):
    OBJECTS[var] = args

# Verb->Function lookup table
VERBS = {
    "add": [add,inc],
    "increment": [inc],
    "increase": [add,inc],
    "+": [add,inc],
    "++": [inc],

    "sub": [sub,dec],
    "subtract": [sub,dec],
    "decrement": [dec],
    "decrease": [sub,dec],
    "-": [sub,dec],
    "--": [dec],

    "multiply": [mul],
    "*": [mul],
    "x": [mul],

    "divide": [div,mod],
    "/": [div],
    "%": [mod],

    "is": [exist],
    "=": [exist],
    "has": [has,exist]
}



### Dash I/O
# Compile input
@app.callback(
    Output('compile', 'children'),
    [Input('submit', 'n_clicks')],
    [State('input', 'value')]
)
def compile_input(n_clicks, text_input):
    # For each sentence, our interpreter breaks it out into a sequence of actions based on the verbs identified.
    # Remove newlines by joining each line into a single string
    paragraph = " ".join(text_input)

    ### Get Subject-Verb-Object chunks
    text = parsetree(paragraph, relations=True, lemmata=True)
    # Treat all unchunked numbers ('CD's) as noun phrases
    for sentence in text:
        for word in sentence:
            if word.type == 'CD' and word.chunk is None:
                word.chunk = Chunk(sentence, words=[word], type='NP')
    # Print resulting structure
    #pprint(parse(paragraph, relations=True, lemmata=True))

    html_form = []  # Container for HTML form children
    ### Step through each clause and map to function calls
    for sentence in text:
        for verb in sentence.verbs:
            # Extract subject & object from parser, or assume nearest noun phrases
            subj = verb.subject or verb.previous(type='NP')
            obj = verb.object or verb.next(type='NP')

            # Generate pseudocode function call (Sprint 3)
            if subj: pseudocode += subj.head.string + '.'
            pseudocode += verb.head.lemma + '('
            if obj: pseudocode += obj.head.string
            pseudocode += ')'
            pseudocode += "\n"

            ### Compile actual function call
            # Lookup verb
            opts = [ {'label': 'Ignore this Verb Phrase', 'value': -1} ]
            if verb.head.lemma in VERBS:
                opts.extend( [{'label': func.__name__, 'value': i} for i,func in enumerate(VERBS[verb.head.lemma])] )

            # Ask user to choose interpretation of Verb Phrase
            html_form.extend([
                html.H3(subj + " " + verb + " " + obj),
                dcc.Dropdown(options=opts, placeholder="Select interpretation"),
                dcc.Checklist(options=[{'label': 'Also pass context?', 'value':'con_var'}])
            ])
    html_form.append(html.Button('Process', id='process'))
    return html_form

# Output
@app.callback(
    Output('out', 'children'),
    [Input('process', 'n_clicks')],
    [State('input', 'value'), State('compile', 'children')]
)
def output(n_clicks, text_input, options):
    # Remove newlines by joining each line into a single string
    paragraph = " ".join(text_input)

    ### Get Subject-Verb-Object chunks
    text = parsetree(paragraph, relations=True, lemmata=True)
    # Treat all unchunked numbers ('CD's) as noun phrases
    for sentence in text:
        for word in sentence:
            if word.type == 'CD' and word.chunk is None:
                word.chunk = Chunk(sentence, words=[word], type='NP')
    # Print resulting structure
    #pprint(parse(paragraph, relations=True, lemmata=True))

    html_out = []  # Container for HTML output div children
    o = 0          # Option index (index of div 'compile' children)
    ### Step through each clause and map to function calls
    for sentence in text:
        for verb in sentence.verbs:
            # Extract subject & object from parser, or assume nearest noun phrases
            subj = verb.subject or verb.previous(type='NP')
            obj = verb.object or verb.next(type='NP')

            # Compute function call
            o+=1    # Get context var checkbox
            if options[o].value == 'con_var':
                con_var = context_vars['var']
            else:
                con_var = None
            o+=1    # Get interpretation dropdown
            if options[o].value >= 0:
                func = VERBS[verb.head.lemma][options[o].value]
                if func.__name__ == 'is' or func.__name__ == 'has':
                    context_vars['var'] = func(subj.head, con_var or number(obj.head) or obj.head)
                else:
                    context_vars['var'] = func(number(subj.head),number(obj.head),con_var)
            else:
                context_vars['var'] = number(obj.head)

            # Generate output
            html_out.append(html.H4(subj + " " + verb + " " + obj + " -- " + context_vars['var']))
    html_out.append(html.H5("Object definitions:"))
    for var,val in OBJECTS.items():
        html_out.append(html.H6(var + ": " + str(val)))
    return html_out


if __name__ == '__main__':
    app.run(debug=True)
