import markdown2
import codecs
import os

def readMarkDown(path):
    return markdown2.markdown_path(path, extras=["tables", "fenced-code-blocks"])

def readRaw(path):
    with codecs.open(path, 'r', 'utf-8') as fh:
        content = fh.read()
    return content

# Die Methode aktualisiert einen Artikel und gibt True zurueck wenn es erfolgreich war, sonst False
def writeRaw(path, content):
    try:
        with codecs.open(path, 'w', 'utf-8') as fh:
            fh.write(content)
    except Exception as e:
        return False

    return True

def moveArticle(src, dest, content):
    success = (False, False)

    # Konnte der Artikel vor dem verschieben aktualisiert werden?
    if writeRaw(src, content):
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