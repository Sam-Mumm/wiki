import os
import shutil
from wiki.views import file_io
import pytest
from tempfile import mkdtemp
import codecs
from .fixtures.conftest import tempdir

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


# Erfolgsfall: Zugriff auf die Rohdaten einer Datei, die lesbar ist
@pytest.mark.parametrize("article", articles)
def test_readRaw(tempdir, article):
    dest_path=os.path.join(tempdir, article['dir'])
    os.makedirs(dest_path, exist_ok=True)

    with codecs.open(os.path.join(dest_path, article['filename']), 'w', 'utf-8') as fh:
        fh.write(article['content_md'])

    assert file_io.readRaw(os.path.join(dest_path, article['filename'])) == article['content_md']


# Fehlerfall: Zugriff auf eine Datei die für den User nicht lesbar ist
@pytest.mark.parametrize("article", articles)
def test_readRaw_no_permissions(tempdir, article):
    dest_path=os.path.join(tempdir, article['dir'])
    os.makedirs(dest_path, exist_ok=True)

    os.mknod(os.path.join(dest_path, article['filename']), 0o200)

    with pytest.raises(PermissionError, match="konnte nicht gelesen werden, bitte die Zugriffsrechte überprüfen"):
        file_io.readRaw(os.path.join(dest_path, article['filename']))


# Fehlerfall: Zugriff auf eine Datei die nicht existiert
def test_readRaw_not_exists(tempdir):
    with pytest.raises(PermissionError, match="konnte nicht gelesen werden, bitte die Zugriffsrechte überprüfen"):
        file_io.readRaw(os.path.join(tempdir, "file_not_exists.md"))


# Erfolgsfall: Zugriff und parsen von einer Datei die lesbar ist
@pytest.mark.parametrize("article", articles)
def test_readMarkDown(tempdir, article):
    dest_path=os.path.join(tempdir, article['dir'])
    os.makedirs(dest_path, exist_ok=True)

    with codecs.open(os.path.join(dest_path, article['filename']), 'w', 'utf-8') as fh:
        fh.write(article['content_md'])

    assert file_io.readMarkDown(os.path.join(dest_path, article['filename'])) == article['content_html']


# Fehlerfall: Zugriff auf ein Datei die für den Benutzer nicht lesbar ist
@pytest.mark.parametrize("article", articles)
def test_readMarkDown_no_permissions(tempdir, article):
    dest_path=os.path.join(tempdir, article['dir'])
    os.makedirs(dest_path, exist_ok=True)

    with codecs.open(os.path.join(dest_path, article['filename']), 'w', 'utf-8') as fh:
        fh.write(article['content_md'])

    os.chmod(os.path.join(dest_path, article['filename']), 0o200)

    with pytest.raises(PermissionError, match="konnte nicht gelesen werden, bitte die Zugriffsrechte überprüfen"):
        assert file_io.readMarkDown(os.path.join(dest_path, article['filename']))


# Fehlerfall: Zugriff auf ein Datei die nicht existiert
def test_readMarkDown_not_exists(tempdir):
    with pytest.raises(PermissionError, match="konnte nicht gelesen werden, bitte die Zugriffsrechte überprüfen"):
        assert file_io.readMarkDown(os.path.join(tempdir, "file_not_exists.md"))


# Erfolgsfall: Erstellen von einer neuen Datei (=neuen Artikel)
@pytest.mark.parametrize("article", articles)
def test_createArticle(tempdir, article):
    dest_path = os.path.join(tempdir, article['dir'])

    assert file_io.createArticle(os.path.join(dest_path, article['filename']), article['content_md']) == True
    assert os.path.exists(os.path.join(dest_path, article['filename']))

    with codecs.open(os.path.join(dest_path, article['filename']), 'r', 'utf-8') as fh:
        assert fh.read() == article['content_md']

# Fehlerfall: Erstellen von einer neuen Datei ohne ausreichende Rechte für das Datenverzeichnis
@pytest.mark.parametrize("article", articles)
def test_createArticle_no_permissions(tempdir, article):
    dest_path = os.path.join(tempdir, article['dir'])

    os.chmod(tempdir, 0o400)

    # Soll die Datei im Root-Verzeichnis erstellt werden?
    if article['dir'] == "":
        with pytest.raises(PermissionError, match="konnte nicht geschrieben werden, bitte die Zugriffsrechte prüfen"):
            file_io.createArticle(os.path.join(dest_path, article['filename']), article['content_md'])
    else:
        with pytest.raises(OSError, match="Die Verzeichnisse konnten nicht erstellt werden"):
            file_io.createArticle(os.path.join(dest_path, article['filename']), article['content_md'])


# Fehlerfall: Erstellen einer Datei die bereits existiert
@pytest.mark.parametrize("article", articles)
def test_createArticle_file_exists(tempdir, article):
    dest_path = os.path.join(tempdir, article['dir'])
    os.makedirs(dest_path, exist_ok=True)

    os.mknod(os.path.join(dest_path, article['filename']))

    with pytest.raises(FileExistsError, match="Es existiert bereits eine Datei mit dem gleichen Namen"):
        file_io.createArticle(os.path.join(dest_path, article['filename']), article['content_md'])


