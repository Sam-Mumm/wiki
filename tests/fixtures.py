import pytest
from wiki import create_app
from tempfile import mkdtemp
import shutil
from flask import template_rendered

@pytest.fixture()
def tempdir():
    tempdir = mkdtemp()
    yield tempdir
    shutil.rmtree(tempdir)


@pytest.fixture()
def app(tempdir):
    wiki = create_app()

    wiki.config['DATA_DIR']=tempdir

    context = wiki.test_request_context()

    context.push()

    yield wiki, tempdir

    context.pop()


@pytest.yield_fixture()
def test_client(app):
    client = app[0].test_client()
    return client, app[1]


@pytest.fixture()
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app[0])
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app[0])