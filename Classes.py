# Correction de G. Poux-Médard, 2021-2022
# Insertion et modification code HNR TDR

# =============== 2.1 : La classe Document ===============
class Document:
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte="", doc_type=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.doc_type = doc_type  # Ajout du nouveau champ pour identifier le type de document
    
    def getType(self):
        return self.doc_type
# =============== 2.2 : REPRESENTATIONS ===============
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\tType: {self.getType()}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.titre}, par {self.auteur} , type: {self.getType()}"

# =============== 2.4 : La classe Author ===============
class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []
# =============== 2.5 : ADD ===============
    def add(self, production):
        self.ndoc += 1
        self.production.append(production)
    def __str__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"

#=============== Les classes filles TD5 =================
# Partie 1 : class RedditDocument
class RedditDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="", nb_commentaires=0):
        super().__init__(titre, auteur, date, url, texte)
        self._nb_commentaires = nb_commentaires  # Utilisation de l'underscore pour indiquer un attribut protégé

    # Accesseur (getter) pour le nombre de commentaires
    @property
    def nb_commentaires(self):
        return self._nb_commentaires

    # Mutateur (setter) pour le nombre de commentaires
    @nb_commentaires.setter
    def nb_commentaires(self, valeur):
        if isinstance(valeur, int) and valeur >= 0:
            self._nb_commentaires = valeur
        else:
            raise ValueError("Le nombre de commentaires doit être un entier positif")
   
    # Typer reddit
    def getType(self):
        return "Reddit"
    
    def __str__(self):
        base = super().__str__()
        return f"{base}\tNombre de commentaires : {self._nb_commentaires}"
    
# Partie 2 : classe ArxivDocument
class ArxivDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="", co_auteurs=None):
        super().__init__(titre, auteur, date, url, texte)
        self.co_auteurs = co_auteurs if co_auteurs is not None else []

    # Typer arxiv 
    def getType(self):
        return "Arxiv"
    
    def __str__(self):
        base_str = super().__str__()  # Appel la méthode de la classe parent, qui inclut l'auteur principal
        co_authors_str = "\tCo-auteurs : " + ", ".join(self.co_auteurs) if self.co_auteurs else ""
        return f"{base_str}{co_authors_str}"
    