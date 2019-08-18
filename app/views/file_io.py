import markdown2
import codecs

def readMarkDown(path):
    return markdown2.markdown_path(path, extras=["tables", "fenced-code-blocks"])

def readRaw(path):
    with codecs.open(path, 'r', 'utf-8') as fh:
        content = fh.read()
    return content

def updateArticle(path, content):
    with codecs.open(path, 'w', 'utf-8') as fh:
        fh.write(content)
