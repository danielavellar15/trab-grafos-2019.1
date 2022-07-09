#!/usr/bin/env python
# coding: utf-8
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import codecs
import unicodedata
import matplotlib.pyplot as plt
 
def read_article(file_name, stop_words):

    filedatas = codecs.open(file_name, 'r', encoding='utf-8').readlines()
    sentences = []
    all_words = []
    itens_types = [0,0,0,0]
    aux = 0
    filedatas[1], filedatas[3] = filedatas[3], filedatas[1]
    for filedata in filedatas:
        
        words = filedata.rstrip().replace(".", "").replace(",","").replace(" - ", " ").split(" ")
        key = words[0].replace(":","")
        words.pop(0)
        
        words=[word.lower() for word in words if not word.lower() in stop_words] #filtra as palavras e coloca tudo minusculo

        all_words = list(set(all_words + words))
        print(words)
        
        for i in range(len(words) - 2):
            item = []
            item.append(words[i])
            item.append(words[i+1])
            item.append(words[i+2])
            sentences.append(item)
            itens_types[aux] = itens_types[aux]+1     

        if itens_types[2] == itens_types[3]:
            itens_types[3] = itens_types[3] + 1

        if aux + 1 < 4:
            itens_types[aux+1] = itens_types[aux]
        aux = aux + 1


    return sentences, all_words, itens_types

def getWeight(index, itens_types):
    if index < itens_types[0]:
        return 2
    elif index < itens_types[1]:
        return 2
    elif index < itens_types[2]:
        return 1
    elif index < itens_types[3]:
        return 1

def sentence_similarity(similarity_matrix, sent, index, all_words, itens_types):
 
 
    # build the vector for the first sentence
    for i in range(len(sent)):
        for aux in range(len(sent)):
            if i == aux:
                continue
            x = all_words.index(sent[i])
            y = all_words.index(sent[aux])
            if index < itens_types[3] - 1:
                similarity_matrix[x][y] += getWeight(index, itens_types)
            else:
                similarity_matrix[x][y] = similarity_matrix[x][y] * 2

    
    return similarity_matrix
 
def build_similarity_matrix(sentences, all_words, itens_types):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(all_words), len(all_words)))
    for idx1 in range(len(sentences)):
            similarity_matrix = sentence_similarity(similarity_matrix, sentences[idx1], idx1, all_words, itens_types)

    return similarity_matrix


def generate_summary(file_name, top_n=5):
    nltk.download("stopwords")
    nltk.download("punkt")
    stop_words = stopwords.words('portuguese')
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences, all_words, itens_types =  read_article(file_name, stop_words)

    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, all_words, itens_types)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
    print("Indexes of top ranked_sentence order are ", ranked_sentence)    

    for i in range(top_n):
      summarize_text.append(" ".join(ranked_sentence[i][1]))

    # Step 5 - Offcourse, output the summarize texr
    print("Summarize Text: \n", ". ".join(summarize_text))

# let's begin
generate_summary( "teste.txt", 2)