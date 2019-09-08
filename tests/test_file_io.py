import os
import sys
import shutil
from app.views import file_io
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


@pytest.mark.parametrize("dir, file, content_plain, content_md", articles)
def test_readRaw(tempdir, dir, file, content_plain, content_md):
    dest_path=os.path.join(tempdir, dir)
    os.makedirs(dest_path, exist_ok=True)

    with codecs.open(os.path.join(dest_path, file), 'w', 'utf-8') as fh:
        fh.write(content_plain)

    assert file_io.readRaw(os.path.join(dest_path, file)) == content_plain


@pytest.mark.parametrize("dir, file, content_plain, content_md", articles)
def test_readRaw_nopermissions(tempdir, dir, file, content_plain, content_md):
    dest_path=os.path.join(tempdir, dir)
    os.makedirs(dest_path, exist_ok=True)

    with codecs.open(os.path.join(dest_path, file), 'w', 'utf-8') as fh:
        fh.write(content_plain)

    os.chmod(os.path.join(dest_path, file), 0o200)

    with pytest.raises(PermissionError, match="konnte nicht gelesen werden, bitte die Zugriffsrechte überprüfen"):
        file_io.readRaw(os.path.join(dest_path, file))


@pytest.mark.parametrize("dir, file, content_plain, content_md", articles)
def test_readMarkDown(tempdir, dir, file, content_plain, content_md):
    dest_path=os.path.join(tempdir, dir)
    os.makedirs(dest_path, exist_ok=True)

    with codecs.open(os.path.join(dest_path, file), 'w', 'utf-8') as fh:
        fh.write(content_plain)

    assert file_io.readMarkDown(os.path.join(dest_path, file)) == content_md


@pytest.mark.parametrize("dir, file, content_plain, content_md", articles)
def test_readMarkDown_nopermission(tempdir, dir, file, content_plain, content_md):
    dest_path=os.path.join(tempdir, dir)
    os.makedirs(dest_path, exist_ok=True)

    with codecs.open(os.path.join(dest_path, file), 'w', 'utf-8') as fh:
        fh.write(content_plain)

    os.chmod(os.path.join(dest_path, file), 0o200)

    with pytest.raises(PermissionError, match="konnte nicht gelesen werden, bitte die Zugriffsrechte überprüfen"):
        file_io.readRaw(os.path.join(dest_path, file))


@pytest.mark.parametrize("dir, file, content_plain, content_md", articles)
def test_updateArticle(tempdir, dir, file, content_plain, content_md):
    dest_path=os.path.join(tempdir, dir)

    os.makedirs(dest_path, exist_ok=True)

    assert file_io.updateArticle(os.path.join(dest_path, file), content_plain)
    assert os.path.exists(os.path.join(dest_path, file))


@pytest.mark.parametrize("dir, file, content_plain, content_md", articles)
def test_updateArticle_nopermission(tempdir, dir, file, content_plain, content_md):
    dest_path = os.path.join(tempdir, dir)

    os.makedirs(dest_path, exist_ok=True)
    os.chmod(dest_path, 0o400)

    with pytest.raises(PermissionError, match="konnte nicht geschrieben werden, bitte die Zugriffsrechte prüfen"):
        file_io.updateArticle(os.path.join(dest_path, file), content_plain)

    assert not os.path.exists(os.path.join(dest_path, file))


