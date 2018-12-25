from app import app
from flask import render_template, redirect, url_for, request
import os, sys
import markdown2
from app.settings import Settings
from app.navigation import Navigation

# get the Settings from wiki_config.json
rs = Settings()
data_dir = rs.get_data_dir()
wiki_name = rs.get_wiki_name()

# Object/Class for the navigation through the wiki content
navi = Navigation(data_dir)


# route for the Navigation
@app.route('/index', defaults={'path': ''})
@app.route('/index/<path:path>')
def index(path):
    if path:
        full_path = os.path.join(data_dir,path)

        if os.path.isdir(full_path):
            content = navi.list_dir(path)
            return render_template('table_content.tmpl.html', wiki_name=wiki_name, content=content)
        elif os.path.isfile(full_path+".md"):
            return redirect(url_for('home')+path)
        else:
            return render_template('404.tmpl.html')

    else:
        content = navi.list_dir(path)
        return render_template('table_content.tmpl.html', wiki_name=wiki_name, content=content)

# Route for editing articles
@app.route('/edit', defaults={'path': 'home'}, methods=["GET","POST"])
@app.route('/edit/<path:path>', methods=["GET","POST"])
def edit(path):
    # Which Buttons should shown? (Index)
    navi = [
        {'endpoint': 'index', 'path': '', 'name': 'Index'},
    ]

    field_content={}

    article_file = os.path.join(data_dir, path+".md")

    if request.method == 'POST':
        content = request.form['article_content']

        if request.form['article_path'] == "home":
            article_file=data_dir + "/README.md"

        with open(article_file, 'w') as fh:
            fh.write(content)
            fh.closed

        return redirect(url_for(request.form['article_path']))

    if path != 'home':
        field_content['path']=path

        print article_file
        if not os.path.isfile(article_file):
            return render_template('404.tmpl.html')
    else:
        field_content['path']="home"
        if os.path.exists(data_dir + "/README.md"):
            article_file=data_dir + "/README.md"

    with open(article_file, 'r') as fh:
        content = fh.read().decode('utf8')
        field_content['content']=content
    fh.closed

    return render_template('edit.tmpl.html', wiki_name=wiki_name, navi=navi, field_content=field_content)


# Route for displaying of a single page
@app.route('/', defaults={'path': 'home'})
@app.route('/<path:path>')
def home(path):
    # Which Buttons should shown? (Edit, Index)
    navi = [
        {'endpoint': 'index', 'path': '', 'name': 'Index'},
        {'endpoint': 'edit', 'path': "/" + path, 'name': 'Bearbeiten'}
    ]
    if path != 'home':
        full_path = os.path.join(data_dir, path)

        if os.path.isfile(full_path+".md"):
            content = markdown2.markdown_path(full_path+".md", extras=["tables", "fenced-code-blocks"])

            return render_template('markdown_content.tmpl.html', content=content, navi=navi)
        elif os.path.isdir(full_path):
            return redirect(url_for('index'))
        else:
            return render_template('404.tmpl.html')
    else:
        if os.path.exists(data_dir+"/README.md"):
            content = markdown2.markdown_path(data_dir+"/README.md", extras=["tables", "fenced-code-blocks"])
        else:
            content=""
        return render_template('markdown_content.tmpl.html', content=content, navi=navi)