from app import app
from flask import render_template
from app.settings import Settings
import os, sys
import markdown2

rs = Settings()
data_dir = rs.get_data_dir()

@app.route('/')
def index():
    if os.path.exists(data_dir+"/README.md"):
        web_content = markdown2.markdown_path(data_dir+"/README.md")

    return render_template('index.html', content=web_content)