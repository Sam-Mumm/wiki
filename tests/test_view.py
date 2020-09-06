import pytest
from tempfile import mkdtemp
import shutil
from wiki import create_app

@pytest.yield_fixture()
def test_client():
    app = create_app()
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    tempdir = mkdtemp()
    yield testing_client
    ctx.pop()
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


# Erfolgsfall: Zugriff auf die Rohdaten einer Datei, die lesbar ist
@pytest.mark.parametrize("article", articles)
def test_view(test_client, article):
    assert True