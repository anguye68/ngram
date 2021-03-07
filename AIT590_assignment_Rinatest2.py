#!/usr/bin/env python
# coding: utf-8

#MacOS Version for Rina to run.
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import random
import re
import sys
import os
import time

#prompts the user to instruct the program the type of n-gram and number of sentences to generate.
arguments = len(sys.argv)

if arguments == 1:
    print("""
    Hi, welcome to our N-gram model! This was developed by AIT590 Team 3: Rafeef Baamer, Ashish Hingle,
      Rina Lidder, and Andy Nguyen.

      To execute the n-gram model pass 'ngram.py' followed by the number of ngrams,
      sentences, and text files you want the program to use.

      To return to the instructions run 'ngram.py' again.""")
    exit(1)   
elif arguments in range(2,4):
    print('Unable to execute without all parameters. Return to instructions')
    exit(1)


cwd = os.path.dirname(os.path.realpath(__file__))
fname = cwd + "/corpus1.txt"
words = int(sys.argv[1]) #secondnumber after file name is the words
sentences = int(sys.argv[2]) #third number after file name is the # sentences
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
    filenames.append(str(cwd) + "/Text Files/" + sys.argv[i])

with open(fname, "w", encoding='utf-8') as f:
    for index, filename in enumerate(filenames):
        f.write(nltk.corpus.gutenberg.raw(filename))
        if index != (len(filenames) - 1):
            f.write(" ")

fo = open (fname, "r", encoding= 'utf-8')
corpus = fo.read()
corpus = corpus.lower()
corpus = re.sub(r'[^A-Za-z0-9. ]', ' ', corpus)
wordToken = word_tokenize(corpus)

#stores the current time of the request from user as the 'start time'
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

#Stores time it took for n-gram model to process input as 'stop time'    
stop_time = time.time()
#subtract the two time periods to calculate the runtime of the n-gram:
print('Time elapsed - ', round(stop_time - start_time), 'secs')

"""
List of References:
geeksforgeeks.org/how-to-use-sys-argv-in-python/
https://stackoverflow.com/questions/4188467/how-to-check-if-an-argument-from-commandline-has-been-set
https://stackabuse.com/python-for-nlp-developing-an-automatic-text-filler-using-n-grams/
"""
