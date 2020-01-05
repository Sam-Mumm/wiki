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

csrf = CSRFProtect()

#wiki = Flask(__name__, instance_relative_config=True)
wiki = Flask(__name__, instance_path=os.path.join(user_home, '.wiki'), instance_relative_config=True)

babel = Babel(wiki)

csrf.init_app(wiki)

#wiki.config.from_pyfile('settings.py')
wiki.config.from_object('wiki.default_settings')


#wiki.config.from_pyfile('config.py')

wiki.secret_key = str(uuid4())

wiki.register_blueprint(pages_view)

wiki.register_blueprint(pages_index)

wiki.register_blueprint(pages_edit)

wiki.register_blueprint(pages_create)

wiki.register_blueprint(pages_search)

wiki.jinja_env.filters['fix_images'] = jinja_filters.fix_images