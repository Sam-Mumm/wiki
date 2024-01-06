from flask import Blueprint, current_app, jsonify, abort
from flask_babel import _
import os
from ..utils.file_io import readArticle, list_files
from wiki.constants import *
from wiki.config import get_config_settings

pages_view = Blueprint("pages_view", __name__, template_folder='templates')

# Route zum anzeigen eines Artikels
@pages_view.route('/', defaults={'path': 'home'}, methods=['GET'])
@pages_view.route('/<path:path>', methods=['GET'])
def view(path):
    ca_config = get_config_settings(current_app)

    if path == "home":
        path = ca_config[CONFIGFILE_KEY_START_SITE]

    try:
        status, content = load_article(ca_config[CONFIGFILE_KEY_DATA_DIR], path)
    except Exception as e:
        return jsonify(statuscode=e.args[0], message=e.args[1]), e.args[0]

    return jsonify(statuscode=status, content=content), status

def load_article(data_dir, path):
    full_path = os.path.splitext(os.path.join(data_dir, path))[0]

    try:
        content = readArticle(full_path+MARKDOWN_FILE_EXTENSION)
    except Exception as e:
        raise Exception(e.args[0], e.args[1])

    return 200, content
