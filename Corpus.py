# Correction de G. Poux-Médard, 2021-2022
# Insertion et modification code HNR TDR

from Classes import Author
import re
import pandas as pd
from collections import Counter
from scipy.sparse import csr_matrix
import numpy as np


# =============== 2.7 : CLASSE CORPUS ===============
class Corpus:
    #Tester patron singeleton td5
    _instance = None  # Initialisation de la variable de classe pour stocker l'unique instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Corpus, cls).__new__(cls)
            # Nous ne réinitialisons pas ici, cela sera pris en charge par __init__
        return cls._instance

    #=========================
    def __init__(self, nom=None):  # mettre le nom optionel
        if not hasattr(self, '_initialized'): 
            self._initialized = True
            self.nom = nom
            self.authors = {}
            self.aut2id = {}
            self.id2doc = {}
            self.ndoc = 0
            self.naut = 0
            self._text_cache = None  # Cache pour la concaténation des textes
    #=========================
    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            raise Exception("Aucune instance de Corpus n'existe. Utilisez Corpus(nom) pour en créer une.")
        return cls._instance
    
    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

# =============== 2.8 : REPRESENTATION ===============
    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))
        
        #Voir le type de doc 
        for doc in docs:
            print(f"Titre: {doc.titre}\tAuteur: {doc.auteur}\tDate: {doc.date}\tType: {doc.getType()}")

    def __repr__(self):

        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))
    
     # recuperation des champs d'un document pour le CSV
       # recuperation des champs d'un document pour le CSV
    def elements_du_corpus(self):
        natures = []
        titres = []
        auteurs = []
        dates = []
        urls = []
        textes = []
        co_auteurs = []
        nb_commentaires=[]
        for key in self.id2doc.keys():
            natures.append(self.id2doc[key].getType())
            titres.append(self.id2doc[key].titre)
            auteurs.append(self.id2doc[key].auteur)
            if(self.id2doc[key].getType() == "Reddit"):
                co_auteurs.append("")  
                nb_commentaires.append(self.id2doc[key].nb_commentaires)
            else:
                co_aut = ','.join(self.id2doc[key].co_auteurs)
                co_auteurs.append(co_aut)
                nb_commentaires.append("")
            dates.append(self.id2doc[key].date)
            urls.append(self.id2doc[key].url)
            textes.append(self.id2doc[key].texte)
        
    
        return natures,titres,auteurs,co_auteurs,nb_commentaires,dates,urls,textes 

# =============== ANALYSE DU CONTENU TEXTUEL TD6 ==================
    """Avec la contribution de ChatGPT"""
    # méthode de recherche utilisant des expressions régulières
    def search(self, keyword):
        print(f"Recherche du terme: {keyword}")
        
        if self._text_cache is None:
            self._text_cache = " ".join(doc.texte for doc in self.id2doc.values())
            print("Cache du texte construit")  

        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        matches = pattern.finditer(self._text_cache)
        
        results = [match.group() for match in matches]
        
        if results:
            print(f"Nombre de correspondances trouvées: {len(results)}")  
        else:
            print("Aucune correspondance trouvée")  
        return results
    
    # methode de concordance pour une expression donnée
    def concorde(self, expression, context_size=30):
        concordance_list = []

        # Itérer sur chaque document pour construire le contexte de concordance
        for doc_id, doc in self.id2doc.items():
            # Préparer le pattern pour inclure le contexte
            pattern = re.compile(f"(.{{0,{context_size}}})\\b({expression})\\b(.{{0,{context_size}}})", re.IGNORECASE)

            # Trouver tous les matches avec leur contexte
            matches = pattern.finditer(doc.texte)

            # Parcourir les correspondances pour construire le concordancier
            for match in matches:
                contexte_gauche, motif_trouve, contexte_droit = match.groups()
                # Nettoyage afin d'éliminer les espaces multiples créés par de nouveaux sauts de ligne ou d'espaces
                contexte_gauche = ' '.join(contexte_gauche.split())
                contexte_droit = ' '.join(contexte_droit.split())
                concordance_list.append((contexte_gauche, motif_trouve, contexte_droit))

        # Créer un DataFrame avec les résultats
        concordance_df = pd.DataFrame(concordance_list, columns=['contexte gauche', 'motif trouvé', 'contexte droit'])

        return concordance_df

# ============== STATISTIQUES TD6 =====================
    def nettoyer_texte(self, texte):
        texte = texte.lower()
        texte = re.sub(r'[\n\t]', ' ', texte)  # Remplacer les retours à la ligne et les tabulations par des espaces
        texte = re.sub(r'[^a-zA-Z0-9\s]', ' ', texte)  # Retirer la ponctuation
        texte = re.sub(r'\s+', ' ', texte)  # Remplacer de multiples espaces par un seul espace
        return texte.strip()

    def stats(self, n):
        vocabulaire = set()
        word_counts = Counter()
        doc_freq = Counter()

        for doc in self.id2doc.values():
            # Nettoyer le texte du document
            cleaned_text = self.nettoyer_texte(doc.texte)
            
            # Obtenir les mots uniques pour la document frequency
            mots_uniques = set(cleaned_text.split())
            # Mettre à jour le compteur de document frequency
            doc_freq.update(mots_uniques)

            # Construire le vocabulaire (sans doublons grâce au set)
            vocabulaire.update(mots_uniques)            
            
            # Compter les occurrences de tous les mots pour term frequency
            word_counts.update(cleaned_text.split())

        # Préparer le tableau freq avec pandas.
        freq = pd.DataFrame(word_counts.items(), columns=['mot', 'term_frequency'])
        # Ajout de la document frequency.
        freq['doc_frequency'] = freq['mot'].apply(lambda x: doc_freq[x])

        # Trier pour obtenir les n mots les plus fréquents.
        freq = freq.sort_values(by='term_frequency', ascending=False)
        
        # Afficher le nombre de mots différents et les n mots les plus fréquents
        print(f"Nombre de mots différents dans le corpus : {len(vocabulaire)}")
        print(f"Les {n} mots les plus fréquents sont:")
        print(freq.head(n))

        # Retourner le tableau freq pour utilisation future si nécessaire
        return freq
