from flask import Blueprint, render_template, current_app
from article_form import ArticleForm

pages_create = Blueprint("pages_create", __name__)

@pages_create.route('/create', defaults={'path': ''})
@pages_create.route('/create/<path:path>')
def create(path):
    # Which Buttons should shown? (here: Index)
    navi_buttons = [
        {'endpoint': 'pages_index.index', 'path': '', 'name': 'Index'},
    ]

    form = ArticleForm()

    return render_template('article_form.tmpl.html', form=form, navi=navi_buttons)