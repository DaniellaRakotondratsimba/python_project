#============= Test des  deux classes filles =========
#Imports appropriés
from Classes import Document, RedditDocument, ArxivDocument
from Corpus import Corpus

# Crée des instances de RedditDocument et ArxivDocument
reddit_doc1 = RedditDocument(titre="Reddit Post 1", auteur="redditor1", date="2023-01-01", url="http://reddit.com/r/example1", texte="Example text 1", nb_commentaires=10)
reddit_doc2 = RedditDocument(titre="Reddit Post 2", auteur="redditor2", date="2023-02-01", url="http://reddit.com/r/example2", texte="Example text 2", nb_commentaires=20)

arxiv_doc1 = ArxivDocument(titre="Arxiv Paper 1", auteur="author1", date="2023-01-15", url="http://arxiv.org/abs/1234.5678v1", texte="Abstract 1", co_auteurs=["coauthor1", "coauthor2"])
arxiv_doc2 = ArxivDocument(titre="Arxiv Paper 2", auteur="author2", date="2023-02-15", url="http://arxiv.org/abs/2345.6789v1", texte="Abstract 2")

# Crée une instance de Corpus.
mon_corpus = Corpus("Mon Corpus de Documents")

# Ajoute les documents Reddit et Arxiv à l'instance de Corpus.
mon_corpus.add(reddit_doc1)
mon_corpus.add(reddit_doc2)
mon_corpus.add(arxiv_doc1)
mon_corpus.add(arxiv_doc2)

# Teste l'affichage du Corpus pour vérifier que tout est en ordre.
print(mon_corpus)  # Cela invoque __repr__ ou __str__ selon votre implémentation
mon_corpus.show() # Cela affiche les documents en utilisant la méthode show

#============== Test methode search =========================
# Création d'instances de Document avec du texte à rechercher
doc1 = Document(titre="Document 1", texte="Ceci est un texte de test avec le mot Huawei.")
doc2 = Document(titre="Document 2", texte="Un autre texte sans texte le mot-clé.")
doc3 = Document(titre="Document 3", texte="Huawei texte fait partie de ce texte aussi.")

# Création du corpus et ajout des documents
corpus = Corpus("TestCorpus")
corpus.add(doc1)
corpus.add(doc2)
corpus.add(doc3)

# Appel de la fonction search pour chercher le mot "Huawei"
results = corpus.search(["texte"])
print(results)
# Vérification et impression des résultats
if not results:
    print("Aucun résultat trouvé.")
# else:
    # for result in results:
    #     print(f"Résultat trouvé : {result}")

#============== Test methode concorde =========================
# Utilisation de la méthode concorde pour rechercher "texte"
expression_recherchee = "texte"
context_size = 20  # Nombre de caractères avant et après le terme pour le contexte
concordance_results = corpus.concorde(expression_recherchee, context_size)

# Afficher le DataFrame des résultats
print("Résultats de concordance pour 'texte':")
print("concordance:", concordance_results)

#============== Test methode stats =========================
freq_table = corpus.stats(3)

#============== Test methode build_vocab =========================
# Construction du vocabulaire
vocab = corpus.build_vocab()

# Test : Affichage des premiers éléments pour vérifier
for word, info in list(vocab.items())[:10]:  # Modifier ce nombre pour voir plus ou moins de résultats
    print(f"Mot: {word}, ID: {info['id']}, Occurrences totales: {info['total_occurrences']}")

# Vous pouvez également tester pour un mot spécifique
test_word = 'exemple'  # Remplacez ceci par un mot de votre choix qui est susceptible d'être dans votre corpus
if test_word in vocab:
    print(f"Test pour le mot '{test_word}':", vocab[test_word])
else:
    print(f"Le mot '{test_word}' n'est pas dans le vocabulaire.") 