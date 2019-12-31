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
        ["", "README.md", "# Hallo Welt", "<h1>Hallo Welt</h1>\n"],
        ["test", "article.md", "# Hallo Welt", "<h1>Hallo Welt</h1>\n"]
]


@pytest.mark.parametrize("dir, file, content_md, content_html", articles)
def test_readRaw(tempdir, dir, file, content_md, content_html):
    dest_path=os.path.join(tempdir, dir)
    os.makedirs(dest_path, exist_ok=True)

    with codecs.open(os.path.join(dest_path, file), 'w', 'utf-8') as fh:
        fh.write(content_md)

    assert file_io.readRaw(os.path.join(dest_path, file)) == content_md


@pytest.mark.parametrize("dir, file, content_md, content_html", articles)
def test_readRaw_no_permissions(tempdir, dir, file, content_md, content_html):
    dest_path=os.path.join(tempdir, dir)
    os.makedirs(dest_path, exist_ok=True)

    with codecs.open(os.path.join(dest_path, file), 'w', 'utf-8') as fh:
        fh.write(content_md)

    os.chmod(os.path.join(dest_path, file), 0o200)

    with pytest.raises(PermissionError, match="konnte nicht gelesen werden, bitte die Zugriffsrechte überprüfen"):
        file_io.readRaw(os.path.join(dest_path, file))


@pytest.mark.parametrize("dir, file, content_md, content_html", articles)
def test_readMarkDown(tempdir, dir, file, content_md, content_html):
    dest_path=os.path.join(tempdir, dir)
    os.makedirs(dest_path, exist_ok=True)

    with codecs.open(os.path.join(dest_path, file), 'w', 'utf-8') as fh:
        fh.write(content_md)

    assert file_io.readMarkDown(os.path.join(dest_path, file)) == content_html


@pytest.mark.parametrize("dir, file, content_md, content_html", articles)
def test_readMarkDown_no_permissions(tempdir, dir, file, content_md, content_html):
    dest_path=os.path.join(tempdir, dir)
    os.makedirs(dest_path, exist_ok=True)

    with codecs.open(os.path.join(dest_path, file), 'w', 'utf-8') as fh:
        fh.write(content_md)

    os.chmod(os.path.join(dest_path, file), 0o200)

    with pytest.raises(PermissionError, match="konnte nicht gelesen werden, bitte die Zugriffsrechte überprüfen"):
        file_io.readRaw(os.path.join(dest_path, file))


@pytest.mark.parametrize("dir, file, content_md, content_html", articles)
def test_updateArticle(tempdir, dir, file, content_md, content_html):
    dest_path=os.path.join(tempdir, dir)

    os.makedirs(dest_path, exist_ok=True)

    assert file_io.updateArticle(os.path.join(dest_path, file), content_md)
    assert os.path.exists(os.path.join(dest_path, file))


@pytest.mark.parametrize("dir, file, content_md, content_html", articles)
def test_updateArticle_no_permission(tempdir, dir, file, content_md, content_html):
    dest_path = os.path.join(tempdir, dir)

    os.makedirs(dest_path, exist_ok=True)
    os.chmod(dest_path, 0o400)

    with pytest.raises(PermissionError, match="konnte nicht geschrieben werden, bitte die Zugriffsrechte prüfen"):
        file_io.updateArticle(os.path.join(dest_path, file), content_md)

    assert not os.path.exists(os.path.join(dest_path, file))


@pytest.mark.parametrize("dir, file, content_md, content_html", articles)
def test_createArticle(tempdir, dir, file, content_md, content_html):
    dest_path = os.path.join(tempdir, dir)

    assert file_io.createArticle(os.path.join(dest_path, file), content_md)
    assert os.path.exists(os.path.join(dest_path, file))


@pytest.mark.parametrize("dir, file, content_md, content_html", articles)
def test_createArticle_no_permission(tempdir, dir, file, content_md, content_html):
    dest_path=os.path.join(tempdir, dir)
    os.makedirs(dest_path, exist_ok=True)

    os.chmod(tempdir, 0o400)

    if dir == "":
        with pytest.raises(PermissionError, match="konnte nicht geschrieben werden, bitte die Zugriffsrechte prüfen"):
            file_io.createArticle(os.path.join(dest_path, file), content_md)
    else:
        with pytest.raises(OSError, match="Die Verzeichnisse konnten nicht erstellt werden"):
            file_io.createArticle(os.path.join(dest_path, file), content_md)
    os.chmod(tempdir, 0o700)


@pytest.mark.parametrize("dir, file, content_md, content_html", articles)
def test_createArticle_file_exists(tempdir, dir, file, content_md, content_html):
    dest_path=os.path.join(tempdir, dir)
    os.makedirs(dest_path, exist_ok=True)

    with codecs.open(os.path.join(dest_path, file), 'w', 'utf-8') as fh:
        fh.write(content_md)

    with pytest.raises(FileExistsError, match="Es existiert bereits eine Datei mit dem gleichen Namen"):
        file_io.createArticle(os.path.join(dest_path, file), content_md)
