from flask import Flask
from uuid import uuid4
from app.views.view import pages_view
from app.views.index import pages_index
from app.views.edit import pages_edit

app = Flask(__name__)
app.config.from_pyfile('settings.py', silent=True)

app.secret_key = str(uuid4())

app.register_blueprint(pages_view)

app.register_blueprint(pages_index)

app.register_blueprint(pages_edit)