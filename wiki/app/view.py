from flask import Blueprint, render_template, current_app, redirect, url_for, flash, jsonify
from flask_babel import _
import os
from ..utils.file_io import readArticle
from ..utils.utils import markdown2html
from wiki.constants import *
from wiki.config import all_endpoints, get_config_settings

pages_view = Blueprint("pages_view", __name__, template_folder='templates')

# Route zum anzeigen eines Artikels
@pages_view.route('/', defaults={'path': 'home'})
@pages_view.route('/<path:path>')
def home(path):
    # Which Buttons should shown? (Create, Index)
    navi_element = all_endpoints.get('create')
    navi_element['parameter'] = {'path': os.path.dirname(path)}

    ca_config=get_config_settings(current_app)

    # Wurde eine Dateiendung mit angegeben?
    if path.endswith(MARKDOWN_FILE_EXTENSION):
        return redirect(url_for('pages_view.home')+os.path.splitext(path)[0])
    try:
        if path == 'home':
            navi_element['parameter'] = {'path': path}

            status, content = load_startsite(ca_config[CONFIGFILE_KEY_DATA_DIR],
                                                 ca_config[CONFIGFILE_KEY_START_SITE])
        else:
            navi_element['parameter'] = {'path': os.path.dirname(path)}
            status, content = load_article(ca_config[CONFIGFILE_KEY_DATA_DIR], path)
    except Exception as e:
        navi_buttons = [all_endpoints.get('index'), navi_element]

        return render_template(TEMPLATE_ARTICLE_NOT_FOUND,
                               navi=navi_buttons,
                               wiki_name=ca_config[CONFIGFILE_KEY_WIKI_NAME])

    navi_buttons = [all_endpoints.get('index'), navi_element]

    return render_template(TEMPLATE_ARTICLE_CONTENT_MARKDOWN,
                           content=markdown2html(content),
                           navi=navi_buttons,
                           wiki_name=ca_config[CONFIGFILE_KEY_WIKI_NAME])


@pages_view.route('/rest/content', defaults={'path': 'home'})
@pages_view.route('/rest/content/<path:path>')
def rest_home(path):
    ca_config = get_config_settings(current_app)

    # Wurde eine Dateiendung mit angegeben?
    if path.endswith(MARKDOWN_FILE_EXTENSION):
        return redirect(url_for('pages_view.home/rest/content') + os.path.splitext(path)[0])

    try:
        if path == 'home':
            status, content = load_startsite(ca_config[CONFIGFILE_KEY_DATA_DIR],
                                             ca_config[CONFIGFILE_KEY_START_SITE])
        else:
            status, content = load_article(ca_config[CONFIGFILE_KEY_DATA_DIR], path)
    except Exception as e:
        return jsonify(status="404", content=_(JSON_PAGE_NOT_FOUND))

    return jsonify(status=status, content=content)


def load_article(data_dir, path):
    full_path = os.path.join(data_dir, path)

    if os.path.isfile(full_path + MARKDOWN_FILE_EXTENSION):
        try:
            content = readArticle(full_path + MARKDOWN_FILE_EXTENSION)
        except Exception as e:
            raise FileNotFoundError()
    elif os.path.isdir(full_path):
        return redirect(url_for('pages_index.index', path=path))
    else:
        raise FileNotFoundError()

    return 200, content


def load_startsite(data_dir, start_site):
    start_site_full_path = os.path.join(data_dir, start_site)

    # TODO: Durch sinnvollen Text (externe Datei?) ersetzen
    content = "<h1>" + _('Willkommen') + "</h1>"

    if os.path.exists(start_site_full_path):
        try:
            content = readArticle(start_site_full_path)
        except Exception as e:
            flash(str(e))

    return 200, content

