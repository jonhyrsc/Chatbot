# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 11:34:25 2019

@author: joao
"""
#%%Imports

import nltk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()


#%% Sentece Segmentation############



#%% Word Tokenization ############
def word_tokenization(text):
    tokenized_text = nltk.tokenize.word_tokenize(text)
    return tokenized_text


#%% Remove StopWords and punctuation
def extract_stopWord(sentence):
    stopword = set(stopwords.words('portuguese') + list(punctuation))
    filtered_sentence = []
    for word in sentence:
        if word not in stopword:
            filtered_sentence.append(word)
    filtered_sentence = " ".join(filtered_sentence)
    return filtered_sentence

#%% Part of speech tagging
def tag_word(sentence):
    tagged_word = nltk.pos_tag(sentence)


#%% Extract verbs/nouns or adjectives
def extract_grammar(tagged_words):
    group = [word[1] for word in tagged_words]
    for x in group:
        if (x == 'NN'):
            group.remove(x)




# #%% Part of speech tagging
#
# tagged_word_Eng = nltk.pos_tag(filtered_sentence_Eng)
# tagged_word_PT = nltk.pos_tag(filtered_sentence_PT)
#
#
#
#
# #%% Stemização
# stemed_word_Eng = []
# for w in filtered_sentence_Eng:
#     stemed_word_Eng.append(porter_stemmer.stem(w))
#
# stemed_word_PT = []
# for w in filtered_sentence_PT:
#     stemed_word_PT.append(porter_stemmer.stem(w))
#
#
# #%% Join text again
#
#
# joined_text_Eng = " ".join(filtered_sentence_Eng)
# joined_text_PT = " ".join(filtered_sentence_PT)


#ver txt's assossiados a cada corpora
#texts_webtext = webtext.fileids()
#texts_state_union = state_union.fileids()
#texts_pt = machado.fileids()







#
#NN_count = 0
#JJ_count = 0
##
##for i in filtered_sentence_tagged:
##    for x in i:
##        tag = x[2]
##        if tag == 'JJ':
##            JJ_count += 1
##        elif tag == 'NN':
##            NN_count += 1
#
#
#
#frequencia = FreqDist(filtered_sentence)



#import numpy as np
