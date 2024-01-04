from flask import Blueprint, current_app, jsonify
import os
from datetime import datetime
from wiki.constants import *
from wiki.config import get_config_settings
from ..utils.utils import validate_path
from flask_babel import _

pages_index = Blueprint("pages_index", __name__)

@pages_index.route('/index', defaults={'path': ''})
@pages_index.route('/index/<path:path>')
def index(path):
    ca_config = get_config_settings(current_app)

    # Validierung ob der Pfad innerhalb des Datenverzeichnisses liegt
    try:
        validate_path(ca_config[CONFIGFILE_KEY_DATA_DIR], path)
    except ValueError as e:
        return jsonify(statuscode=401, message=str(e)), 401

    full_path = os.path.join(ca_config[CONFIGFILE_KEY_DATA_DIR], path)

    if not os.path.isdir(full_path+MARKDOWN_FILE_EXTENSION):
        return jsonify(statuscode=400, messager=MSG_INVALID_PATH), 400

    try:
        content=list_dir(ca_config[CONFIGFILE_KEY_DATA_DIR], '')
    except Exception as e:
        return jsonify(statuscode=400, messager=str(e)), 400


# Listet alle Dateien und Verzeichnisses des uebergebenen Verzeichnisses auf
# und liefert eine Liste von Dictionaries zurueck
def list_dir(data_dir, dir):
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


