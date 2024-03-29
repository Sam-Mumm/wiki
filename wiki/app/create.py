from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash
from ..utils.file_io import createArticle
from .article_form import ArticleForm
from ..utils.whoosh_search import add_document_index
import os
from wiki.constants import *
from wiki.config import all_endpoints, get_config_settings

pages_create = Blueprint("pages_create", __name__, template_folder='templates')


@pages_create.route('/create', defaults={'path': ''}, methods=["GET","POST"])
@pages_create.route('/create/<path:path>', methods=["GET","POST"])
def create(path):
    ca_config=get_config_settings(current_app)

    start_site_full_path = os.path.join(ca_config[CONFIGFILE_KEY_DATA_DIR], ca_config[CONFIGFILE_KEY_START_SITE])

    form = ArticleForm()

    # Which Buttons should shown? (here: Index)
    navi_buttons = [all_endpoints.get('index')]

    if request.method == HTTP_REQUEST_METHOD_POST:
        return form_processing(ca_config[CONFIGFILE_KEY_DATA_DIR],
                               form,
                               ca_config[CONFIGFILE_KEY_INDEX_DIR],
                               navi_buttons, path,
                               ca_config[CONFIGFILE_KEY_WIKI_NAME])

    if path == "home" and not os.path.isfile(start_site_full_path):
        form.path.data = "home"
    elif path == "home" and os.path.exists(start_site_full_path) or path=="":
        form.path.data = ""
    else:
        form.path.data = path + os.path.sep

    return render_template(TEMPLATE_ARTICLE_FORM, form=form, navi=navi_buttons, wiki_name=wiki_name)


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
        return render_template(TEMPLATE_ARTICLE_FORM, form=form, navi=navi_buttons, wiki_name=wiki_name,
                               error=str(e))

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