# Correction de G. Poux-Médard, 2021-2022

# =============== PARTIE 1 =============
# =============== 1.1 : REDDIT ===============
# Library
import praw
from os import path
import pandas as pd

# Fonction affichage hiérarchie dict
def showDictStruct(d):
    def recursivePrint(d, i):
        for k in d:
            if isinstance(d[k], dict):
                print("-"*i, k)
                recursivePrint(d[k], i+2)
            else:
                print("-"*i, k, ":", d[k])
    recursivePrint(d, 1)

# Identification
reddit = praw.Reddit(client_id='wfrwVmRrikEa9yhkXWMzMQ', client_secret='ahqeIx-Xp4pbFgGccGsLrrd1aecWkg', user_agent='projet_python')

# Requête
limit = 100
hot_posts = reddit.subreddit('all').hot(limit=limit)#.top("all", limit=limit)#

# Récupération du texte
docs = []
docs_bruts = []
afficher_cles = False
for i, post in enumerate(hot_posts):
    if i%10==0: print("Reddit:", i, "/", limit)
    if afficher_cles:  # Pour connaître les différentes variables et leur contenu
        for k, v in post.__dict__.items():
            pass
            print(k, ":", v)

    if post.selftext != "":  # Osef des posts sans texte
        pass
        #print(post.selftext)
    docs.append(post.selftext.replace("\n", " "))
    docs_bruts.append(("Reddit", post))

print (docs)
# =============== 1.2 : ArXiv ===============
# Libraries
import urllib, urllib.request
import xmltodict

# Paramètres
query_terms = ["clustering", "Dirichlet"]
max_results = 50

# Requête
url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'
data = urllib.request.urlopen(url)

# Format dict (OrderedDict)
data = xmltodict.parse(data.read().decode('utf-8'))

#showDictStruct(data)

# Ajout résumés à la liste
for i, entry in enumerate(data["feed"]["entry"]):
    if i%10==0: print("ArXiv:", i, "/", limit)
    docs.append(entry["summary"].replace("\n", ""))
    docs_bruts.append(("ArXiv", entry))
    #showDictStruct(entry)

# =============== 1.3 : Exploitation ===============
print(f"# docs avec doublons : {len(docs)}")
docs = list(set(docs))
print(f"# docs sans doublons : {len(docs)}")

for i, doc in enumerate(docs):
    print(f"Document {i}\t# caractères : {len(doc)}\t# mots : {len(doc.split(' '))}\t# phrases : {len(doc.split('.'))}")
    if len(doc)<100:
        docs.remove(doc)

longueChaineDeCaracteres = " ".join(docs)

# =============== PARTIE 2 =============
# =============== 2.1, 2.2 : CLASSE DOCUMENT ===============
from Classes import Document

# =============== 2.3 : MANIPS ===============
"""import datetime
collection = []
for nature, doc in docs_bruts:
    if nature == "ArXiv":  # Les fichiers de ArXiv ou de Reddit sont pas formatés de la même manière à ce stade.
        #showDictStruct(doc)

        titre = doc["title"].replace('\n', '')  # On enlève les retours à la ligne
        try:
            authors = ", ".join([a["name"] for a in doc["author"]])  # On fait une liste d'auteurs, séparés par une virgule
        except:
            authors = doc["author"]["name"]  # Si l'auteur est seul, pas besoin de liste
        summary = doc["summary"].replace("\n", "")  # On enlève les retours à la ligne
        date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  # Formatage de la date en année/mois/jour avec librairie datetime

        doc_classe = Document(titre, authors, date, doc["id"], summary)  # Création du Document
        collection.append(doc_classe)  # Ajout du Document à la liste.

    elif nature == "Reddit":
        #print("".join([f"{k}: {v}\n" for k, v in doc.__dict__.items()]))
        titre = doc.title.replace("\n", '')
        auteur = str(doc.author)
        date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
        url = "https://www.reddit.com/"+doc.permalink
        texte = doc.selftext.replace("\n", "")

        doc_classe = Document(titre, auteur, date, url, texte)

        collection.append(doc_classe)"""
#================ GENERATION DE DOCUMENT TD5 ==================
from Classes import Document, RedditDocument, ArxivDocument
import datetime

