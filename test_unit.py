import unittest
from Classes import Document, RedditDocument, ArxivDocument
from Corpus import Corpus

class TestDocumentSystem(unittest.TestCase):
    def test_document_creation(self):
        # Testez la création d'un document Reddit avec un nombre de commentaires
        reddit_doc = RedditDocument(titre="Reddit Title", auteur="Reddit Author", date="2023-03-14", url="http://reddit.com/r/Example", texte="Example content", nb_commentaires=42)
        self.assertEqual(reddit_doc.nb_commentaires, 42)

        # Testez la création d'un document Arxiv avec une liste d'auteurs
        arxiv_doc = ArxivDocument(titre="Arxiv Title", auteurs=["Alice", "Bob"], date="2023-02-14", url="http://arxiv.org/abs/1234.5678", texte="Abstract")
        self.assertIn("Alice", arxiv_doc.auteurs)
        
    def test_corpus_polymorphism(self):
        # Testez l'ajout de documents Reddit et Arxiv à un corpus
        corpus = Corpus("Test Corpus")
        reddit_doc = RedditDocument("Reddit Test", "Author1", "2023-03-14", "http://reddit.com", "Text", 10)
        arxiv_doc = ArxivDocument("Arxiv Test", ["Author2"], "2023-02-14", "http://arxiv.org", "Text")
        
        corpus.add(reddit_doc)
        corpus.add(arxiv_doc)
        
        self.assertEqual(len(corpus.authors), 2)
        self.assertIsInstance(corpus.id2doc[1], RedditDocument)
        self.assertIsInstance(corpus.id2doc[2], ArxivDocument)

    def test_document_str(self):
        # Testez la méthode __str__ pour s'assurer qu'elle renvoie la chaîne attendue pour chaque type de document
        reddit_doc = RedditDocument("Reddit Test", "Author1", "2023-03-14", "http://reddit.com", "Text", 10)
        arxiv_doc = ArxivDocument("Arxiv Test", ["Author2"], "2023-02-14", "http://arxiv.org", "Text")

        self.assertEqual(str(reddit_doc), "Reddit Test, par Author1\tNombre de commentaires : 10")
        self.assertEqual(str(arxiv_doc), "Arxiv Test, par Author2\tCo-auteurs : Author2")

# Exécutez les tests
if __name__ == '__main__':
    unittest.main()