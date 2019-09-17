from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash
from .file_io import createArticle
from .article_form import ArticleForm
from .whoosh_search import add_document_index
import os, sys

pages_create = Blueprint("pages_create", __name__)

@pages_create.route('/create', defaults={'path': 'home'}, methods=["GET","POST"])
@pages_create.route('/create/<path:path>', methods=["GET","POST"])
def create(path):
    data_dir = current_app.config['DATA_DIR']
    index_dir = current_app.config['INDEX_DIR']
    start_site = current_app.config['START_SITE']
    wiki_name = current_app.config['WIKI_NAME']

    start_site_full_path = os.path.join(data_dir, start_site)

    form = ArticleForm()

    # Which Buttons should shown? (here: Index)
    navi_buttons = [
        {'endpoint': 'pages_index.index', 'path': '', 'name': 'Index'},
    ]

    if request.method == 'POST':

        # wurde der Abbruch-Button gedrueckt?
        if "cancel" in request.form:
            return redirect(url_for('pages_view.index') + path)

        form_content = request.form['article_content']

        if 'path' in request.form:
            form_path = request.form['path'].replace(" ", "_").strip(os.path.sep)
            redirect_path=form_path
        else:
            redirect_path=""
            form_path = "README"

#        form_comment = request.form['comment']     -> wird erst fuer die Commit Message benoetigt

        article_fullpath = os.path.join(data_dir, form_path+".md")

        try:
            createArticle(article_fullpath, form_content)
        except Exception as e:
            flash(str(e))
            return redirect(url_for('pages_view.home'))

        try:
            add_document_index(index_dir, data_dir, article_fullpath, form_content)
        except Exception as e:
            flash(str(e))

        return redirect(url_for('pages_view.home') + redirect_path)


    if path == "home" and not os.path.isfile(start_site_full_path):
        form.path.data = "home"
    elif path == "home" and os.path.exists(start_site_full_path):
        form.path.data = ""
    else:
        form.path.data = path+os.path.sep

    return render_template('article_form.tmpl.html', form=form, navi=navi_buttons, wiki_name=wiki_name)