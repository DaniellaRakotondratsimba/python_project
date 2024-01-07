#Créer le générateur de documents td5

from Classes import RedditDocument, ArxivDocument
import datetime

class DocumentFactory:
    @staticmethod
    def create_document(nature, doc):
        if nature == "ArXiv":
            titre = doc["title"].replace('\n', '')
            authors = ", ".join([a["name"] for a in doc["author"]]) if "author" in doc else ""
            summary = doc["summary"].replace("\n", "") if "summary" in doc else ""
            date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d") if "published" in doc else ""
            return ArxivDocument(titre, authors, date, doc["id"], summary)
        elif nature == "Reddit":
            titre = doc.title.replace("\n", '')
            auteur = str(doc.author)
            date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
            url = "https://www.reddit.com/"+doc.permalink
            texte = doc.selftext.replace("\n", "")
            return RedditDocument(titre, auteur, date, url, texte)
        else:
            raise ValueError("Nature de document non supportée.")