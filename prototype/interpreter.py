import fileinput
from pattern.en import parse, pprint, parsetree, Chunk
from pattern.search import search

### Init
code = ""   # Container for pseudocode (Sprint 3 demonstration of function calls)

# Declare contextual variables (inspired by Perl speclal/default variables)
# Nouns are basically copied here when referenced so that pronouns / implicit references can access them
context_vars = {
    "male": None,   # "he", "his", etc
    "female": None, # "she", "her", etc
    "var": None,    # "that", "its", etc -- also includes male *or* female references
    "array": []     # "they", "their", "those", etc -- no gendered plural pronouns as far as I'm aware
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
pprint(parse(paragraph, relations=True, lemmata=True))

### Step through each clause and map to function calls
for sentence in text:
    for verb in sentence.verbs:
        # Extract subject & object from parser, or assume nearest noun phrases
        subj = verb.subject or verb.previous(type='NP')
        obj = verb.object or verb.next(type='NP')

        if subj: code += subj.head.string + '.'
        code += verb.head.lemma + '('
        if obj: code += obj.head.string
        code += ')'
        code += "\n"

print(code)


VERBS = {

}

FUNCS = [
    {
        "desc": "assignment / existence.",
        "func": None
    }
]
