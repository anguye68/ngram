#!/usr/bin/env python
# coding: utf-8

""" Programming Assignment 2: Team 3 - Rafeef Baamer, Ashish Hingle, Rina Lidder, & Andy Nguyen

 Description: This program takes input from multiple text files and generates a given number of randomized sentences.
 The program  is run by calling 'ngram.py' and will learn an N-gram language model based on the submitted plain text files. 
 
 The program can be called from a command line based on the submitted plain text files, the number of desired n-grams (n)
 and desired sentences (m). For example, the command "ngram.py 3 10 3435-0.txt pg10662.txt pg4836.txt" can
 be used to run the program.
 
  Resources used for this lab come from the materials provided in the AIT 590 course materials.
 - Lecture powerpoints (AIT 590)
 - Stanford University Prof. Dan Jurafsky's Video Lectures (https://www.youtube.com/watch?v=zQ6gzQ5YZ8o)
 - Joe James Python: NLTK video series (https://www.youtube.com/watch?v=RYgqWufzbA8)
 - w3schools Python Reference (https://www.w3schools.com/python/)
 - regular expressions 101 (https://regex101.com/)
 - Timer examples understood from: https://stackoverflow.com/questions/15528939/python-3-timed-input
 - How to use command line: geeksforgeeks.org/how-to-use-sys-argv-in-python/
 - How to use command line: https://stackoverflow.com/questions/4188467/how-to-check-if-an-argument-from-commandline-has-been-set
 - Overall process guidance: https://stackabuse.com/python-for-nlp-developing-an-automatic-text-filler-using-n-grams/
 
"""

#import libraries
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import random
import re
import sys
import os
import time
from string import punctuation

#stores the current time of the request from user as the 'start time'
start_time = time.time()

#Interprets the number of arguments a user is passing in the command line
arguments = len(sys.argv)

#if the user is just passing the file name in the terminal it will provide the following instructions
if arguments == 1:
    print("""
    Hi, welcome to our N-gram model! This was developed by AIT590 Team 3: Rafeef Baamer, Ashish Hingle,
      Rina Lidder, and Andy Nguyen.

      To execute the n-gram model pass 'ngram.py' followed by the number of ngrams,
      sentences, and text files you want the program to use.

      To return to the instructions run 'ngram.py' again.""")
    exit(1)   
elif arguments in range(2,4): #if the user is forgetting to give the words/sentences for the n-grams it will provide this error message.
    print('\nUnable to execute without all parameters. Return to instructions')
    exit(1)

#take input from command line and save variables
cwd = os.path.dirname(os.path.realpath(__file__))    #determine the path where the file is being run from
fname = cwd + "/corpus1.txt"    #declare the corpus1 file
words = int(sys.argv[1])        #saves the number of ngrams desired based on the user's call
sentences = int(sys.argv[2])    #saves the number of sentences desired based on the user's call
min_length = 10                 #minimum number of words in a sentence
filenames = []                  #variable that will store the input files

#initilaize the first words and ngrams dictionaries
first_words = {}
ngrams = {}

#this function generates a dictionary of possible first words that begin a sentence
def generate_first_words():
    for sent in sentToken:
        #tokenize the individual sentence and save it in a temp list
        holder = word_tokenize(sent)
        #save the adjacent words to the sequence
        seq = ' '.join(holder[i:i+words])

        #If the sentence has atleast the number of ngrams requested, then this sentence can be considered
        #for use with as a first word
        if len(holder) > words+1:
            #checks if the sequence is not in the first words dictionary, then add it to the dictionary
            if  seq not in first_words.keys():
                first_words[seq] = []
            first_words[seq].append(holder[words])

