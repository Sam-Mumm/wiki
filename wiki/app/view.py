from flask import Blueprint, render_template, current_app, redirect, url_for, flash
from flask_babel import _
import os
from ..utils.file_io import readMarkDown
from wiki.constants import *
from wiki.config import all_endpoints

pages_view = Blueprint("pages_view", __name__, template_folder='templates')

# Route zum anzeigen eines Artikels
@pages_view.route('/', defaults={'path': 'home'})
@pages_view.route('/<path:path>')
def home(path):
    # Which Buttons should shown? (Create, Index)
    navi_element = all_endpoints.get('create')
    navi_element['parameter'] = {'path': path}

    navi_buttons = [all_endpoints.get('index'), navi_element]

    data_dir=current_app.config[CONFIGFILE_KEY_DATA_DIR]
    wiki_name=current_app.config[CONFIGFILE_KEY_WIKI_NAME]
    start_site=current_app.config[CONFIGFILE_KEY_START_SITE]

    # Wurde eine Dateiendung mit angegeben?
    if path.endswith(MARKDOWN_FILE_EXTENSION):
        return redirect(url_for('pages_view.home')+os.path.splitext(path)[0])

    if path != 'home':
        full_path = os.path.join(data_dir, path)

        if os.path.isfile(full_path + MARKDOWN_FILE_EXTENSION):
            navi_element=all_endpoints.get('edit')
            navi_element['parameter'] = { 'path': path }
            navi_buttons.append(navi_element)

            try:
                content = readMarkDown(full_path + MARKDOWN_FILE_EXTENSION)
            except Exception as e:
                return render_template('404.tmpl.html', navi=navi_buttons, wiki_name=wiki_name)

            return render_template('markdown_content.tmpl.html', content=content, navi=navi_buttons, wiki_name=wiki_name)
        elif os.path.isdir(full_path):
            return redirect(url_for('pages_index.index', path=path))
        else:
            return render_template('404.tmpl.html', navi=navi_buttons, wiki_name=wiki_name)
    else:
        start_site_full_path = os.path.join(data_dir, start_site)

        if os.path.exists(start_site_full_path):
            try:
                content = readMarkDown(start_site_full_path)
            except Exception as e:
                flash(str(e))
        else:
            content = "<h1>"+_('Willkommen')+"</h1>"

        return render_template('markdown_content.tmpl.html', content=content, navi=navi_buttons, wiki_name=wiki_name)

