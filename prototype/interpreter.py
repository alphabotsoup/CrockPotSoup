import fileinput
import nltk.chunk       # Chunking tools to translate groups of verbs/nouns into Subject-Verb-Object
import nltk.chunk.util
import nltk.chunk.regexp
from nltk.stem import WordNetLemmatizer
import nltk.tag         # Part-of-Speech Tagging (to determine verbs, nouns, etc)
import nltk.tokenize    # Breaking down raw input into words / symbols


### Init
wordnet = WordNetLemmatizer()

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
        ### Get Subject-Verb-Object chunks
        # Define regex rules for identifying SVO
        chunk_rules = [
            "<VB.?><CD>(?!<NN.?>)"  # Example: Get verbs followed by a number that *isn't* counting objects (e.g. "add seven")
        ]
        # Get chunked result
        chunked_sentence = RegexpChunkParser([ChunkRule(cr) for cr in chunk_rules], chunk_label='SVO').parse(sentence)
        # Step through each clause and map to function calls
        pass


VERBS = {

}

FUNCS = [
    {
        "desc": "assignment / existence.",
        "func": None
    }
]