#this function generates a sentence based on the number of ngrams entered
def generate_sentence():
    #variable to hold if the end point (. ? !) has been reached
    running = True
    
    #generates a random ngram to begin the sentence
    curr_sequence = random.choice(list(first_words))
    output = curr_sequence
    
    #loop while the running is true. Based on the first ngram that was generated above, look for a potential next word
    #continue until a (. ? !) have been reached, and end the loop.
    while running == True:
        if curr_sequence not in ngrams.keys():
            break
        possible_words = ngrams[curr_sequence]
        next_word = possible_words[random.randrange(len(possible_words))]
        output += ' ' + next_word
        seq_words = nltk.word_tokenize(output)
        curr_sequence = ' '.join(seq_words[len(seq_words)-words:len(seq_words)])

        #when a (. ! ?) is found, change the running variable and end the while loop
        if bool(re.search('[\.\?!]', next_word)) == True:
            running = False
    return output

#format the final output
def formatter(str):
    
    #Change the final punctuation to format correctly without an extra space 
    if str[-1] == '.':
        str = re.sub(r'(\s\.)', '.', str)
    elif str[-1] == '!':
        str = re.sub(r'(\s\!)', '!', str)
    elif str[-1] == '?':
        str = re.sub(r'(\s\?)', '?', str)
    
    #Change the first letter to a capital letter
    str = str.capitalize()
    
    #Captialize i to I in the text
    str = re.sub(r'( i )', r' I ', str)
    
    #regex to remove the extra space before an apostrophe
    str = re.sub(r'\s\'', '\'', str)

    #regex to remove the extra space before a `
    str = re.sub(r'\s`', '`', str)
    
    #regex to remove the extra space before a comma
    str = re.sub(r'\s,', ',', str)
    
    #regex to remove commas at the beginning of a sentence
    str = re.sub(r'^,\s', '', str)
    str = str[0].upper() + str[1:]      #capitalize the first word
      
    return str

#counts the amount of words in a sentence
def count_words(str):
    return len(re.findall(r'\w+', str))

#create a list of text files based on the input provided by the user's call
for i in range(3, len(sys.argv)):
    filenames.append(str(cwd) + "\\Text Files\\" + sys.argv[i])

#write all the text files into a single text file 
with open(fname, "w", encoding='utf-8') as f:
    for index, filename in enumerate(filenames):
        f.write(nltk.corpus.gutenberg.raw(filename))
        if index != (len(filenames) - 1):
            f.write(" ")

#opens and readsthe single text file
fo = open (fname, "r", encoding= 'utf-8')
corpus = fo.read()

#change the contents of the text file to lowercase
corpus = corpus.lower()

#remove any unsactioned characters from the text
corpus = re.sub(r'[^A-Za-z0-9.\?!\'`, ]', ' ', corpus)

#tokenize the words and sentences
wordToken = word_tokenize(corpus)
sentToken = sent_tokenize(corpus)

#creates a list of the first words in the sentences that can be used to generate starting positions
generate_first_words()

#loop through all the words in the text file, and save the contents as ngrams based on the user's call
for i in range(len(wordToken)-words):
    seq = ' '.join(wordToken[i:i+words])
    if  seq not in ngrams.keys():
        ngrams[seq] = []
    ngrams[seq].append(wordToken[i+words])

#prints an informative welcome message
print('This program generates random sentences based on an Ngram model.')
print('AIT590 Team 3: Rafeef Baamer, Ashish Hingle, Rina Lidder, and Andy Nguyen')
print('Command line settings :', sys.argv[0], ', n:', words, ', m:', sentences, '\n')
   
#generate the sentences based on the user's call. Checks if the sentence meets the minimum length... if not, generate a new sentence
for i in range(sentences):
    output = generate_sentence()
    while (count_words(output) < min_length):
        output = generate_sentence()
    
    # formats the output before printing
    output = formatter(output)
    print("Sentence " + str(i + 1) + ": " + output + '\n')  #print the formatted sentence

#Stores time it took for n-gram model to process input as 'stop time'    
stop_time = time.time()
#subtract the two time periods to calculate the runtime of the n-gram:
print('Time elapsed :', round(stop_time - start_time), 'secs')