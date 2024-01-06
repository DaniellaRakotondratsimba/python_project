#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 08/05/2020
@author: julien and antoine
"""

import praw
import urllib.request
import xmltodict
import numpy as np
import pickle
import datetime
import pandas as pd

#Chargement des données de Reddit
reddit = praw.Reddit(client_id='wfrwVmRrikEa9yhkXWMzMQ', client_secret='ahqeIx-Xp4pbFgGccGsLrrd1aecWkg', user_agent='projet_python')

subr = reddit.subreddit('Coronavirus')

textes_Reddit = []

for post in subr.hot(limit=100):
    texte = post.title
    texte = texte.replace("\n", " ")
    textes_Reddit.append(texte)

#Chargement des données d'Arxiv
textes_Arxiv = []

query = "covid"
url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results=100'
url_read = urllib.request.urlopen(url).read()

#url_read est un "byte stream" qui a besoin d'être décodé
data =  url_read.decode()

dico = xmltodict.parse(data) #xmltodict permet d'obtenir un objet ~JSON
docs = dico['feed']['entry']
for d in docs:
    texte = d['title']+ ". " + d['summary']
    texte = texte.replace("\n", " ")
    textes_Arxiv.append(texte)

#on concatène tout ça :    
corpus = textes_Reddit + textes_Arxiv
print("Longueur du corpus : " + str(len(corpus)))

for doc in corpus:
    print("Nombre de phrases : " + str(len(doc.split("."))))
    print("Nombre de mots : " + str(len(doc.split(" "))))    

nb_phrases = [len(doc.split(".")) for doc in corpus]
print("Moyenne du nombre de phrases : " + str(np.mean(nb_phrases)))

nb_mots = [len(doc.split(" ")) for doc in corpus]
print("Moyenne du nombre de mots : " + str(np.mean(nb_mots)))
print("Nombre total de mots dans le corpus : " + str(np.sum(nb_mots)))

corpus_plus100 = [doc for doc in corpus if len(doc)>100]

chaine_unique = " ".join(corpus_plus100)

with open("out.pkl", "wb") as f:
    pickle.dump(corpus_plus100, f)
    
with open("out.pkl", "rb") as f:
    corpus_plus100 = pickle.load(f)

aujourdhui = datetime.datetime.now()
print(aujourdhui)

#Mettre le corpus dans un dataFrame
"""@author: chatGPT"""

#Créer les identifiants
ids = list(range(1, len(corpus_plus100) + 1))

#Créer une liste des origines : Reddit ou Arxiv
origins = ['reddit' if i < len(textes_Reddit) else 'arxiv' for i in range(len(corpus_plus100))]

df = pd.DataFrame({
    'ID': ids,
    'Text': corpus_plus100,
    'Origin': origins
})

print(df)