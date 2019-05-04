from flask import Blueprint, render_template, current_app, request
from article_form import ArticleForm
from file_io import readRaw
import hashlib
import os, sys

pages_edit = Blueprint("pages_edit", __name__)

@pages_edit.route('/edit', defaults={'path': 'home'}, methods=["GET","POST"])
@pages_edit.route('/edit/<path:path>', methods=["GET","POST"])
def edit(path):
    data_dir = current_app.config['DATA_DIR']
    start_site = current_app.config['START_SITE']

    form = ArticleForm()

    # Which Buttons should shown? (here: Index)
    navi_buttons = [
        {'endpoint': 'pages_index.index', 'path': '', 'name': 'Index'},
    ]

    if request.method == 'POST':
        print "foobar"


    if path != 'home':
        article_file = os.path.join(data_dir, path + ".md")

        if not os.path.isfile(article_file):
            return render_template('404.tmpl.html')

        article_path=path
        content=readRaw(article_file)
        form.checksum.data=hashlib.md5(content.encode('utf-8')).hexdigest()
    else:
        article_path = 'home'

        if os.path.isfile(data_dir+"/"+start_site):
            content = readRaw(data_dir+"/"+start_site)
            form.checksum.data=hashlib.md5(content.encode('utf-8')).hexdigest()
        else:
            content=""

    form.path.data=article_path
    form.article_content.data=content

    return render_template('article_form.tmpl.html', form=form, navi=navi_buttons)
