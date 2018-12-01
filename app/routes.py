from app import app
from flask import render_template, redirect, url_for
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

@app.route('/edit', defaults={'path': ''})
@app.route('/edit/<path:path>')
def edit(path):
    navi = [
        {'endpoint': 'index', 'path': '', 'name': 'Index'},
    ]

    return render_template('edit.tmpl.html', wiki_name=wiki_name, navi=navi)


# Route for the displaying of a single page
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    navi = [
        {'endpoint': 'index', 'path': '', 'name': 'Index'},
    ]

    if path:
        navi.append({'endpoint': 'edit', 'path': "/"+path, 'name': 'Bearbeiten'})
        full_path = os.path.join(data_dir, path)

        if os.path.isfile(full_path+".md"):
            content = markdown2.markdown_path(full_path+".md", extras=["tables", "fenced-code-blocks"])

            return render_template('markdown_content.tmpl.html', content=content, navi=navi)
        elif os.path.isdir(full_path):
            return redirect(url_for('index'))
        else:
            return render_template('404.tmpl.html')

    else:
        navi.append({'endpoint': 'edit', 'path': '', 'name': 'Bearbeiten'})

        if os.path.exists(data_dir+"/README.md"):
            content = markdown2.markdown_path(data_dir+"/README.md", extras=["tables", "fenced-code-blocks"])
        else:
            content=""
        return render_template('markdown_content.tmpl.html', content=content, navi=navi)