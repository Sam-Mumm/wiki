import pytest
from wiki import create_app
from tempfile import mkdtemp
import shutil
from wiki.constants import *
import json

@pytest.fixture(scope="session")
def temp_datadir():
    tempdir = mkdtemp()

    yield tempdir
    shutil.rmtree(tempdir)

@pytest.fixture(scope="session")
def app(request, temp_datadir):
    app = create_app()

    create_testdata(app, temp_datadir, data_structure)

    app.config['DATA_DIR']=temp_datadir

    with app.app_context():
        yield app


@pytest.fixture(scope="session")
def client(request, app):
    client = app.test_client()
    return client


@pytest.fixture(scope="session")
def data_structure():
    return read_file()


def read_file():
    with open("./data.json", "r") as f:
        return json.load(f)


# Generieren von Testdaten basierend auf data.json
def create_testdata(app, temp_datadir, data_structure):

    print(data_structure)
    # Anlegen der Startseite
    start_site="{}/{}{}".format(temp_datadir, app.config['START_SITE'], MARKDOWN_FILE_EXTENSION)
    with open(start_site, "w") as f:
        f.write("# Startseite fuer Testdaten\n")
