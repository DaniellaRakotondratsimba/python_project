# Correction de G. Poux-Médard, 2021-2022

from Classes import Author

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




