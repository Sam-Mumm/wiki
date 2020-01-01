import os
import sys
import shutil
from wiki.views import file_io
import pytest
from tempfile import mkdtemp
import codecs

@pytest.fixture()
def tempdir():
    tempdir = mkdtemp()
    yield tempdir
    shutil.rmtree(tempdir)

articles = [
                { "dir": "",
                  "filename": "README.md",
                  "content_md": "# Hallo Welt",
                  "content_html": "<h1>Hallo Welt</h1>\n"
                },
                { "dir": "test",
                  "filename": "article.md",
                  "content_md": "# Hallo Welt",
                  "content_html": "<h1>Hallo Welt</h1>\n"
                }
    ]


@pytest.mark.parametrize("article", articles)
def test_readRaw(tempdir, article):
    dest_path=os.path.join(tempdir, article['dir'])
    os.makedirs(dest_path, exist_ok=True)

    with codecs.open(os.path.join(dest_path, article['filename']), 'w', 'utf-8') as fh:
        fh.write(article['content_md'])

    assert file_io.readRaw(os.path.join(dest_path, article['filename'])) == article['content_md']


@pytest.mark.parametrize("article", articles)
def test_readRaw_no_permissions(tempdir, article):
    dest_path=os.path.join(tempdir, article['dir'])
    os.makedirs(dest_path, exist_ok=True)

    os.mknod(os.path.join(dest_path, article['filename']), 0o200)

    with pytest.raises(PermissionError, match="konnte nicht gelesen werden, bitte die Zugriffsrechte überprüfen"):
        file_io.readRaw(os.path.join(dest_path, article['filename']))


@pytest.mark.parametrize("article", articles)
def test_readMarkDown(tempdir, article):
    dest_path=os.path.join(tempdir, article['dir'])
    os.makedirs(dest_path, exist_ok=True)

    with codecs.open(os.path.join(dest_path, article['filename']), 'w', 'utf-8') as fh:
        fh.write(article['content_md'])

    assert file_io.readMarkDown(os.path.join(dest_path, article['filename'])) == article['content_html']


@pytest.mark.parametrize("article", articles)
def test_readMarkDown_no_permissions(tempdir, article):
    dest_path=os.path.join(tempdir, article['dir'])
    os.makedirs(dest_path, exist_ok=True)

    with codecs.open(os.path.join(dest_path, article['filename']), 'w', 'utf-8') as fh:
        fh.write(article['content_md'])

    os.chmod(os.path.join(dest_path, article['filename']), 0o200)

    with pytest.raises(PermissionError, match="konnte nicht gelesen werden, bitte die Zugriffsrechte überprüfen"):
        assert file_io.readMarkDown(os.path.join(dest_path, article['filename'])) == article['content_html']


@pytest.mark.parametrize("article", articles)
def test_createArticle(tempdir, article):
    dest_path = os.path.join(tempdir, article['dir'])

    assert file_io.createArticle(os.path.join(dest_path, article['filename']), article['content_md'])
    assert os.path.exists(os.path.join(dest_path, article['filename']))

    with codecs.open(os.path.join(dest_path, article['filename']), 'r', 'utf-8') as fh:
        assert fh.read() == article['content_md']


@pytest.mark.parametrize("article", articles)
def test_createArticle_no_permissions(tempdir, article):
    dest_path = os.path.join(tempdir, article['dir'])

    os.chmod(tempdir, 0o400)

    if article['dir'] == "":
        with pytest.raises(PermissionError, match="konnte nicht geschrieben werden, bitte die Zugriffsrechte prüfen"):
            file_io.createArticle(os.path.join(dest_path, article['filename']), article['content_md'])
    else:
        with pytest.raises(OSError, match="Die Verzeichnisse konnten nicht erstellt werden"):
            file_io.createArticle(os.path.join(dest_path, article['filename']), article['content_md'])


@pytest.mark.parametrize("article", articles)
def test_createArticle_file_exists(tempdir, article):
    dest_path = os.path.join(tempdir, article['dir'])
    os.makedirs(dest_path, exist_ok=True)

    os.mknod(os.path.join(dest_path, article['filename']))

    with pytest.raises(FileExistsError, match="Es existiert bereits eine Datei mit dem gleichen Namen"):
        file_io.createArticle(os.path.join(dest_path, article['filename']), article['content_md'])


@pytest.mark.parametrize("article", articles)
def test_updateArticle(tempdir, article):
    dest_path = os.path.join(tempdir, article['dir'])
    os.makedirs(dest_path, exist_ok=True)

    os.mknod(os.path.join(dest_path, article['filename']))

    assert file_io.updateArticle(os.path.join(dest_path, article['filename']), article['content_md'])

    with codecs.open(os.path.join(dest_path, article['filename']), 'r', 'utf-8') as fh:
        assert fh.read() == article['content_md']


@pytest.mark.parametrize("article", articles)
def test_updateArticle_no_permissions(tempdir, article):
    dest_path = os.path.join(tempdir, article['dir'])
    os.makedirs(dest_path, exist_ok=True)

    os.mknod(os.path.join(dest_path, article['filename']), 0o400)

    with pytest.raises(PermissionError, match="konnte nicht geschrieben werden, bitte die Zugriffsrechte prüfen"):
        assert file_io.updateArticle(os.path.join(dest_path, article['filename']), article['content_md'])