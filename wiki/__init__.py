from flask import Flask
from uuid import uuid4
from wiki.views.view import pages_view
from wiki.views.index import pages_index
from wiki.views.edit import pages_edit
from wiki.views.create import pages_create
from wiki.views.search import pages_search
from wiki.jinja_filters import fix_images

wiki = Flask(__name__)

wiki.config.from_pyfile('settings.py', silent=True)

wiki.secret_key = str(uuid4())

wiki.register_blueprint(pages_view)

wiki.register_blueprint(pages_index)

wiki.register_blueprint(pages_edit)

wiki.register_blueprint(pages_create)

wiki.register_blueprint(pages_search)

wiki.jinja_env.filters['fix_images'] = jinja_filters.fix_images