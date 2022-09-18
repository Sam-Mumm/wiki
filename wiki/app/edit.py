from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash
from .article_form import ArticleForm
from flask_babel import _
from ..utils.file_io import readRaw, updateArticle, moveArticle
from ..utils.whoosh_search import update_document_index
import os
from wiki.constants import *
from wiki.config import all_endpoints, get_config_settings

pages_edit = Blueprint("pages_edit", __name__, template_folder='templates')

@pages_edit.route('/edit', defaults={'path': 'home'}, methods=["GET","POST"])
@pages_edit.route('/edit/<path:path>', methods=["GET","POST"])
def edit(path):
    ca_config=get_config_settings(current_app)

    form = ArticleForm()

    # Which Buttons should shown? (Create, Index)
    navi_element = all_endpoints.get('create')
    navi_element['parameter'] = {'path': path}

    navi_buttons = [all_endpoints.get('index'), navi_element]

    # Wurde der Speicher-Button gedrueckt?
    if request.method == HTTP_REQUEST_METHOD_POST:
        return form_processing(ca_config[CONFIGFILE_KEY_DATA_DIR],
                               form,
                               ca_config[CONFIGFILE_KEY_INDEX_DIR],
                               navi_buttons, path,
                               ca_config[CONFIGFILE_KEY_WIKI_NAME])

    return load_form_data(ca_config[CONFIGFILE_KEY_DATA_DIR], form,
                          navi_buttons, path,
                          ca_config[CONFIGFILE_KEY_START_SITE],
                          ca_config[CONFIGFILE_KEY_WIKI_NAME])


def load_form_data(data_dir, form, navi_buttons, path, start_site, wiki_name):
    form.article_content.data = ""

    # Ist die zu bearbeitende Seite die Startseite?
    if path != 'home':
        article_file = os.path.join(data_dir, path + MARKDOWN_FILE_EXTENSION)

        if not os.path.isfile(article_file):
            return render_template(TEMPLATE_ARTICLE_NOT_FOUND, wiki_name=wiki_name)

        form.path.data = path

        try:
            form.article_content.data = readRaw(article_file)
        except Exception as e:
            flash(str(e))
            return redirect(url_for('pages_view.home'))
    else:
        form.path.data = 'home'

        start_site_absolute = os.path.join(data_dir, start_site)
        if os.path.isfile(start_site_absolute):
            try:
                form.article_content.data = readRaw(start_site_absolute)
            except Exception as e:
                flash(str(e))
                return redirect(url_for('pages_view.home'))

    return render_template(TEMPLATE_ARTICLE_FORM, form=form, navi=navi_buttons, wiki_name=wiki_name)


def form_processing(data_dir, form, index_dir, navi_buttons, path, wiki_name):
    # wurde der Abbruch-Button gedrueckt?
    if "cancel" in request.form:
        return redirect(url_for('pages_view.home', path=path))

    form_content = request.form['article_content']

    if 'path' in request.form:
        form_path = request.form['path'].replace(" ", "_").strip(os.path.sep)
        redirect_path = form_path
    else:
        redirect_path = ""
        form_path = "README"
        path = form_path

    try:
        form.validate_path(data_dir, form_path)
    except Exception as e:
        form.article_content.data = form_content
        form.path.data = form_path
        return render_template(TEMPLATE_ARTICLE_FORM, form=form, navi=navi_buttons, wiki_name=wiki_name,
                               error=str(e))

    #        form_comment = request.form['comment']     -> wird erst fuer die Commit Message benoetigt

    article_full_form_path = os.path.join(data_dir, form_path + MARKDOWN_FILE_EXTENSION)
    article_full_origin_path = os.path.join(data_dir, path + MARKDOWN_FILE_EXTENSION)

    # Wurde der Artikel auch verschoben?
    if article_full_origin_path == article_full_form_path:
        # Versuche den Artikel zu aktualisieren
        try:
            updateArticle(article_full_origin_path, form_content)
        except Exception as e:
            flash(str(e))
            return redirect(url_for('pages_view.home', path=redirect_path))
    else:
        # Versuche den Artikel zu verschieben
        try:
            moveArticle(article_full_origin_path, article_full_form_path, form_content)
        except Exception as e:
            flash(str(e))
            return redirect(url_for('pages_view.home') + '/'.join(request.path.split("/")[2:]))

    # Versuche den Index zu aktualisieren
    try:
        update_document_index(index_dir, data_dir, path, form_path, form_content)
    except Exception as e:
        flash(str(e))

    flash(_(MSG_UPDATE_SUCCESSFUL))
    return redirect(url_for('pages_view.home', path=redirect_path))