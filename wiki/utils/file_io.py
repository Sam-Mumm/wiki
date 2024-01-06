from flask_babel import _
import codecs
import os
from wiki.constants import *
from datetime import datetime

# Auslesen eines Artikels (=Datei) ohne Parsing
def readArticle(path):
    try:
        with codecs.open(path, 'r', 'utf-8') as fh:
            content = fh.read()
    except Exception as e:
        raise Exception(404, _(MSG_PAGE_NOT_FOUND))

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

# Listet alle Dateien und Verzeichnisses des uebergebenen Verzeichnisses auf
# und liefert eine Liste von Dictionaries zurueck
def list_files(data_dir, dir):
    dir_content = []

    full_path = os.path.join(data_dir, dir)

    try:
        for e in os.listdir(full_path):
            full_entry = os.path.join(data_dir, dir, e)

            entry = {'name': None, 'isdir': None, 'path': None, 'size': None, 'mtime': None, 'ctime': None}

            # Auflisten von Verzeichnissen und Dateien ohne, welche die Endung *.md haben
            if os.path.isdir(full_entry) and not e == GIT_SYS_FOLDER:
                entry['is_dir'] = True
                entry['name'] = e
                entry['path'] = os.path.join(dir, e)
            elif os.path.isfile(full_entry) and e.endswith(MARKDOWN_FILE_EXTENSION):
                entry['size'] = os.path.getsize(full_entry)
                entry['name'] = e[:-3]
                entry['path'] = os.path.join(dir, e[:-3])
            else:
                continue

            entry['mtime'] = datetime.fromtimestamp(os.path.getmtime(full_entry)).strftime('%Y-%m-%d %H:%M')
            entry['ctime'] = datetime.fromtimestamp(os.path.getctime(full_entry)).strftime('%Y-%m-%d %H:%M')

            dir_content.append(entry)
    except Exception as e:
        raise PermissionError(_(MSG_DATA_DIR_CANNOT_BE_READ)+str(e))
    return dir_content
