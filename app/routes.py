from app import app
from flask import render_template
import os, sys
import markdown2
from app.settings import Settings
from app.navigation import Navigation
from flaskext.markdown import Markdown
Markdown(app)

# get the Settings from wiki_config.json
rs = Settings()
data_dir = rs.get_data_dir()
wiki_name = rs.get_wiki_name()

# Object/Class for the navigation through the wiki content
navi = Navigation(data_dir)

@app.route('/')
def home():
    if os.path.exists(data_dir+"/README.md"):
        content = markdown2.markdown_path(data_dir+"/README.md")
    return render_template('markdown_content.tmpl.html', content=content)

@app.route('/index', defaults={'path': ''})
@app.route('/index/<path:path>')
def index(path):
    
    content=navi.list_dir(path)

    return render_template('table_content.tmpl.html', wiki_name=wiki_name, content=content)