# ============== MATRICE DOCUMENT TD7 =====================
    """Avec la contribution de ChatGPT"""
    # Créer un dictionnaire de vocabulaire
    def build_vocab(self):
        vocab = {}
        word_id = 0

        # Boucler sur tous les documents pour construire le vocabulaire
        for doc in self.id2doc.values():
            cleaned_text = self.nettoyer_texte(doc.texte)
            words = set(cleaned_text.split())

            for word in words:
                if word not in vocab:
                    vocab[word] = {
                        'id': word_id,
                        'total_occurrences': 0  # Cette valeur sera mise à jour plus tard
                    }
                    word_id += 1
        
        # Trier le vocabulaire par ordre alphabétique des mots
        vocab = dict(sorted(vocab.items()))

        # Maintenant, calculons les occurrences totales pour chaque mot
        for doc in self.id2doc.values():
            cleaned_text = self.nettoyer_texte(doc.texte)
            words = cleaned_text.split()

            for word in words:
                if word in vocab:  # Assurez-vous que le mot est dans le vocab
                    vocab[word]['total_occurrences'] += 1

        self.vocab = vocab
        
        return vocab
    
    # Créer matrice Term Frequency (TF)
    def build_tf_matrix(self):
        # S'assurer que le vocabulaire est à jour
        self.build_vocab()

        # Préparer les données pour construire la matrice creuse
        documents = list(self.id2doc.values())
        num_docs = len(documents)
        vocab_size = len(self.vocab)
        # Row, Column et Value pour construire la matrice creuse
        rows = []
        cols = []
        data = []

        # Remplir les listes pour les termes de chaque document
        for doc_idx, doc in enumerate(documents):
            word_counter = Counter(doc.texte.lower().split())  # S'assurer que le texte est en minuscule
            for word, count in word_counter.items():
                if word in self.vocab:  # Vérifier si le mot est dans self.vocab
                    word_idx = self.vocab[word]['id']  # Index du mot dans la matrice (col)
                    rows.append(doc_idx)  # Index du document dans la matrice (row)
                    cols.append(word_idx)
                    data.append(count)  # Nombre d'occurrences du mot dans le document (data)
                else:
                    # Gérer le cas oú le mot n'est pas trouvé. Par exemple : 
                    # - Ajouter une condition pour l'ajouter au vocabulaire 
                    # - Avertir que le mot n'est pas dans le vocabulaire.
                    print(f"Le mot '{word}' n'est pas dans le vocabulaire.")

        # Création de la matrice TF creuse
        self.tf_matrix = csr_matrix((data, (rows, cols)), shape=(num_docs, vocab_size))
        return self.tf_matrix
    
    # calculer le nombre total d’occurrences
    def update_vocab_with_doc_frequency(self):
        if not hasattr(self, 'tf_matrix'):
            raise Exception("La matrice TF n'a pas été construite.")
        
        # Calcul du nombre de documents contenant chaque mot
        binary_matrix = self.tf_matrix.copy()
        binary_matrix.data = np.ones_like(self.tf_matrix.data)
        doc_count = binary_matrix.sum(axis=0)

        # Mise à jour de vocab avec le nombre total d’occurrences et le document count
        for word, value in self.vocab.items():
            word_id = value['id']
            value['doc_count'] = doc_count[0, word_id]  # Le nombre de documents où le mot apparait
            value['total_occurrences'] = self.tf_matrix[:, word_id].sum()  # La somme des occurrences dans tous les documents
        
        return self.vocab  # Retourner le dictionnaire vocab mis à jour
    
    # calculer la 2e matrice mat_TFxIDF
    def build_tfidf_matrix(self):
        # Si le vocabulaire ou la matrice TF n'est pas encore créé, le créer
        if not hasattr(self, 'tf_matrix'):
            self.build_tf_matrix()

        # Nombre total de documents dans le corpus
        num_docs = self.tf_matrix.shape[0] 

        # Calculer l'IDF pour chaque terme dans vocab
        # IDF(t) = log_e(Total number of documents / Number of documents with term t in it)
        idfs = []
        for term_info in self.vocab.values():
            term_idf = np.log(num_docs / (1 + term_info['doc_count']))  # +1 pour éviter la division par zéro
            idfs.append(term_idf)
        idfs = np.array(idfs)

        # Créer la matrice TFxIDF en multipliant les éléments de TF par leurs idfs correspondants
        # Pour cela nous devons aligner idfs à être une matrice diagonale pour la multiplication
        self.mat_TFxIDF = self.tf_matrix.multiply(idfs)
        
        return self.mat_TFxIDF
    
    