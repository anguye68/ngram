#!/usr/bin/env python
# coding: utf-8

# In[9]:


import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import random
import re
import sys
import os
import time

if len(sys.argv) < 4:
    print('Please provide the the following arguments: n-gram, number of sentences, and at least one text file.')
    exit(1)

cwd = os.path.dirname(os.path.realpath(__file__))
fname = cwd + "\\corpus1.txt"
words = int(sys.argv[1])
sentences = int(sys.argv[2])
min_length = 10
filenames = []

def generate_sentence():
    running = True
    curr_sequence = random.choice(list(ngrams))
    output = curr_sequence
    while running == True:
        if curr_sequence not in ngrams.keys():
            break
        possible_words = ngrams[curr_sequence]
        next_word = possible_words[random.randrange(len(possible_words))]
        output += ' ' + next_word
        seq_words = nltk.word_tokenize(output)
        curr_sequence = ' '.join(seq_words[len(seq_words)-words:len(seq_words)])

        if bool(re.search("\.", next_word)) == True:
            running = False
    return output
    
def count_words(str):
    return len(re.findall(r'\w+', str))
    
for i in range(3, len(sys.argv)):
    filenames.append(str(cwd) + "\\Text Files\\" + sys.argv[i])

#filenames = [
#    "/Users/rafeefbaamer/Desktop/AIT590/3435-0.txt",
#    "/Users/rafeefbaamer/Desktop/AIT590/pg10662.txt",
#    "/Users/rafeefbaamer/Desktop/AIT590/pg4836.txt",
#]
#with open("/Users/rafeefbaamer/Desktop/AIT590/corpus1.txt", "w") as f:
with open(fname, "w", encoding='utf-8') as f:
    for index, filename in enumerate(filenames):
        f.write(nltk.corpus.gutenberg.raw(filename))
        if index != (len(filenames) - 1):
            f.write(" ")


# In[10]:


fo = open (fname, "r", encoding= 'utf-8')
corpus = fo.read()
corpus = corpus.lower()
corpus = re.sub(r'[^A-Za-z0-9. ]', ' ', corpus)
wordToken = word_tokenize(corpus)
#print(wordToken[:10])
#print(len(wordToken))
#sent_list = sent_tokenize(corpus)
#print(sent_list[:12])

start_time = time.time()

ngrams = {}
for i in range(len(wordToken)-words):
    seq = ' '.join(wordToken[i:i+words])
    #print(seq[:10])
    if  seq not in ngrams.keys():
        ngrams[seq] = []
    ngrams[seq].append(wordToken[i+words])

for i in range(sentences):
    output = generate_sentence()
    while (count_words(output) < min_length):
        output = generate_sentence()
    print("Sentence " + str(i + 1) + ": " + output)
stop_time = time.time()
print('Time elapsed - ', round(stop_time - start_time), 'secs')
#print(ngrams.items())
