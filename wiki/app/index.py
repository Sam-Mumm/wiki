from flask import Blueprint, render_template, current_app, redirect, url_for
from flask_babel import _
import os
from datetime import datetime
from ..utils import magic
from wiki.config import all_endpoints

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
        if os.path.isdir(full_entry) and not e == magic.GIT_SYS_FOLDER:
            entry['is_dir'] = True
            entry['name'] = e
            entry['path'] = os.path.join(dir, e)
        elif os.path.isfile(full_entry) and e.endswith(magic.MARKDOWN_FILE_EXTENSION):
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

    if path!='':
        create_path="/" + path
    else:
        create_path=''

    navi_element = all_endpoints.get('create')
    navi_element['parameter'] = {'path': path}
    navi_buttons = [navi_element]

    data_dir=current_app.config[magic.CONFIGFILE_KEY_DATA_DIR]
    wiki_name=current_app.config[magic.CONFIGFILE_KEY_WIKI_NAME]

    full_path = os.path.join(data_dir, path)

    if path:
        # Existiert das in der URL referenzierte Verzeichnis im Daten-Verzeichnis
        if os.path.isdir(full_path):
            content = list_dir(data_dir, path)
            return render_template('table_content.tmpl.html', wiki_name=wiki_name, content=content, navi=navi_buttons)
        # Referenziert der Eintrag in der URL auf eine Datei auf root-Ebene?
        elif os.path.isfile(full_path + magic.MARKDOWN_FILE_EXTENSION):
            return redirect(url_for('pages_view.home', path=path))
        else:
            return render_template('404.tmpl.html')

    else:
        content = list_dir(data_dir, '')
        return render_template('table_content.tmpl.html', wiki_name=wiki_name, content=content, navi=navi_buttons)