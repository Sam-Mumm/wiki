from whoosh.fields import *
import whoosh.index
from whoosh.qparser import QueryParser
import os, sys, shutil
from whoosh.filedb.filestore import FileStorage
import codecs

def create_index(index_dir, data_dir):
    index_dir_absolute = os.path.abspath(index_dir)
    schema = Schema(path=ID(stored=True, unique=True), content=TEXT(stored=True))

    storage_obj = FileStorage(index_dir_absolute)

    if whoosh.index.exists_in(index_dir_absolute):
        try:
            shutil.rmtree(index_dir_absolute)
            os.makedirs(index_dir_absolute)
        except e:
            return False

    idx = storage_obj.create_index(schema)

    writer = idx.writer()

    for (path, dirs, files) in os.walk(data_dir):
        # Remove the git-Folder
        if '.git' in dirs:
            dirs.remove('.git')

        for article in files:
            if article.endswith('.md'):
                article_path=path+"/"+article

#            # Get file content
            with codecs.open(article_path, "r", "utf-8") as f:
                content = f.read()
                writer.add_document(path=article_path, content=content)

    writer.commit()

    return True


def search_index(search_str, index_dir, data_dir):
    msg = ""
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

    if len(results) == 0:
        msg = "Es gab fuer den Suchstring "+search_str+" keine Treffer"
        return msg, result_set

    msg = "Es wurden "+str(len(results))+" Treffer fuer die Suchanfrage "+search_str+" gefunden"
    for r in  results:
        hit = {}

        hit['path'] = "/".join(os.path.normpath(r['path']).split(os.path.sep)[3:])
        hit['content'] = r['content']

        result_set.append(hit)

    return msg, result_set


def add_document_index(index_dir, data_dir, path, content):
    index_dir_absolute = os.path.abspath(index_dir)
    storage_obj = FileStorage(index_dir_absolute)

    try:
        idx=storage_obj.open_index()
    except whoosh.index.EmptyIndexError:
        create_index(index_dir, data_dir)
        idx=storage_obj.open_index()
        return True

    writer = idx.writer()
    writer.add_document(path=path, content=content)
    writer.commit()



#def update_document_index(index_dir, data_dir, path, content)