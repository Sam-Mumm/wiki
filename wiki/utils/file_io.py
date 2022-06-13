from flask_babel import _
import markdown2
import codecs
import os
from wiki.constants import *

# Auslesen eines Artikels (=Datei) einschliesslich Markdown-Parsing
def readMarkDown(path):
    try:
        return markdown2.markdown_path(path, extras=["tables", "fenced-code-blocks", "break-on-newline"])
    except:
        raise PermissionError(_(MSG_NO_READ_PERMISSION))


# Auslesen eines Artikels (=Datei) ohne Parsing
def readRaw(path):
    try:
        with codecs.open(path, 'r', 'utf-8') as fh:
            content = fh.read()
    except:
        raise PermissionError(_(MSG_NO_READ_PERMISSION))

    return content


# Aktualisiert einen Artikel und gibt True zurueck wenn es erfolgreich war, sonst False
def updateArticle(path, content):
    try:
        with codecs.open(path, 'w+', 'utf-8') as fh:
            fh.write(content)
    except:
        raise PermissionError(_(MSG_NO_WRITE_PERMISSION))

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
        raise OSError(_(MSG_DIR_CANNOT_BE_CREATED))

    # Pruefen ob an dem Ziel bereits eine Datei/ein Verzeichnis mit dem gleichen Namen existiert
    if os.path.exists(dest):
        raise FileExistsError(_(MSG_FILE_CANNOT_BE_MOVED_SAME_NAME_EXISTS))

    # Den Artikel umzubennen / verschieben
    try:
        os.rename(src, dest)
    except PermissionError:
        raise PermissionError(_(MSG_FILE_CANNOT_BE_MOVE_NO_PERMISSION))

    return True


# Erstellt einen neuen Artikel
def createArticle(article_fullpath, content):
    # Existiert bereits eine Datei/Verzeichnis mit dem gleichen Namen?
    if os.path.exists(article_fullpath):
        raise FileExistsError(_(MSG_FILE_CANNOT_BE_CREATE_SAME_NAME_EXISTS))

    # extrahieren des Verzeichnisnamens aus dem Pfad
    dest_path = os.path.dirname(article_fullpath)

    # Versuche das Verzeichnis zu erstellen
    try:
        os.makedirs(dest_path, exist_ok=True)
    except Exception as e:
        raise OSError(_(MSG_DIR_CANNOT_BE_CREATED))

    return updateArticle(article_fullpath, content)