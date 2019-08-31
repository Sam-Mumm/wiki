from flask import Blueprint, render_template, current_app, redirect, url_for
import os, sys
from .file_io import readMarkDown

pages_view = Blueprint("pages_view", __name__)

# Route zum anzeigen eines Artikels
@pages_view.route('/', defaults={'path': 'home'})
@pages_view.route('/<path:path>')
def home(path):
    # Which Buttons should shown? (Edit, Index)
    navi_buttons = [
        {'endpoint': 'pages_index.index', 'path': '', 'name': 'Index'}
    ]

    data_dir=current_app.config['DATA_DIR']

    start_site=current_app.config['START_SITE']

    # Wurde eine Dateiendung mit angegeben?
    if path.endswith(".md"):
        return redirect(url_for('pages_view.home')+os.path.splitext(path)[0])

    if path != 'home':

        full_path = os.path.join(data_dir, path)

        if os.path.isfile(full_path+".md"):

            navi_buttons.append(
                {'endpoint': 'pages_edit.edit', 'path': "/" + path, 'name': 'Bearbeiten'}
            )

            content = readMarkDown(full_path+".md")

            return render_template('markdown_content.tmpl.html', content=content, navi=navi_buttons)
        elif os.path.isdir(full_path):
            return redirect(url_for('pages_index.index')+"/"+path)
        else:
            return render_template('404.tmpl.html')
    else:
        start_site_full_path = os.path.join(data_dir, start_site)

        if os.path.exists(start_site_full_path):
            content = readMarkDown(start_site_full_path)
            navi_buttons.append(
                {'endpoint': 'pages_edit.edit', 'path': "/" + path, 'name': 'Bearbeiten'}
            )
        else:
            navi_buttons.append(
                {'endpoint': 'pages_create.create', 'path': "", 'name': 'Erstellen'}
            )

            content=""
        return render_template('markdown_content.tmpl.html', content=content, navi=navi_buttons)

