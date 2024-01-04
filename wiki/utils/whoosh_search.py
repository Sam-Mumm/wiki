from whoosh.fields import *
import whoosh.index
from whoosh.qparser import QueryParser
from whoosh.filedb.filestore import FileStorage
from whoosh.highlight import ContextFragmenter
import os, shutil
import codecs
from flask_babel import _
from wiki.constants import *

# Erstellt von data_dir einen neuen Index in index_dir.
# Liefert True zurueck, falls die indizierung erfolgreich war
def create_index(index_dir, data_dir):
    if not os.path.isdir(index_dir):
        try:
            os.makedirs(index_dir)
        except:
            raise PermissionError(_(MSG_INDEX_DIR_CANNOT_BE_CREATED))

    if not os.path.isdir(os.path.abspath(data_dir)):
        try:
            os.makedirs(os.path.abspath(data_dir))
        except:
            raise PermissionError(_(MSG_DATA_DIR_CANNOT_BE_CREATED))

    schema = Schema(path=ID(stored=True, unique=True), content=TEXT(stored=True))

    storage_obj = FileStorage(index_dir)

    if whoosh.index.exists_in(index_dir):
        try:
            shutil.rmtree(index_dir)
            os.makedirs(index_dir)
        except:
            raise PermissionError(_(MSG_INDEX_DIR_CANNOT_BE_CREATED))

    idx = storage_obj.create_index(schema)

    writer = idx.writer()

    # Iteriere über alle Dateien die auf .md enden
    for (path, dirs, files) in os.walk(data_dir):
        # Remove the git-Folder
        if GIT_SYS_FOLDER in dirs:
            dirs.remove(GIT_SYS_FOLDER)

        for article in files:
            if article.endswith(MARKDOWN_FILE_EXTENSION):
                article_path=os.path.join(os.path.relpath(path, data_dir).strip('./'), article)

                try:
                    # Get file content
                    with codecs.open(os.path.join(path, article), "r", "utf-8") as f:
                        content = f.read()
                        writer.add_document(path=article_path, content=content)
                except:
                    continue

    writer.commit()

    return True


def search_index(search_str, index_dir, data_dir):
    result_set = []
    index_dir_absolute = os.path.abspath(index_dir)

    storage_obj = FileStorage(index_dir_absolute)

    try:
        idx=storage_obj.open_index()
    except whoosh.index.EmptyIndexError:
        create_index(index_dir, data_dir)
        idx=storage_obj.open_index()

    query_obj=QueryParser("content", idx.schema).parse(search_str)
    searcher = idx.searcher()
    results = searcher.search(query_obj)

    results.fragmenter = whoosh.highlight.ContextFragmenter(surround=20)

    for r in results:
        hit = {}

        hit['path'] = r['path']
#        hit['content'] = r.highlights("content")
        result_set.append(hit)

    return len(results), result_set


def add_document_index(index_dir, data_dir, path, content):
    index_dir_absolute = os.path.abspath(index_dir)
    storage_obj = FileStorage(index_dir_absolute)

    try:
        idx=storage_obj.open_index()
    except whoosh.index.EmptyIndexError:
        create_index(index_dir, data_dir)
        idx=storage_obj.open_index()

    writer = idx.writer()
    writer.add_document(path=path, content=content)
    writer.commit()
    return True


def update_document_index(index_dir, data_dir, path, content):
    index_dir_absolute = os.path.abspath(index_dir)
    storage_obj = FileStorage(index_dir_absolute)

    try:
        idx=storage_obj.open_index()
    except whoosh.index.EmptyIndexError:
        create_index(index_dir, data_dir)
        idx=storage_obj.open_index()

    writer = idx.writer()

    writer.update_document(path=path, content=content)
    writer.commit()