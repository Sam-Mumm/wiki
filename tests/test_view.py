from .fixtures.conftest import test_client, app, captured_templates, tempdir
import os
import codecs
import pytest

articles = [
                { "dir": "",
                  "filename": "README.md",
                  "url": "/",
                  "content_md": "# Hallo Welt",
                  "content_html": "<h1>Hallo Welt</h1>\n"
                },
                { "dir": "test",
                  "filename": "article.md",
                  "url": "/test/article",
                  "content_md": "# Hallo Welt",
                  "content_html": "<h1>Hallo Welt</h1>\n"
                }
    ]


# Test auf einem Wiki mit einem leeren Datenverzeichnis
@pytest.mark.parametrize("article", articles)
def test_wiki_empty(test_client, captured_templates, article):
    response = test_client.get(article['url'])

    response.status_code == 200

    template, content = captured_templates[0]

    if article['url'] == "/":
        assert template.name == "markdown_content.tmpl.html"
        assert content['content'] == "<h1>Willkommen</h1>"

        # Anzahl der Buttons
        assert len(content['navi']) == 2
    else:
        assert template.name == "404.tmpl.html"

        # Anzahl der Buttons
        assert len(content['navi']) == 0


    assert content['wiki_name'] == "My Wiki"


# Test auf einem Wiki mit einem leeren Datenverzeichnis
@pytest.mark.parametrize("article", articles)
def test_wiki_empty(test_client, captured_templates, tempdir, article):
    # Anlegen der zu verschiebenden Datei
    src_path=os.path.join(tempdir, article['dir'])

    os.makedirs(src_path, exist_ok=True)

    with codecs.open(os.path.join(src_path, article['filename']), 'w', 'utf-8') as fh:
        fh.write(article['content_md'])

    response = test_client.get(article['url'])

    response.status_code == 200

    template, content = captured_templates[0]

    assert template.name == "markdown_content.tmpl.html"
