from flask import Blueprint, render_template, current_app, redirect, url_for, flash
from flask_babel import _
import os
from ..utils.file_io import readMarkDown
from ..utils import magic

pages_view = Blueprint("pages_view", __name__, template_folder='templates')

# Route zum anzeigen eines Artikels
@pages_view.route('/', defaults={'path': 'home'})
@pages_view.route('/<path:path>')
def home(path):
    # Which Buttons should shown? (Edit, Index)
    navi_buttons = [
        {'endpoint': 'pages_index.index', 'path': '', 'name': magic.LBL_INDEX}
    ]

    data_dir=current_app.config[magic.CONFIGFILE_KEY_DATA_DIR]
    wiki_name=current_app.config[magic.CONFIGFILE_KEY_WIKI_NAME]
    start_site=current_app.config[magic.CONFIGFILE_KEY_START_SITE]

    # Wurde eine Dateiendung mit angegeben?
    if path.endswith(magic.MARKDOWN_FILE_EXTENSION):
        return redirect(url_for('pages_view.home')+os.path.splitext(path)[0])
    if path != 'home':
        full_path = os.path.join(data_dir, path)

        if os.path.isfile(full_path + magic.MARKDOWN_FILE_EXTENSION):
            navi_buttons.append(
                {'endpoint': 'pages_edit.edit', 'path': "/" + path, 'name': _(magic.LBL_EDIT)}
            )

            try:
                content = readMarkDown(full_path + magic.MARKDOWN_FILE_EXTENSION)
            except Exception as e:
                return render_template('404.tmpl.html', navi=[], wiki_name=wiki_name)

            return render_template('markdown_content.tmpl.html', content=content, navi=navi_buttons, wiki_name=wiki_name)
        elif os.path.isdir(full_path):
            return redirect(url_for('pages_index.index')+"/"+path)
        else:
            return render_template('404.tmpl.html', navi=[], wiki_name=wiki_name)
    else:
        start_site_full_path = os.path.join(data_dir, start_site)

        if os.path.exists(start_site_full_path):

            try:
                content = readMarkDown(start_site_full_path)
            except Exception as e:
                flash(str(e))
                content = "<h1>"+_('Willkommen')+"</h1>"

            navi_buttons.append(
                {'endpoint': 'pages_edit.edit', 'path': "/" + path, 'name': _(magic.LBL_EDIT)}
            )
        else:
            navi_buttons.append(
                {'endpoint': 'pages_create.create', 'path': "", 'name': _(magic.LBL_CREATE)}
            )

            content="<h1>"+_('Willkommen')+"</h1>"

        return render_template('markdown_content.tmpl.html', content=content, navi=navi_buttons, wiki_name=wiki_name)

