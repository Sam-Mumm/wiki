from flask import Blueprint, current_app, request, jsonify
from ..utils.whoosh_search import search_index
from wiki.constants import *
from wiki.config import get_config_settings
from flask_babel import _

pages_search = Blueprint("pages_search", __name__, template_folder='templates')

#@pages_search.before_app_first_request
@pages_search.route('/search', methods=["GET"])
def search():
    if "s" not in request.args:
        return jsonify(statuscode=400, message=_(MSG_NO_SEARCH_PHRASE)), 400

    ca_config = get_config_settings(current_app)

    hits, results = search_index(request.args['s'],
                                ca_config[CONFIGFILE_KEY_INDEX_DIR],
                                ca_config[CONFIGFILE_KEY_DATA_DIR])

    return jsonify(statuscode=200, hits=hits, results=results), 200
