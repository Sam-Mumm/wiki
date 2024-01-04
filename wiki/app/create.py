from flask import Blueprint, jsonify, current_app, request
from ..utils.file_io import createArticle
from ..utils.whoosh_search import add_document_index
from ..utils.utils import validate_path
import os
from wiki.constants import *
from wiki.config import get_config_settings

pages_create = Blueprint("pages_create", __name__, template_folder='templates')


@pages_create.route('/create', defaults={'path': ''}, methods=["POST"])
@pages_create.route('/create/<path:path>', methods=["POST"])
def create(path):
    ca_config=get_config_settings(current_app)
    data = request.get_json()

    if path == "home":
        path = ca_config[CONFIGFILE_KEY_START_SITE]

    status, msg = data_processing(ca_config[CONFIGFILE_KEY_DATA_DIR],
                                  ca_config[CONFIGFILE_KEY_INDEX_DIR],
                                  path,
                                  data['content'])

    if msg!="":
        return "", 201
    else:
        return jsonify(statuscode=status, message=msg), status


def data_processing(data_dir, index_dir, path, content):
    full_path = os.path.join(data_dir, path + MARKDOWN_FILE_EXTENSION)

    try:
        validate_path(data_dir, path)
    except Exception as e:
        return jsonify(statuscode=401, message=str(e)), 401

    try:
        createArticle(full_path, content)
    except Exception as e:
        return jsonify(statuscode=500, message=str(e)), 500

    # Aktualisieren des Suchindex
    try:
        add_document_index(index_dir, data_dir, form_path, form_content)
    except Exception as e:
        return jsonify(statuscode=500, message=str(e)), 500

    return 201, ""
