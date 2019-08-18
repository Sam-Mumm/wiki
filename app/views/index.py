from flask import Blueprint, render_template, current_app, redirect, url_for
import os, sys
import markdown2
from datetime import datetime

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
        if os.path.isdir(full_entry) and not e==".git":
            entry['is_dir'] = True
            entry['name'] = e
            entry['path'] = os.path.join(dir, e)
        elif os.path.isfile(full_entry) and e.endswith('.md'):
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
    # Which Buttons should shown? (here: Create)
    navi_buttons = [
        {'endpoint': 'pages_create.create', 'path': '', 'name': 'Erstellen'},
    ]

    data_dir=current_app.config['DATA_DIR']
    wiki_name=current_app.config['WIKI_NAME']

    full_path = os.path.join(data_dir, path)

    if path:
        # Existiert das in der URL referenzierte Verzeichnis im Daten-Verzeichnis
        if os.path.isdir(full_path):
            content = list_dir(data_dir, path)
            return render_template('table_content.tmpl.html', wiki_name=wiki_name, content=content, navi=navi_buttons)
        # Referenziert der Eintrag in der URL auf eine Datei auf root-Ebene?
        elif os.path.isfile(full_path+".md"):
            return redirect(url_for('pages_view.home')+path)
        else:
            return render_template('404.tmpl.html')

    else:
        content = list_dir(data_dir, '')
        return render_template('table_content.tmpl.html', wiki_name=wiki_name, content=content, navi=navi_buttons)