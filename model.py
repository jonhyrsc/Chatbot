# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 11:34:25 2019

@author: joao
"""
import nltk
import sys
from nltk.corpus import *
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.tag import pos_tag_sents
from nltk.probability import FreqDist
from string import punctuation

exemplo = """É um não querer mais que bem querer. É um andar solitário entre a gente.É nunca contentar-se de contente.É um cuidar que se ganha em se perder."""

exemplo2 = """ Amor é fogo que arde sem se ver.É ferida que dói, e não se sente.É um contentamento descontente.É dor que desatina sem doer.
"""

#ver txt's assossiados a cada corpora
#texts_webtext = webtext.fileids()
#texts_state_union = state_union.fileids()
#texts_pt = machado.fileids()
#
text_web = webtext.raw('firefox.txt')
#token_web  = nltk.word_tokenize(text_web.lower())

text_pt = machado.raw('contos/macn001.txt')
# sentencas = sent_tokenize(text_pt) # token por sentenca
# palavras = word_tokenize(text_pt.lower()) # token por palavra
# teste = word_tokenize(exemplo.lower())

#set de stopwords
stopword = set(stopwords.words('portuguese') + list(punctuation)) # o set não permite palavras repetidas
#filtered_sentence = [w for w in palavras if not w in stopword]

#fitrar a sentenca
def tokenize_sentence(text):
    return word_tokenize(text.lower)






filtered_sentence = []
for w in palavras:
    if  w not in stopword:
        filtered_sentence.append(w)

#print(teste)
#print(filtered_sentence)


filtered_sentence_tagged = nltk.pos_tag(filtered_sentence)

NN_count = 0
JJ_count = 0
#
#for i in filtered_sentence_tagged:
#    for x in i:
#        tag = x[2]
#        if tag == 'JJ':
#            JJ_count += 1
#        elif tag == 'NN':
#            NN_count += 1


#ler linhas
def create_lexicon(text_pt, text_web):
    lexicon = []
    for file in [text_pt, text_web]:
        with open(file, 'r') as f:
            conteudo = f.readlines()
            for l in conteudo[:hm_line]:
                all_words = word_tokenize(l.lower())
                lexicon += list(all_words)
#lematização
    lexicon = [lemmatizer.lemmatize(i) for i in lexicon]




dicionario = create_lexicon(text_pt, text_web)

frequencia = FreqDist(filtered_sentence)



#import numpy as np

#sentence_teste = "Nós estamos aqui reunidos, com certeza, de uma só coisa! "

#token = nltk.word_tokenize(sentence_teste)
