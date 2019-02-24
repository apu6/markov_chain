from flask import Flask
from flask import render_template
from flask import ( request )
import math
import spacy
import random
from spacy.lang.en import English

app = Flask(__name__)
nlp = spacy.load('en')
nlp = spacy.load('en_core_web_sm')
parser = English()


content = open("data/10k_words.txt", "r").read()

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

@app.route('/', methods=['POST', 'GET'])
def generate():
    if request.method == 'POST':
        # req = request.get_json()
        r_adj = request.form["adj"]
        r_verb = request.form["verb"]
        r_noun = request.form["noun"]
        r_adv = request.form["adv"]
        r_prep = request.form["prep"]

        if (r_adj == None or r_verb == None or r_noun == None or r_adv == None or r_prep == None):
            return "Missing an input!"

        first_line = gen_first_line(r_noun, r_verb, r_adj, r_adv, r_prep)
        second_line = gen_line()
        third_line = gen_line()
        fourth_line = gen_line()

        return render_template('poem.html', first = first_line, second = second_line, third = third_line, fourth = fourth_line)

    if request.method == 'GET':
        return render_template('form.html')

def gen_match(target, pos):
    max = -math.inf
    match = ''
    targ_tok = nlp(target)[0]
    for token in pos:
        if token.similarity(targ_tok) > max and target != token.text:
            max = token.similarity(targ_tok)
            match = token.text
    return match

def gen_rand_match(pos):
    idx = random.randint(1, len(pos))
    return pos[idx].text


def gen_first_line(r_noun, r_verb, r_adj, r_adv, r_prep):
    idx = random.randint(0,3)
    first_line = ""
    if idx == 0:
        gen_adj = gen_match(r_adj, adjectives)
        gen_noun = gen_match(r_noun, nouns)
        gen_verb = gen_match(r_verb, verbs)
        first_line = gen_adj + " " + gen_noun + " " + gen_verb
    elif idx == 1:
        gen_adv = gen_match(r_adv, adverbs)
        gen_verb = gen_match(r_verb, verbs)
        gen_prep = gen_match(r_prep, preps)
        gen_adj = gen_match(r_adj, adjectives)
        gen_noun = gen_match(r_noun, nouns)
        first_line = gen_adv + " " + gen_verb + " " + gen_prep + " " + gen_adj + " " + gen_noun
    elif idx == 2:
        gen_adj = gen_match(r_adj, adjectives)
        gen_noun = gen_match(r_noun, nouns)
        gen_verb = gen_match(r_verb, verbs)
        gen_adv = gen_match(r_adv, adverbs)
        gen_prep = gen_match(r_prep, preps)
        gen_noun = gen_match(r_noun, nouns)
        first_line = gen_adj + " " + gen_noun + " " + gen_verb + " " + gen_adv + " " + gen_prep + " " + gen_noun
    elif idx == 3:
        gen_adv = gen_match(r_adv, adverbs)
        gen_verb = gen_match(r_verb, verbs)
        rand_adv = gen_rand_match(adverbs)
        rand_verb = gen_rand_match(verbs)
        rand_adv2 = gen_rand_match(adverbs)
        rand_verb2 = gen_rand_match(verbs)
        first_line = gen_adv + " " + gen_verb + " " + rand_adv + " " + rand_verb + " " + rand_adv2 + " " + rand_verb2
    return first_line

def gen_line():
    idx = random.randint(0,3)
    line = ""
    if idx == 0:
        rand_adj = gen_rand_match(adjectives)
        rand_noun = gen_rand_match(nouns)
        rand_verb = gen_rand_match(verbs)
        line = rand_adj + " " + rand_noun + " " + rand_verb
    elif idx == 1:
        rand_adv = gen_rand_match(adverbs)
        rand_verb = gen_rand_match(verbs)
        rand_prep = gen_rand_match(preps)
        rand_adj = gen_rand_match(adjectives)
        rand_noun = gen_rand_match(nouns)
        line = rand_adv + " " + rand_verb + " " + rand_prep + " " + rand_adj + " " + rand_noun
    elif idx == 2:
        rand_adj = gen_rand_match(adjectives)
        rand_noun = gen_rand_match(nouns)
        rand_verb = gen_rand_match(verbs)
        rand_adv = gen_rand_match(adverbs)
        rand_prep = gen_rand_match(preps)
        rand_noun = gen_rand_match(nouns)
        line = rand_adj + " " + rand_noun + " " + rand_verb + " " + rand_adv + " " + rand_prep + " " + rand_noun
    elif idx == 3:
        rand_adv = gen_rand_match(adverbs)
        rand_verb = gen_rand_match(verbs)
        rand_adv2 = gen_rand_match(adverbs)
        rand_verb2 = gen_rand_match(verbs)
        rand_adv3 = gen_rand_match(adverbs)
        rand_verb3 = gen_rand_match(verbs)
        line = rand_adv + " " + rand_verb + " " + rand_adv2 + " " + rand_verb2 + " " + rand_adv3 + " " + rand_verb3
    return line


s1 = ["adj", "n", "v"]
s2 = ["adv", "v", "p", "a", "n"]
s3 = ["adj", "n", "v", "adv", "p", "n"]
s4 = ["adv", "v", "adv", "v", "adv", "v"]



