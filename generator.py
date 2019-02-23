from flask import Flask
from flask import render_template
from flask import ( request )
import spacy
import math
from spacy.lang.en import English

app = Flask(__name__)
nlp = spacy.load('en')
nlp = spacy.load('en_core_web_sm')
parser = English()


content = open("data/small_dictionary.txt", "r").read()

doc = nlp(content)

nouns = []
adjectives = []
adverbs = []
verbs = []
preps = []
articles = []

for token in doc:
    if token.pos_ == "NOUN":
        nouns.append(token)
    elif token.pos_ == "ADV":
        adverbs.append(token)
    elif token.pos_ == "ADJ":
        adjectives.append(token)
    elif token.pos_ == "VERB":
        verbs.append(token)
    elif token.pos_ == "ADP":
        preps.append(token)
    elif token.pos_ == "DET":
        articles.append(token)

# print(nlp("in")[0].pos_)
# print(preps)
# print(articles)

# print(nouns)
@app.route('/', methods=['POST', 'GET'])
def generate():
    if request.method == 'POST':
        # req = request.get_json()
        r_adj = request.form["adj"]
        r_verb = request.form["verb"]
        r_noun = request.form["noun"]
        r_adv = request.form["adv"]
        r_prep = request.form["prep"]
        # print(r_prep)
        # print(r_noun)

        gen_noun = get_match(r_noun, nouns)
        gen_verb = get_match(r_verb, verbs)
        gen_adj = get_match(r_adj, adjectives)
        gen_adv = get_match(r_adv, adverbs)
        gen_prep = get_match(r_prep, preps)

        poem = gen_adj + " " + gen_noun + " " + gen_adv + " " + gen_verb
        return poem

    if request.method == 'GET':
        return render_template('main.html')

def get_match(target, pos):
    max = -math.inf
    match = ''
    targ_tok = nlp(target)[0]
    for token in pos:
        if token.similarity(targ_tok) > max and target != token.text:
            max = token.similarity(targ_tok)
            match = token.text
    return match

s1 = ["adj", "n", "v"]
s2 = ["adv", "v", "p", "a", "n"]
s3 = ["adj", "n", "v", "adv", "p", "n"]

# print(get_match("happy", adjectives))
# print(get_match("dog", nouns))
# print(get_match("run", verbs))
# print(get_match("sadly", adverbs))
# print(get_match("in", preps))
# print(get_match("field", nouns))


