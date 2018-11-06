from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False
app.static_folder = 'static'

from app import routes
from filters import caps