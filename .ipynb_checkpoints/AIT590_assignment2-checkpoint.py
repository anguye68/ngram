#!/usr/bin/env python
# coding: utf-8

# In[9]:


import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import random
import re
import sys
import os

cwd = os.getcwd()

for i in range(1, len(sys.argv)):
    files.append(cwd.join(sys.argv(i))

n = sys.argv(0)

files = []
filenames = [
    "/Users/rafeefbaamer/Desktop/AIT590/3435-0.txt",
    "/Users/rafeefbaamer/Desktop/AIT590/pg10662.txt",
    "/Users/rafeefbaamer/Desktop/AIT590/pg4836.txt",
]
with open("/Users/rafeefbaamer/Desktop/AIT590/corpus1.txt", "w") as f:
    for index, filename in enumerate(filenames):
        f.write(nltk.corpus.gutenberg.raw(filename))
        if index != (len(filenames) - 1):
            f.write(" ")


# In[10]:


fo = open ("/Users/rafeefbaamer/Desktop/AIT590/corpus1.txt", "r", encoding= 'utf-8')
corpus = fo.read()
corpus = corpus.lower()
corpus = re.sub(r'[^A-Za-z0-9. ]', ' ', corpus)
wordToken = word_tokenize(corpus)
#print(wordToken[:10])
#print(len(wordToken))
#sent_list = sent_tokenize(corpus)
#print(sent_list[:12])

ngrams = {}
words = 3
for i in range(len(wordToken)-words):
    seq = ' '.join(wordToken[i:i+words])
    #print(seq[:10])
    if  seq not in ngrams.keys():
        ngrams[seq] = []
    ngrams[seq].append(wordToken[i+words])


# In[28]:
#To obtain start words of the n-grams generated
startwords = random.choice(list(ngrams)) #Will randomly choose one from ngrams dictionary
print(startwords)

curr_sequence = ' '.join(startwords) #beginning 0-3 words of text
output = curr_sequence
running = True

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
        
print(output)
print(ngrams.items())


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




