from flask import Blueprint, jsonify, current_app, request
from flask_babel import _
from ..utils.utils import validate_path
from ..utils.file_io import updateArticle
from ..utils.whoosh_search import update_document_index
import os
from wiki.constants import *
from wiki.config import get_config_settings

pages_edit = Blueprint("pages_edit", __name__, template_folder='templates')

@pages_edit.route('/edit', defaults={'path': 'home'}, methods=["POST"])
@pages_edit.route('/edit/<path:path>', methods=["POST"])
def edit(path):
    ca_config=get_config_settings(current_app)
    data = request.get_json()

    if path == "home":
        path=ca_config[CONFIGFILE_KEY_START_SITE]

    status, msg = data_processing(ca_config[CONFIGFILE_KEY_DATA_DIR],
                                  ca_config[CONFIGFILE_KEY_INDEX_DIR],
                                  path,
                                  data['content'])

    return jsonify(statuscode=status, message=msg), status


def data_processing(data_dir, index_dir, path, content):
    full_path = os.path.join(data_dir, path + MARKDOWN_FILE_EXTENSION)

    # Validierung ob der Pfad innerhalb des Datenverzeichnisses liegt
    try:
        validate_path(data_dir, path)
    except ValueError as e:
        return jsonify(statuscode=401, message=str(e)), 401

    try:
        updateArticle(full_path, content)
    except Exception as e:
        return jsonify(statuscode=500, message=str(e)), 500

    # Versuche den Index zu aktualisieren
    try:
        update_document_index(index_dir, data_dir, path, content)
    except Exception as e:
        return jsonify(statuscode=500, message=str(e)), 500

    return jsonify(statuscode=200, message=_(MSG_UPDATE_SUCCESSFUL)), 200
