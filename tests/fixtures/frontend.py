import pytest
from wiki import create_app
from tempfile import mkdtemp
import shutil
from flask import template_rendered

@pytest.fixture
def app():
    wiki = create_app()
    context = wiki.test_request_context()
    context.push()

    tempdir = mkdtemp()

    yield wiki

    shutil.rmtree(tempdir)

    context.pop()


@pytest.yield_fixture()
def test_client(app):
    client = app.test_client()
    return client


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)