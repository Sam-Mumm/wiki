from flask import Blueprint, render_template, current_app, request
from .article_form import ArticleForm
from .file_io import readRaw
import hashlib
import os, sys

pages_edit = Blueprint("pages_edit", __name__)

# Pruefung und speichern der Aenderunngen nach dem absenden von dem Formular
def store_article():
    # Inhalt der Formularfelder holen
    form_content = request.form['article_content']
    form_path = request.form['path']
    form_comment = request.form['comment']






@pages_edit.route('/edit', defaults={'path': 'home'}, methods=["GET","POST"])
@pages_edit.route('/edit/<path:path>', methods=["GET","POST"])
def edit(path):
    # Holen der Einstellungen aus der settings.py
    data_dir = current_app.config['DATA_DIR']
    start_site = current_app.config['START_SITE']

    form = ArticleForm()

    # Which Buttons should shown? (here: Index)
    navi_buttons = [
        {'endpoint': 'pages_index.index', 'path': '', 'name': 'Index'},
    ]

    # Wurde der Speicher-Button gedrueckt?
    if request.method == 'POST':
        store_article()


    # Ist die zu bearbeitende Seite die Startseite?
    if path != 'home':
        article_file = os.path.join(data_dir, path + ".md")

        if not os.path.isfile(article_file):
            return render_template('404.tmpl.html')

        print(path)
        article_path=path
        content=readRaw(article_file)
    else:
        article_path = 'home'

        if os.path.isfile(data_dir+"/"+start_site):
            content = readRaw(data_dir+"/"+start_site)
        else:
            content=""

    form.path.data=article_path
    form.article_content.data=content

    return render_template('article_form.tmpl.html', form=form, navi=navi_buttons)
