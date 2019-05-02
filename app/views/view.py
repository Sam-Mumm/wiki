from flask import Blueprint, render_template, current_app
import os, sys
import markdown2

pages_view = Blueprint("pages_view", __name__)

# Route zum anzeigen eines Artikels
@pages_view.route('/', defaults={'path': 'home'})
@pages_view.route('/<path:path>')
def home(path):
    # Which Buttons should shown? (Edit, Index)
    navi_buttons = [
        {'endpoint': 'pages_index.index', 'path': '', 'name': 'Index'},
        {'endpoint': 'pages_edit.edit', 'path': "/" + path, 'name': 'Bearbeiten'}
    ]

    data_dir=current_app.config['DATA_DIR']

    if path != 'home':
        full_path = os.path.join(data_dir, path)

        if os.path.isfile(full_path+".md"):
            content = markdown2.markdown_path(full_path+".md", extras=["tables", "fenced-code-blocks"])

            return render_template('markdown_content.tmpl.html', content=content, navi=navi_buttons)
        elif os.path.isdir(full_path):
            return redirect(url_for('index'))
        else:
            return render_template('404.tmpl.html')
    else:
        if os.path.exists(data_dir+"/README.md"):
            content = markdown2.markdown_path(data_dir+"/README.md", extras=["tables", "fenced-code-blocks"])
        else:
            content=""
        return render_template('markdown_content.tmpl.html', content=content, navi=navi_buttons)