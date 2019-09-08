import markdown2
import codecs
import os

# Auslesen eines Artikels (=Datei) einschliesslich Markdown-Parsing
def readMarkDown(path):
    try:
        return markdown2.markdown_path(path, extras=["tables", "fenced-code-blocks"])
    except:
        raise PermissionError("Der Artikel konnte nicht gelesen werden, bitte die Zugriffsrechte überprüfen")


# Auslesen eines Artikels (=Datei) ohne Parsing
def readRaw(path):
    try:
        with codecs.open(path, 'r', 'utf-8') as fh:
            content = fh.read()
    except:
        raise PermissionError("Der Artikel konnte nicht gelesen werden, bitte die Zugriffsrechte überprüfen")

    return content


# Aktualisiert einen Artikel und gibt True zurueck wenn es erfolgreich war, sonst False
def updateArticle(path, content):
    try:
        with codecs.open(path, 'w+', 'utf-8') as fh:
            fh.write(content)
    except:
        raise PermissionError("Der Artikel konnte nicht geschrieben werden, bitte die Zugriffsrechte prüfen")

    return True


# Verschiebt einen Artikel und gibt bei Erfolg true zurueck
def moveArticle(src, dest, content):
    # Versuche den Artikel zu aktualisieren
    updateArticle(src, content)

    # Versuche die Verzeichnisstruktur anzulegen
    dest_path = os.path.dirname(dest)
    try:
        os.makedirs(dest_path, exist_ok=True)
    except:
        raise PermissionError("Die Verzeichnisse konnten nicht erstellt werden")

    # Den Artikel umzubennen / zu verschieben
    try:
        os.rename(src, dest)
    except FileExistsError:
        raise FileExistsError("Es existiert bereits eine Datei mit dem gleichen Namen")

    return True


# Erstellt einen neuen Artikel
def createArticle(article_fullpath, content):
    # Existiert der Zielpfad?
    dest_path = os.path.dirname(article_fullpath)

    # Versuche das Verzeichnis zu erstellen
    try:
        os.makedirs(dest_path, exist_ok=True)
    except Exception as e:
        raise PermissionError("Die Verzeichnisse konnten nicht erstellt werden")

    return updateArticle(article_fullpath, content)