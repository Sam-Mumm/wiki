from whoosh.fields import *
import whoosh.index
from whoosh.qparser import QueryParser
import os, sys
from whoosh.filedb.filestore import FileStorage
import codecs

class Search:
    data_dir = None
    storage_obj = None


    def __init__(self, data_dir, index_dir):
        # Get data and index-Directory from the configuration-File
        rs = Settings()
        self.data_dir = data_dir
        index_dir = index_dir

        # Create storage-object
        self.storage_obj = FileStorage(index_dir)

    # Generate a new index in index_dir of data_dir
    def generate_index(self):
        schema = Schema(path=ID(stored=True, unique=True), content=TEXT(stored=True))

        # Schema of the index
        idx = self.storage_obj.create_index(schema)

        writer = idx.writer()

        # Iterate over the data_dir and add the contents to the index
        for (path, dirs, files) in os.walk(self.data_dir):
            # Remove the git-Folder
            if '.git' in dirs:
                dirs.remove('.git')

            # Iterate over the *.md-files in the current directory
            for article in files:
                if article.endswith('.md'):
                    article_path=path+"/"+article

                    # Get file content
                    with codecs.open(article_path, "r", "utf-8") as f:
                        content = f.read()
                        writer.add_document(path=unicode(article_path), content=unicode(content))
        writer.commit()

    def search(self, query_str):
        try:
            idx=self.storage_obj.open_index()
        except whoosh.index.EmptyIndexError:
            self.generate_index()
            idx=self.storage_obj.open_index()

        query_obj=QueryParser("content", idx.schema).parse("SsH")
        searcher = idx.searcher()
        results = searcher.search(query_obj)
        return results

