from flask import Flask
from flask import render_template
from flask import ( request )
import math
import random

app = Flask(__name__)

trigrams = {}
bigrams = {}
unigrams = {}

content = open("data/camus.txt", "r").read()

words = content.split()

for i in range(0,len(words) - 2):
    first = words[i]
    second = words[i+1]
    third = words[i+2]
    full = first + " " + second
    if full in trigrams:
        if third in trigrams[full]:
            trigrams[full][third] += 1
        else:
            trigrams[full][third] = 1
    else:
        trigrams[full] = {third: 1}

for key in trigrams:
    if key == "in the":
        print("key")
        print(key)
        print("val")
        print(trigrams[key])

if "of life" in trigrams:
    print("oh")

for i in range(0,len(words)-1):
    first = words[i]
    second = words[i+1]
    if first in bigrams:
        if second in bigrams[first]:
            bigrams[first][second] += 1
        else:
            bigrams[first][second] = 1
    else:
        bigrams[first] = {second: 1}

for i in range(0,len(words)):
    if words[i] in unigrams:
        unigrams[words[i]] += 1
    else:
        unigrams[words[i]] = 1
    

def get_trigram_next(two_words):
    min = 0
    res = ""
    for val in trigrams[two_words]:
        count = trigrams[two_words][val]
        if count > min:
            min = count
            res = val
    return res

def get_bigram_next(word):
    min = 0
    res = ""
    for key in bigrams[word]:
        count = bigrams[word][key]
        if count > min:
            min = count
            res = key
    return res

def get_unigram_next():
    min = 0
    res = ""
    for key in unigrams:
        if unigrams[key] > min:
            min = unigrams[key]
            res = key
    return res


@app.route('/', methods=['POST', 'GET'])
def generate():
    if request.method == 'POST':
        r = request.form["input"]
        if (r == None):
            return "Missing input!"
        
        split_input = r.split()
        last_two = split_input[-2] + " " + split_input[-1]
        last = split_input[-1]
        out = r
        for i in range(200):
            split_input = out.split()
            last_two = split_input[-2] + " " + split_input[-1]
            last = split_input[-1]
            if last_two in trigrams:
                print("trigram called")
                # split_input = out.split()
                # last_two = split_input[-2] + " " + split_input[-1]
                # last = split_input[-1]
                out = out + " " + get_trigram_next(last_two)
            elif last in bigrams:
                print("bigram called")
                # split_input = out.split()
                # last = split_input[-1]
                out = out + " " + get_bigram_next(last)
            else: 
                print("unigram called")
                # split_input = out.split()
                # last = split_input[-1]
                out = out + " " + get_unigram_next()

                
        
        return render_template('output.html', output = out)

    if request.method == 'GET':
        return render_template('form.html')