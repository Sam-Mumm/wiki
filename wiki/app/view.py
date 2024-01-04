from flask import Blueprint, current_app, redirect, jsonify, url_for
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
        print(str(e))
        return jsonify(statuscode=404,
                       message=_(MSG_PAGE_NOT_FOUND)), 404

    return jsonify(statuscode=status, content=content), status

def load_article(data_dir, path):
    full_path = os.path.join(data_dir, path)

    if os.path.isdir(full_path):
        return 200, list_files(data_dir, path)
 
    try:
        content = readArticle(full_path+MARKDOWN_FILE_EXTENSION)
    except Exception as e:
        raise Exception(str(e))

    return 200, content
