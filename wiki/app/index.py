from flask import Blueprint, current_app, jsonify
import os
from wiki.constants import *
from wiki.config import get_config_settings
from ..utils.utils import validate_path
from ..utils.file_io import list_files

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

    if os.path.isdir(full_path):
        try:
            content = list_files(ca_config[CONFIGFILE_KEY_DATA_DIR], path)
            return jsonify(statuscode=200, content=content), 200

        except Exception as e:
            return jsonify(statuscode=400, messager=str(e)), 400

    return jsonify(statuscode=400, messager=MSG_INVALID_PATH), 400