# Erfolgsfall: Aktualisieren von einem vorhandenen Artikel
@pytest.mark.parametrize("article", articles)
def test_updateArticle(tempdir, article):
    dest_path = os.path.join(tempdir, article['dir'])
    os.makedirs(dest_path, exist_ok=True)

    os.mknod(os.path.join(dest_path, article['filename']))

    assert file_io.updateArticle(os.path.join(dest_path, article['filename']), article['content_md']) == True

    with codecs.open(os.path.join(dest_path, article['filename']), 'r', 'utf-8') as fh:
        assert fh.read() == article['content_md']


# Fehlerfall: Aktualisieren von einem vorhandenen Artikel auf den der User keine Schreibrechte hat
@pytest.mark.parametrize("article", articles)
def test_updateArticle_no_permissions(tempdir, article):
    dest_path = os.path.join(tempdir, article['dir'])
    os.makedirs(dest_path, exist_ok=True)

    os.mknod(os.path.join(dest_path, article['filename']), 0o400)

    with pytest.raises(PermissionError, match="konnte nicht geschrieben werden, bitte die Zugriffsrechte prüfen"):
        assert file_io.updateArticle(os.path.join(dest_path, article['filename']), article['content_md'])


# Erfolgsfall: Verschieben von einem Artikel
@pytest.mark.parametrize("article", articles)
def test_moveArticle(tempdir, article):
    # Verschieben der README.md wird durch die Oberfläche unterbunden
    if article['filename']=="README.md":
        pytest.skip()

    # Definition des Zielverzeichnisses
    dest_path=os.path.join(tempdir, "targetdir")

    # Anlegen der zu verschiebenden Datei
    src_path=os.path.join(tempdir, article['dir'])

    os.makedirs(src_path, exist_ok=True)

    with codecs.open(os.path.join(src_path, article['filename']), 'w', 'utf-8') as fh:
        fh.write(article['content_md'])

    # Verschieben und aktualisieren der Datei
    assert file_io.moveArticle(os.path.join(src_path, article['filename']),
                               os.path.join(dest_path, article['filename']),
                               article['content_md']) == True

    assert len(os.listdir(src_path)) == 0
    assert len(os.listdir(dest_path)) == 1

    with codecs.open(os.path.join(dest_path, article['filename']), 'r', 'utf-8') as fh:
        assert fh.read() == article['content_md']


# Fehlerfall: Verschieben einer Datei in ein Zielverzeichnis auf das der User keine Schreibrechte hat
@pytest.mark.parametrize("article", articles)
def test_moveArticle_no_dir_permissions(tempdir, article):
    # Verschieben der README.md wird durch die Oberfläche unterbunden
    if article['filename']=="README.md":
        pytest.skip()

    # Anlegen der zu verschiebenden Datei
    src_path=os.path.join(tempdir, article['dir'])
    os.makedirs(src_path, exist_ok=True)

    with codecs.open(os.path.join(src_path, article['filename']), 'w', 'utf-8') as fh:
        fh.write(article['content_md'])

    # Definition des Zielverzeichnisses
    dest_path=os.path.join(tempdir, "targetdir")
    os.makedirs(dest_path, exist_ok=True)
    os.chmod(dest_path, 0o400)

    with pytest.raises(PermissionError, match="Artikel konnte nicht verschoben werden, "
                                              "bitte die Zugriffsrechte prüfen"):
        assert file_io.moveArticle(os.path.join(src_path, article['filename']),
                                   os.path.join(dest_path, article['filename']),
                                   article['content_md']) == True


# Fehlerfall: Verschieben einer Datei in ein Zielverzeichnis wo bereits eine Datei mit dem gleichen Namen existiert
@pytest.mark.parametrize("article", articles)
def test_moveArticle_target_file_exist(tempdir, article):
    # Verschieben der README.md wird durch die Oberfläche unterbunden
    if article['filename']=="README.md":
        pytest.skip()

    # Anlegen der zu verschiebenden Datei
    src_path=os.path.join(tempdir, article['dir'])
    os.makedirs(src_path, exist_ok=True)

    with codecs.open(os.path.join(src_path, article['filename']), 'w', 'utf-8') as fh:
        fh.write(article['content_md'])

    # Definition des Zielverzeichnisses
    dest_path=os.path.join(tempdir, "targetdir")
    os.makedirs(dest_path, exist_ok=True)
    os.mknod(os.path.join(dest_path, article['filename']), 0o200)

    with pytest.raises(FileExistsError, match="Artikel konnte nicht verschoben werden, "
                                              "es existiert bereits eine Datei mit dem gleichen Namen"):
        assert file_io.moveArticle(os.path.join(src_path, article['filename']),
                                   os.path.join(dest_path, article['filename']),
                                   article['content_md']) == True