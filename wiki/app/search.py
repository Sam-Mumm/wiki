from flask import Blueprint, render_template, current_app, request
from flask_babel import _
from ..utils.whoosh_search import search_index, create_index
import os

pages_search = Blueprint("pages_search", __name__, template_folder='templates')

@pages_search.before_app_first_request
def index_refresh():
    index_dir = os.path.abspath(current_app.config['INDEX_DIR'])
    data_dir = current_app.config['DATA_DIR']

    if not os.path.isdir(index_dir):
        try:
            os.makedirs(index_dir)
        except:
            raise PermissionError(_("Das Index-Verzeichnis konnte nicht erstellt werden"))

    if not os.path.isdir(os.path.abspath(data_dir)):
        try:
            os.makedirs(os.path.abspath(data_dir))
        except:
            raise PermissionError(_("Das Daten-Verzeichnis konnte nicht erstellt werden"))

    create_index(index_dir, data_dir)

@pages_search.route('/search', methods=["POST", "GET"])
def search():
    results = []
    index_dir = current_app.config['INDEX_DIR']
    data_dir = current_app.config['DATA_DIR']
    wiki_name = current_app.config['WIKI_NAME']

    navi_buttons = [
        {'endpoint': 'pages_index.index', 'path': '', 'name': 'Index'}
    ]

    if request.method != 'POST':
        msg = _("Es wurde kein Suchbegriff angegeben")
        return render_template('search_results.tmpl.html', search_msg=msg, results=results, navi=navi_buttons, wiki_name=wiki_name)

    search_str = request.form['search']

    msg, results = search_index(search_str, index_dir, data_dir)

    return render_template('search_results.tmpl.html', search_msg=msg, results=results, navi=navi_buttons, wiki_name=wiki_name)