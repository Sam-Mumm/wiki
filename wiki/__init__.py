# noinspection PyInterpreter,PyInterpreter
from flask import Flask
from flask_babel import Babel
from uuid import uuid4
from flask_wtf.csrf import CSRFProtect
from wiki.views.view import pages_view
from wiki.views.index import pages_index
from wiki.views.edit import pages_edit
from wiki.views.create import pages_create
from wiki.views.search import pages_search
from wiki.jinja_filters import fix_images
from pathlib import Path
import os

user_home = str(Path.home())

def create_app(config_filename="default_settings"):
    csrf = CSRFProtect()

    wiki = Flask(__name__, instance_path = os.path.join(user_home, '.wiki'), instance_relative_config=True)

    wiki.config.from_object(config_filename)

    # Laden der benutzerdefinierten Einstellungen (falls vorhanden)
    if os.path.isfile(os.path.join(user_home, *['.wiki', 'settings.py'])):
        wiki.config.from_pyfile('settings.py')

    babel = Babel(wiki)

    csrf.init_app(wiki)
    register_blueprints(wiki)

    return wiki


def register_blueprints(wiki):
    wiki.secret_key = str(uuid4())

    wiki.register_blueprint(pages_view)

    wiki.register_blueprint(pages_index)

    wiki.register_blueprint(pages_edit)

    wiki.register_blueprint(pages_create)

    wiki.register_blueprint(pages_search)

    wiki.jinja_env.filters['fix_images'] = jinja_filters.fix_images