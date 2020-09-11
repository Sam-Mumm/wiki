from .fixtures.conftest import test_client, app, captured_templates
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