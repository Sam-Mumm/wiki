from flask import Blueprint, render_template, current_app, redirect, url_for
import os
from datetime import datetime
from wiki.constants import *
from wiki.config import all_endpoints, get_config_settings

pages_index = Blueprint("pages_index", __name__)

# Listet alle Dateien und Verzeichnisses des uebergebenen Verzeichnisses auf
# und liefert eine Liste von Dictionaries zurueck
def list_dir(data_dir, dir):
    dir_content = []

    full_path = os.path.join(data_dir, dir)

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
    return dir_content


@pages_index.route('/index', defaults={'path': ''})
@pages_index.route('/index/<path:path>')
def index(path):
    navi_element = all_endpoints.get('create')
    navi_element['parameter'] = {'path': path}
    navi_buttons = [navi_element]

    ca_config = get_config_settings(current_app)

    full_path = os.path.join(ca_config[CONFIGFILE_KEY_DATA_DIR], path)

    if path:
        # Existiert das in der URL referenzierte Verzeichnis im Daten-Verzeichnis
        if os.path.isdir(full_path):
            content = list_dir(ca_config[CONFIGFILE_KEY_DATA_DIR], path)
            return render_template(TEMPLATE_TABLE, wiki_name=ca_config[CONFIGFILE_KEY_WIKI_NAME], content=content, navi=navi_buttons)
        # Referenziert der Eintrag in der URL auf eine Datei auf root-Ebene?
        elif os.path.isfile(full_path + MARKDOWN_FILE_EXTENSION):
            return redirect(url_for('pages_view.home', path=path))
        else:
            return render_template(TEMPLATE_ARTICLE_NOT_FOUND)

    else:
        content = list_dir(ca_config[CONFIGFILE_KEY_DATA_DIR], '')
        return render_template(TEMPLATE_TABLE, wiki_name=ca_config[CONFIGFILE_KEY_WIKI_NAME], content=content, navi=navi_buttons)