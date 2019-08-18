import markdown2
import codecs
from os import rename

def readMarkDown(path):
    return markdown2.markdown_path(path, extras=["tables", "fenced-code-blocks"])

def readRaw(path):
    with codecs.open(path, 'r', 'utf-8') as fh:
        content = fh.read()
    return content

def writeRaw(path, content):
    with codecs.open(path, 'w', 'utf-8') as fh:
        fh.write(content)

def moveArticle(src, dest, content):
    writeRaw(src, content)

    # Existiert bereits eine Zieldatei mit dem gleichnamen?
    if os.path.exists(dest):
        return False

    rename(src, dest)