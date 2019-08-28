from flask import Blueprint, render_template, current_app, request, redirect, url_for
from whoosh.fields import *
import whoosh.index
from whoosh.qparser import QueryParser
import os, sys
from whoosh.filedb.filestore import FileStorage
import codecs

pages_search = Blueprint("pages_search", __name__)

@pages_search.before_app_first_request
def refresh_search_db():

    index_dir = current_app.config['INDEX_DIR']
    data_dir = current_app.config['DATA_DIR']

    storage_obj = FileStorage(os.path.abspath(index_dir))

    schema = Schema(path=ID(stored=True, unique=True), content=TEXT(stored=True))

    # Schema of the index
    idx = storage_obj.create_index(schema)

    writer = idx.writer()

    # Iterate over the data_dir and add the contents to the index
    for (path, dirs, files) in os.walk(data_dir):
        # Remove the git-Folder
        if '.git' in dirs:
            dirs.remove('.git')

        for article in files:
            if article.endswith('.md'):
                article_path=path+"/"+article

            # Get file content
            with codecs.open(article_path, "r", "utf-8") as f:
                content = f.read()
                writer.add_document(path=article_path, content=content)
    writer.commit()


@pages_search.route('/search', methods=["POST", "GET"])
def search():
    if request.method != 'POST':
        return redirect(url_for('pages_view.home'))

    navi_buttons = [
        {'endpoint': 'pages_index.index', 'path': '', 'name': 'Index'}
    ]

    index_dir = current_app.config['INDEX_DIR']

    search_str = request.form['search']

    storage_obj = FileStorage(os.path.abspath(index_dir))

    try:
        idx=storage_obj.open_index()
    except whoosh.index.EmptyIndexError:
        refresh_search_db
        idx=storage_obj.open_index()

    query_obj=QueryParser("content", idx.schema).parse(search_str)
    searcher = idx.searcher()
    results = searcher.search(query_obj)

    return render_template('search_results.tmpl.html', results=results, navi=navi_buttons)
