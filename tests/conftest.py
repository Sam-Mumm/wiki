import pytest
from wiki import create_app
from tempfile import mkdtemp
import shutil
from wiki.constants import *
import json
import os

@pytest.fixture(scope="session")
def temp_datadir():
    tempdir = mkdtemp()

    yield tempdir
    shutil.rmtree(tempdir)

@pytest.fixture(scope="session", name="app")
def app(request, temp_datadir, data_structure):
    app = create_app()

    create_testdata(app, temp_datadir, data_structure)

    app.config['DATA_DIR']=temp_datadir

    with app.app_context():
        yield app


@pytest.fixture(scope="session")
def client(request, app):
    client = app.test_client()
    return client


@pytest.fixture(scope="session", name="data_structure")
def data_structure():
    with open("data.json", "r") as f:
        return json.load(f)


# Generieren von Testdaten basierend auf data.json
def create_testdata(app, temp_datadir, data_structure):
    # Anlegen der Startseite abhängig von der Konfigurationsdatei
    start_site="{}/{}{}".format(temp_datadir, app.config['START_SITE'], MARKDOWN_FILE_EXTENSION)
    with open(start_site, "w") as f:
        f.write("# Startseite fuer Testdaten\n")

    for e in data_structure:
        dir_path="{}/{}".format(temp_datadir, e['path'])
        os.makedirs(dir_path, exist_ok=True)

        with open("{}/{}".format(dir_path, e['filename']), 'w') as f:
            f.write(e['content'])

