from app import app
from flask import render_template
from settings import Settings

rs = Settings()
bla = rs.readConfig();

@app.route('/')
def index():
    user="Dan"
    return render_template('index.html', username=bla)