from flask import Blueprint, render_template, current_app, request, redirect, url_for
from .article_form import ArticleForm
from .file_io import readRaw, updateArticle, moveArticle
import os, sys

pages_edit = Blueprint("pages_edit", __name__)

# Pruefung und speichern der Aenderunngen nach dem absenden von dem Formular
def store_article(data_dir, origin_path, content, new_path):
    new_article_file = os.path.join(data_dir, new_path + ".md")

    print("origin: "+origin_path)
    print("new_path"+new_path)
    if origin_path == new_path:
        updateArticle(new_article_file, content)
    else:
        origin_article_file = os.path.join(data_dir, origin_path + ".md")

        moveArticle(origin_article_file, new_article_file, content)

    return True


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
        form_content = request.form['article_content']

        if 'path' in request.form:
            form_path = request.form['path'].replace(" ", "_").strip(os.path.sep)
            redirect_path=form_path
        else:
            redirect_path=""
            form_path = "README"
            path=form_path

#        form_comment = request.form['comment']     -> wird erst fuer die Commit Message benoetigt

        # Konnte die Datei erfolgreich gespeichert werden?
        if store_article(data_dir, path, form_content, form_path):
            return redirect(url_for('pages_view.home') + redirect_path)

    # Ist die zu bearbeitende Seite die Startseite?
    if path != 'home':
        article_file = os.path.join(data_dir, path + ".md")

        if not os.path.isfile(article_file):
            return render_template('404.tmpl.html')

        form.path.data=path
        form.article_content.data=readRaw(article_file)
    else:
        form.path.data = 'home'

        if os.path.isfile(data_dir+"/"+start_site):
            form.article_content.data = readRaw(data_dir+"/"+start_site)
        else:
            form.article_content.data=""

    return render_template('article_form.tmpl.html', form=form, navi=navi_buttons)
