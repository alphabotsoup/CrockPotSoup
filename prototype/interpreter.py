import fileinput
from nltk.stem import WordNetLemmatizer
import nltk.tag
import nltk.tokenize


### Init
wordnet = WordNetLemmatizer()

# Check adjacent tokens for function arguments (verb objects)
def check_args():
    pass

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
for paragraph in fileinput.input():
    if paragraph.isspace(): continue    # Skip empty lines

    # Break down paragraph into sentences, then into words/tokens
    sentences = [[word for word in nltk.word_tokenize(sentence)] for sentence in nltk.sent_tokenize(paragraph)]
    for sentence in [nltk.tag.pos_tag(sentence) for sentence in sentences]:
        print(sentence)
        # Hunt down each action verb in the sentence (a sentence with no verbs is meaningless, right?)
        for index in range(len(sentence)):
            token, tag = sentence[index]
            if tag == 'VB' or tag == 'VBD' or tag == 'VBG' or tag == 'VBN': # Verb invocation
                verb = wordnet.lemmatize(token, 'v')   # Get base form of verb
                # Get subject / objects (arguments), if any


VERBS = {

}

FUNCS = [
    {
        "desc": "assignment / existence.",
        "func": None
    }
]
