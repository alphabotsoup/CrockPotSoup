import fileinput
from pattern.en import parse, pprint, parsetree, Chunk
from pattern.search import search

### Init
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
        else:
            n += arg
    return n
def sub():
    n = args[0]
    for arg in args[1:]:
        if isinstance(arg, list):
            # If an argument is a list of numbers, unpack and make recursive call
            n -= sub(*arg)
        else:
            n -= arg
    return n
def mul():
    n = args[0]
    for arg in args[1:]:
        if isinstance(arg, list):
            # If an argument is a list of numbers, unpack and make recursive call
            n *= mul(*arg)
        else:
            n *= arg
    return n
def div():
    n = args[0]
    for arg in args[1:]:
        if isinstance(arg, list):
            # If an argument is a list of numbers, unpack and make recursive call
            n /= div(*arg)
        else:
            n /= arg
    return n
def mod():
    n = args[0]
    for arg in args[1:]:
        if isinstance(arg, list):
            # If an argument is a list of numbers, unpack and make recursive call
            n %= mod(*arg)
        else:
            n %= arg
    return n
def inc(num):
    return num+1
def dec(num):
    return num-1

# Assignment
OBJECTS = {}    # Runtime table of declared objects

def exist(obj,val):
    OBJECTS[obj] = val
def has(obj,*args):
    OBJECTS[obj] = args

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


### Here begins the REPL -- Read, Eval, Print Loop
### Our interpreter accepts either an input filename or raw input from STDIN.
### So far: For each sentence, our interpreter breaks it out into a sequence of actions based on the verbs identified.
# Remove newlines by joining each line into a single string
paragraph = " ".join(fileinput.input())

### Get Subject-Verb-Object chunks
text = parsetree(paragraph, relations=True, lemmata=True)
# Treat all unchunked numbers ('CD's) as noun phrases
for sentence in text:
    for word in sentence:
        if word.type == 'CD' and word.chunk is None:
            word.chunk = Chunk(sentence, words=[word], type='NP')
# Print resulting structure
#pprint(parse(paragraph, relations=True, lemmata=True))

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
        pass
        # Lookup verb, ask user to choose function (or skip), ask user to include context variable
        # Make real function call and set context variable to result


print(pseudocode)
print(OBJECTS)  # Dump objects created from this input

