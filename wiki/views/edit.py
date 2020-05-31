from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash
from .article_form import ArticleForm
from flask_babel import _
from .file_io import readRaw, updateArticle, moveArticle
from .whoosh_search import update_document_index
import os, sys

pages_edit = Blueprint("pages_edit", __name__)

@pages_edit.route('/edit', defaults={'path': 'home'}, methods=["GET","POST"])
@pages_edit.route('/edit/<path:path>', methods=["GET","POST"])
def edit(path):
    # Holen der Einstellungen aus der settings.py
    data_dir = current_app.config['DATA_DIR']
    index_dir = current_app.config['INDEX_DIR']
    start_site = current_app.config['START_SITE']
    wiki_name = current_app.config['WIKI_NAME']

    form = ArticleForm()

    # Which Buttons should shown? (here: Index)
    navi_buttons = [
        {'endpoint': 'pages_index.index', 'path': '', 'name': 'Index'},
    ]

    # Wurde der Speicher-Button gedrueckt?
    if request.method == 'POST':

        # wurde der Abbruch-Button gedrueckt?
        if "cancel" in request.form:
            return redirect(url_for('pages_view.home') + path)

        form_content = request.form['article_content']

        if 'path' in request.form:
            form_path = request.form['path'].replace(" ", "_").strip(os.path.sep)
            redirect_path=form_path
        else:
            redirect_path=""
            form_path = "README"
            path=form_path

        try:
            form.validate_path(data_dir, form_path)
        except Exception as e:
            form.article_content.data = form_content
            form.path.data = form_path
            return render_template('article_form.tmpl.html', form=form, navi=navi_buttons, wiki_name=wiki_name, error=str(e))

#        form_comment = request.form['comment']     -> wird erst fuer die Commit Message benoetigt

        article_full_form_path = os.path.join(data_dir, form_path + ".md")
        article_full_orign_path = os.path.join(data_dir, path + ".md")

        # Wurde der Artikel auch verschoben?
        if article_full_orign_path == article_full_form_path:
            # Versuche den Artikel zu aktualisieren
            try:
                updateArticle(article_full_orign_path, form_content)
            except Exception as e:
                flash(str(e))
                return redirect(url_for('pages_view.home') + redirect_path)
        else:
            # Versuche den Artikel zu verschieben
            try:
                moveArticle(article_full_orign_path, article_full_form_path, form_content)
            except Exception as e:
                flash(str(e))
                return redirect(url_for('pages_view.home') + redirect_path)

        # Versuche den Index zu aktualisieren
        try:
           update_document_index(index_dir, data_dir, path, form_path, form_content)
        except Exception as e:
           flash(str(e))

        flash(_("Der Artikel wurde erfolgreich aktualisiert"))
        return redirect(url_for('pages_view.home') + redirect_path)

    # Ist die zu bearbeitende Seite die Startseite?
    if path != 'home':
        article_file = os.path.join(data_dir, path + ".md")

        if not os.path.isfile(article_file):
            return render_template('404.tmpl.html', wiki_name=wiki_name)

        form.path.data=path

        try:
            form.article_content.data=readRaw(article_file)
        except Exception as e:
            flash(str(e))
            return redirect(url_for('pages_view.home'))
    else:
        form .path.data = 'home'

        start_site_absolute = os.path.join(data_dir, start_site)
        if os.path.isfile(start_site_absolute):
            try:
                form.article_content.data = readRaw(start_site_absolute)
            except Exception as e:
                flash(str(e))
                return redirect(url_for('pages_view.home'))
        else:
            form.article_content.data=""

    return render_template('article_form.tmpl.html', form=form, navi=navi_buttons, wiki_name=wiki_name)