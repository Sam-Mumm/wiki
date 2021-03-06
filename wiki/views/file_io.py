from flask_babel import _
import markdown2
import codecs
import os

# Auslesen eines Artikels (=Datei) einschliesslich Markdown-Parsing
def readMarkDown(path):
    try:
        return markdown2.markdown_path(path, extras=["tables", "fenced-code-blocks", "break-on-newline"])
    except:
        raise PermissionError(_("Der Artikel konnte nicht gelesen werden, bitte die Zugriffsrechte überprüfen"))


# Auslesen eines Artikels (=Datei) ohne Parsing
def readRaw(path):
    try:
        with codecs.open(path, 'r', 'utf-8') as fh:
            content = fh.read()
    except:
        raise PermissionError(_("Der Artikel konnte nicht gelesen werden, bitte die Zugriffsrechte überprüfen"))

    return content


# Aktualisiert einen Artikel und gibt True zurueck wenn es erfolgreich war, sonst False
def updateArticle(path, content):
    try:
        with codecs.open(path, 'w+', 'utf-8') as fh:
            fh.write(content)
    except:
        raise PermissionError(_("Der Artikel konnte nicht geschrieben werden, bitte die Zugriffsrechte prüfen"))

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
        raise OSError(_("Die Verzeichnisse konnten nicht erstellt werden"))

    # Pruefen ob an dem Ziel bereits eine Datei/ein Verzeichnis mit dem gleichen Namen existiert
    if os.path.exists(dest):
        raise FileExistsError(_("Der Artikel konnte nicht verschoben werden, es existiert bereits eine Datei mit dem gleichen Namen"))

    # Den Artikel umzubennen / verschieben
    try:
        os.rename(src, dest)
    except PermissionError:
        raise PermissionError(_("Der Artikel konnte nicht verschoben werden, bitte die Zugriffsrechte prüfen"))

    return True


# Erstellt einen neuen Artikel
def createArticle(article_fullpath, content):
    # Existiert bereits eine Datei/Verzeichnis mit dem gleichen Namen?
    if os.path.exists(article_fullpath):
        raise FileExistsError(_("Es existiert bereits eine Datei mit dem gleichen Namen"))

    # extrahieren des Verzeichnisnamens aus dem Pfad
    dest_path = os.path.dirname(article_fullpath)

    # Versuche das Verzeichnis zu erstellen
    try:
        os.makedirs(dest_path, exist_ok=True)
    except Exception as e:
        raise OSError(_("Die Verzeichnisse konnten nicht erstellt werden"))

    return updateArticle(article_fullpath, content)