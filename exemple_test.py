#============= Test des  deux classes filles =========
#Imports appropriés
from Classes import RedditDocument, ArxivDocument
from Corpus import Corpus

# Créez des instances de RedditDocument et ArxivDocument.
reddit_doc1 = RedditDocument(titre="Reddit Post 1", auteur="redditor1", date="2023-01-01", url="http://reddit.com/r/example1", texte="Example text 1", nb_commentaires=10)
reddit_doc2 = RedditDocument(titre="Reddit Post 2", auteur="redditor2", date="2023-02-01", url="http://reddit.com/r/example2", texte="Example text 2", nb_commentaires=20)

arxiv_doc1 = ArxivDocument(titre="Arxiv Paper 1", auteur="author1", date="2023-01-15", url="http://arxiv.org/abs/1234.5678v1", texte="Abstract 1", co_auteurs=["coauthor1", "coauthor2"])
arxiv_doc2 = ArxivDocument(titre="Arxiv Paper 2", auteur="author2", date="2023-02-15", url="http://arxiv.org/abs/2345.6789v1", texte="Abstract 2")

# Créez une instance de Corpus.
mon_corpus = Corpus("Mon Corpus de Documents")

# Ajoutez les documents Reddit et Arxiv à l'instance de Corpus.
mon_corpus.add(reddit_doc1)
mon_corpus.add(reddit_doc2)
mon_corpus.add(arxiv_doc1)
mon_corpus.add(arxiv_doc2)

# Testez l'affichage du Corpus pour vérifier que tout est en ordre.
print(mon_corpus)  # Cela invoque __repr__ ou __str__ selon votre implémentation.
mon_corpus.show() # Cela affiche les documents en utilisant la méthode show. 

