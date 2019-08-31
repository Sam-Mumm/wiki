import markdown2
import codecs
import os

# Auslesen eines Artikels (=Datei) einschliesslich Markdown-Parsing
def readMarkDown(path):
    return markdown2.markdown_path(path, extras=["tables", "fenced-code-blocks"])


# Auslesen eines Artikels (=Datei) ohne Parsing
def readRaw(path):
    with codecs.open(path, 'r', 'utf-8') as fh:
        content = fh.read()
    return content


# Aktualisiert einen Artikel und gibt True zurueck wenn es erfolgreich war, sonst False
def updateArticle(path, content):
    try:
        with codecs.open(path, 'w+', 'utf-8') as fh:
            fh.write(content)
    except Exception as e:
        return False

    return True


# Verschiebt einen Artikel und gibt true zurueck falls es erfolgreich war, sonst false
def moveArticle(src, dest, content):
    success = (False, False)

    # Konnte der Artikel vor dem verschieben aktualisiert werden?
    if updateArticle(src, content):
        success = (True, False)
    else:
        return success

    # Existiert der Zielpfad?
    dest_path = os.path.dirname(dest)
    if not os.path.isdir(dest_path):
        try:
            os.makedirs(dest_path, exist_ok=True)
        except Exception as e:
            return success

    # Existiert bereits eine Zieldatei mit dem gleichen Namen?
    if os.path.exists(dest):
        return success

    os.rename(src, dest)

    return success


# Erstellt einen neuen Artikel
def createArticle(article_fullpath, content):
    # Existiert der Zielpfad?
    dest_path = os.path.dirname(article_fullpath)

    if not os.path.isdir(dest_path):
        try:
            os.makedirs(dest_path, exist_ok=True)
        except Exception as e:
            return False

    return updateArticle(article_fullpath, content)