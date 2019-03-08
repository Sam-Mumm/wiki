from app import app
from flask import render_template, redirect, url_for, request
import os, sys
import markdown2
from app.settings import Settings
from app.navigation import Navigation
import codecs
import hashlib

# get the Settings from wiki_config.json
rs = Settings()
data_dir = rs.get_data_dir()
wiki_name = rs.get_wiki_name()

# route for the Navigation

# Route for creating new articles
@app.route('/create', methods=["GET","POST"])
def create():
    navi_buttons = [
        {'endpoint': 'index', 'path': '', 'name': 'Index'},
    ]

    if request.method == 'POST':
        # Get the content of the form fields
        content_form = request.form['article_content']
        path_form=request.form['article_path'].strip("/")

        field_content = {}

        if path_form == "home":
            article_file=os.path.join(data_dir, "README.md")
        else:
            # Create the fullpath to the article file from the form field path
            article_file = os.path.join(data_dir, path_form + ".md")

        field_content['content'] = content_form;
        field_content['path'] = path_form

        # Did a target with the same name already exists?
        if os.path.isfile(article_file):
            error_msg = "Datei existiert im Zielverzeichnis, es wurden nur die Aenderungen an Ursprungsort gespeichert"
            return render_template('edit.tmpl.html', wiki_name=wiki_name, navi=navi_buttons, field_content=field_content)
        # Did the target directory NOT exists?
        elif not os.path.isdir(os.path.dirname(article_file)):
            # Try to create new target directory
            try:
                os.makedirs(os.path.dirname(article_file))
            except OSError as e:
                error_msg = "Das Verzeichnis konnte nicht erstellt werden"
                return render_template('edit.tmpl.html', wiki_name=wiki_name, navi=navi_buttons, field_content=field_content)

        with codecs.open(article_file, 'w', 'utf-8') as fh:
            fh.write(content_form)
            fh.closed
        return redirect(url_for("home", path=path_form))

    return render_template('create.tmpl.html', wiki_name=wiki_name, navi=navi_buttons)
