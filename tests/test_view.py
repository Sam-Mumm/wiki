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
                  "content_md": "# Hello World",
                  "content_html": "<h1>Hello World</h1>\n"
                }
    ]


# Erfolgsfall: Test auf einem Wiki mit einem leeren Datenverzeichnis
@pytest.mark.parametrize("article", articles)
def test_wiki_empty(test_client, captured_templates, article):
    response = test_client[0].get(article['url'])

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


    assert content['wiki_name'] == "My Testwiki"


# Erfolgsfall: Test von dem anzeigen von Artikeln
@pytest.mark.parametrize("article", articles)
def test_view_article(test_client, captured_templates, article):
    # Anlegen der zu verschiebenden Datei
    src_path=os.path.join(test_client[1], article['dir'])
    os.makedirs(src_path, exist_ok=True)

    with codecs.open(os.path.join(src_path, article['filename']), 'w', 'utf-8') as fh:
        fh.write(article['content_md'])

    response = test_client[0].get(article['url'])

    response.status_code == 200

    template, content = captured_templates[0]

    assert content['wiki_name'] == "My Testwiki"
    assert template.name == "markdown_content.tmpl.html"
    assert content['content'] == article['content_html']
    assert len(content['navi']) == 2


@pytest.mark.parametrize("article", articles)
def test_wiki_root_no_permissions(test_client, captured_templates, article):
    # Anlegen der zu verschiebenden Datei
    src_path=os.path.join(test_client[1], article['dir'])
    os.makedirs(src_path, exist_ok=True)

    with codecs.open(os.path.join(src_path, article['filename']), 'w', 'utf-8') as fh:
        fh.write(article['content_md'])

    os.chmod(test_client[1], 0o000)

    response = test_client[0].get(article['url'])

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

    assert content['wiki_name'] == "My Testwiki"

    os.chmod(test_client[1], 0o700)


@pytest.mark.parametrize("article", articles[1:])
def test_wiki_subdir_no_permissions(test_client, captured_templates, article):
    src_path=os.path.join(test_client[1], article['dir'])
    os.makedirs(src_path, exist_ok=True)

    with codecs.open(os.path.join(src_path, article['filename']), 'w', 'utf-8') as fh:
        fh.write(article['content_md'])

    os.chmod(src_path, 0o200)

    response = test_client[0].get(article['url'])

    response.status_code == 200

    template, content = captured_templates[0]

    assert template.name == "404.tmpl.html"

    # Anzahl der Buttons
    assert len(content['navi']) == 0

    assert content['wiki_name'] == "My Testwiki"

    os.chmod(src_path, 0o700)


@pytest.mark.parametrize("article", articles)
def test_wiki_article_no_permissions(test_client, captured_templates, article):
    src_path=os.path.join(test_client[1], article['dir'])
    os.makedirs(src_path, exist_ok=True)

    with codecs.open(os.path.join(src_path, article['filename']), 'w', 'utf-8') as fh:
        fh.write(article['content_md'])

    os.chmod(os.path.join(src_path, article['filename']), 0o200)

    response = test_client[0].get(article['url'])

    response.status_code == 200

    template, content = captured_templates[0]

    if article['url'] == "/":
        assert template.name == "markdown_content.tmpl.html"
        assert len(content['navi']) == 2
    else:
        assert template.name == "404.tmpl.html"
        assert len(content['navi']) == 0

    assert content['wiki_name'] == "My Testwiki"

    os.chmod(os.path.join(src_path, article['filename']), 0o700)