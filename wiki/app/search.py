from flask import Blueprint, render_template, current_app, request
from flask_babel import _
from ..utils.whoosh_search import search_index, create_index
import os
from wiki.constants import *
from wiki.config import all_endpoints

pages_search = Blueprint("pages_search", __name__, template_folder='templates')

@pages_search.before_app_first_request
def index_refresh():
    index_dir = os.path.abspath(current_app.config[CONFIGFILE_KEY_INDEX_DIR])
    data_dir = current_app.config[CONFIGFILE_KEY_DATA_DIR]

    if not os.path.isdir(index_dir):
        try:
            os.makedirs(index_dir)
        except:
            raise PermissionError(_(MSG_INDEX_DIR_CANNOT_BE_CREATED))

    if not os.path.isdir(os.path.abspath(data_dir)):
        try:
            os.makedirs(os.path.abspath(data_dir))
        except:
            raise PermissionError(_(MSG_DATA_DIR_CANNOT_BE_CREATED))

    create_index(index_dir, data_dir)

@pages_search.route('/search', methods=["POST", "GET"])
def search():
    results = []
    index_dir = current_app.config[CONFIGFILE_KEY_INDEX_DIR]
    data_dir = current_app.config[CONFIGFILE_KEY_DATA_DIR]
    wiki_name = current_app.config[CONFIGFILE_KEY_WIKI_NAME]

    # Which Buttons should shown? (Create, Index)
    navi_buttons = [all_endpoints.get('index'), all_endpoints.get('create')]

    if request.method != HTTP_REQUEST_METHOD_POST:
        msg = _(MSG_NO_SEARCH_PHRASE)
        return render_template('search_results.tmpl.html', search_msg=msg, results=results, navi=navi_buttons, wiki_name=wiki_name)

    search_str = request.form['search']

    msg, results = search_index(search_str, index_dir, data_dir)

    return render_template('search_results.tmpl.html', search_msg=msg, results=results, navi=navi_buttons, wiki_name=wiki_name)