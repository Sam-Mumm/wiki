from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash
from ..utils.file_io import createArticle
from .article_form import ArticleForm
from ..utils.whoosh_search import add_document_index
import os
from wiki.constants import *
from wiki.config import all_endpoints

pages_create = Blueprint("pages_create", __name__, template_folder='templates')


@pages_create.route('/create', defaults={'path': ''}, methods=["GET","POST"])
@pages_create.route('/create/<path:path>', methods=["GET","POST"])
def create(path):
    data_dir = current_app.config[CONFIGFILE_KEY_DATA_DIR]
    index_dir = current_app.config[CONFIGFILE_KEY_INDEX_DIR]
    start_site = current_app.config[CONFIGFILE_KEY_START_SITE]
    wiki_name = current_app.config[CONFIGFILE_KEY_WIKI_NAME]

    start_site_full_path = os.path.join(data_dir, start_site)

    form = ArticleForm()

    # Which Buttons should shown? (here: Index)
    navi_buttons = [all_endpoints.get('index')]

    if request.method == HTTP_REQUEST_METHOD_POST:
        return form_processing(data_dir, form, index_dir, navi_buttons, path, wiki_name)

    if path == "home" and not os.path.isfile(start_site_full_path):
        form.path.data = "home"
    elif path == "home" and os.path.exists(start_site_full_path) or path=="":
        form.path.data = ""
    else:
        form.path.data = path + os.path.sep

    return render_template('article_form.tmpl.html', form=form, navi=navi_buttons, wiki_name=wiki_name)


def form_processing(data_dir, form, index_dir, navi_buttons, path, wiki_name):
    # wurde der Abbruch-Button gedrueckt?
    if "cancel" in request.form and path != "home":
        return redirect(url_for('pages_view.index', path=path))
    elif "cancel" in request.form and path == "home":
        return redirect(url_for('pages_view.home'))

    form_content = request.form['article_content']

    if 'path' in request.form:
        form_path = request.form['path'].replace(" ", "_").strip(os.path.sep)
        redirect_path = form_path
    else:
        redirect_path = ""
        form_path = "README"

    try:
        form.validate_path(data_dir, form_path)
    except Exception as e:
        form.article_content.data = form_content
        form.path.data = form_path
        return render_template('article_form.tmpl.html', form=form, navi=navi_buttons, wiki_name=wiki_name,
                               error=str(e))

#        form_comment = request.form['comment']     -> wird erst fuer die Commit Message benoetigt

    article_fullpath = os.path.join(data_dir, form_path + MARKDOWN_FILE_EXTENSION)

    try:
        createArticle(article_fullpath, form_content)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('pages_view.home'))

    # Aktualisieren des Suchindex
    try:
        add_document_index(index_dir, data_dir, form_path, form_content)
    except Exception as e:
        flash(str(e))

    return redirect(url_for('pages_view.home', path=redirect_path))