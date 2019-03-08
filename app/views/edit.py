from flask import Blueprint, render_template, current_app
from article_form import ArticleForm

pages_edit = Blueprint("pages_edit", __name__)

def read_article(path):
    content="Lorem ipsum"
    template="kekse"
    return content, template
#    return "Lorem ipsum"



@pages_edit.route('/edit', defaults={'path': 'home'}, methods=["GET","POST"])
@pages_edit.route('/edit/<path:path>', methods=["GET","POST"])
def edit(path):

    form = ArticleForm()

    # Which Buttons should shown? (here: Index)
    navi_buttons = [
        {'endpoint': 'page_index.index', 'path': '', 'name': 'Index'},
    ]

    content, template=read_article(path)
    form.article_content.data=content
    form.path.data=template

    return render_template('article_form.tmpl.html', form=form)