collection = []
# =============== FACTORY PATTERN ===============
class DocumentFactory:
    @staticmethod
    def create_document(nature, doc):
        if nature == "ArXiv":  # Les fichiers de ArXiv ou de Reddit sont pas formatés de la même manière à ce stade.
        #showDictStruct(doc)

            titre = doc["title"].replace('\n', '')  # On enlève les retours à la ligne
            """try:
                authors = ", ".join([a["name"] for a in doc["author"]])  # On fait une liste d'auteurs, séparés par une virgule
            except:
                authors = doc["author"]["name"]  # Si l'auteur est seul, pas besoin de liste"""
            # récupérer l'auteur et les co-auteur
            try:
                authors_list = [a["name"] for a in doc["author"]]
                primary_author = authors_list[0]
                co_authors = authors_list[1:] if len(authors_list) > 1 else []
            except TypeError:
                primary_author = doc["author"]["name"]
                co_authors = []
            summary = doc["summary"].replace("\n", "")  # On enlève les retours à la ligne
            date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  # Formatage de la date en année/mois/jour avec librairie datetime

            #return ArxivDocument(titre, authors, date, doc["id"], summary) 
            return ArxivDocument(titre, primary_author, date, doc["id"], summary, co_auteurs=co_authors)# Création du Document
           
        elif nature == "Reddit":
            titre = doc.title.replace("\n", '')
            auteur = str(doc.author)
            date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
            url = "https://www.reddit.com/"+doc.permalink
            texte = doc.selftext.replace("\n", "")
            nb_commentaires = doc.num_comments
            return RedditDocument(titre, auteur, date, url, texte, nb_commentaires)
        else:
            raise ValueError("Nature de document non supportée.")

# Utilisation du factory pour créer des objets Document
for nature, doc in docs_bruts:
    doc_classe = DocumentFactory.create_document(nature, doc)
    collection.append(doc_classe)

#===========================================================
# Création de l'index de documents
id2doc = {}
for i, doc in enumerate(collection):
    id2doc[i] = doc.titre

# =============== 2.4, 2.5 : CLASSE AUTEURS ===============
from Classes import Author

# =============== 2.6 : DICT AUTEURS ===============
authors = {}
aut2id = {}
num_auteurs_vus = 0

# Création de la liste+index des Auteurs
for doc in collection:
    if doc.auteur not in aut2id:
        num_auteurs_vus += 1
        authors[num_auteurs_vus] = Author(doc.auteur)
        aut2id[doc.auteur] = num_auteurs_vus

    authors[aut2id[doc.auteur]].add(doc.texte)


# =============== 2.7, 2.8 : CORPUS ===============
from Corpus import Corpus
corpus = Corpus("Mon corpus")

# Construction du corpus à partir des documents
for doc in collection:
    corpus.add(doc)
#corpus.show(tri="abc")
#print(repr(corpus))


# =============== 2.9 : SAUVEGARDE ===============
# Vérifier si le fichier 'corpus.csv' existe déjà
csv_file_exists = path.exists('corpus.csv')
pickle_file_exists = path.exists('corpus.pkl')

if not pickle_file_exists: 
    import pickle

    # Ouverture d'un fichier, puis écriture avec pickle
    with open("corpus.pkl", "wb") as f:
        pickle.dump(corpus, f)

    # Supression de la variable "corpus"
    del corpus

    # Ouverture du fichier, puis lecture avec pickle
    with open("corpus.pkl", "rb") as f:
        corpus = pickle.load(f)

    # La variable est réapparue
    print("Corpus brut", corpus)

if not csv_file_exists:
    # Création du contenu CSV
    nature=corpus.elements_du_corpus()[0]
    titre=corpus.elements_du_corpus()[1]
    Auteur=corpus.elements_du_corpus()[2]
    Co_Auteurs=corpus.elements_du_corpus()[3]
    nb_commentaires=corpus.elements_du_corpus()[4]
    Date=corpus.elements_du_corpus()[5]
    url=corpus.elements_du_corpus()[6]
    texte=corpus.elements_du_corpus()[7]
    
    # Transformation des données en csv
    df = pd.DataFrame(zip(nature,titre,Auteur,Co_Auteurs,Date,url,texte,nb_commentaires), columns=['Nature','Titre','Auteur','Co_Auteurs','Date','URL','Texte','Nb commentaires'])
    df.to_csv(r'corpus.csv',index=False,sep=';')
    
    print("Creation du CSV OK")

else:
    print("Le corpus et le fichier CSV existent déjà.")

print(corpus)



