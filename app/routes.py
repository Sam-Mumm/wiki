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
@app.route('/index', defaults={'path': ''})
@app.route('/index/<path:path>')
def index(path):
    # Which Buttons should shown? (here: Create)
    navi_buttons = [
        {'endpoint': 'create', 'path': '', 'name': 'Erstellen'},
    ]

    # Object/Class for the navigation through the wiki content
    navi = Navigation(data_dir)

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
        return render_template('table_content.tmpl.html', wiki_name=wiki_name, content=content, navi=navi_buttons)


# Route for editing articles
@app.route('/edit', defaults={'path': 'home'}, methods=["GET","POST"])
@app.route('/edit/<path:path>', methods=["GET","POST"])
def edit(path):
    # Which Buttons should shown? (here: Index)
    navi_buttons = [
        {'endpoint': 'index', 'path': '', 'name': 'Index'},
    ]

    field_content={}

    article_file = os.path.join(data_dir, path+".md")

    # Processing after submit
    if request.method == 'POST':
        # Get the content of the form fields
        content_form = request.form['article_content']
        path_form=request.form['article_path']
        checksum_form=request.form['checksum']

        # if there is no modification return to view of article
        if checksum_form == hashlib.md5(content_form.encode('utf-8')).hexdigest():
            return redirect(url_for("home", path=request.form['article_path']))

        # Create the fullpath to the article file from the form field path
        target_file_fullpath = os.path.join(data_dir, path_form + ".md")

        if path_form == "home":
            article_file=data_dir + "/README.md"
        else:
            # Was the article-file moved?
            if path != path_form:

                # Did a target with the same name already exists?
                if os.path.isfile(target_file_fullpath):
                    error_msg="Datei existiert im Zielverzeichnis, es wurden nur die Aenderungen an Ursprungsort gespeichert"
                # Did the target directory NOT exists?
                elif not os.path.isdir(os.path.dirname(target_file_fullpath)):
                    # Try to create new target directory
                    try:
                        os.makedirs(os.path.dirname(target_file_fullpath))
                        article_file = target_file_fullpath
                    except OSError as e:
                        error_msg="Das Verzeichnis konnte nicht erstellt werden, speichere Datei am urspruenglichen Ort"
                # Did the target-directory exists and did not exists a file with the same name?
                elif not os.path.isfile(target_file_fullpath) and os.path.isdir(os.path.dirname(target_file_fullpath)):
                    article_file = target_file_fullpath

        # Write to file
        with codecs.open(article_file, 'w', 'utf-8') as fh:
            fh.write(content_form)
            fh.closed

        # Redirect to the new updated article
        return redirect(url_for("home", path=request.form['article_path']))

    if path != 'home' and path != 'README':
        field_content['path']=path

        # Error-Handling for not existing file
        if not os.path.isfile(article_file):
            return render_template('404.tmpl.html')
    else:
        field_content['path']="home"
        if os.path.exists(data_dir + "/README.md"):
            article_file=data_dir + "/README.md"

    # Read from article file
    with codecs.open(article_file, 'r', 'utf-8') as fh:
        content = fh.read()
        field_content['content']=content

        # Generate checksum of article content
        field_content['checksum']=hashlib.md5(content.encode('utf-8')).hexdigest()

        fh.closed

    return render_template('edit.tmpl.html', wiki_name=wiki_name, navi=navi_buttons, field_content=field_content)


# Route for displaying of a single page
@app.route('/', defaults={'path': 'home'})
@app.route('/<path:path>')
def home(path):
    # Which Buttons should shown? (Edit, Index)
    navi_buttons = [
        {'endpoint': 'index', 'path': '', 'name': 'Index'},
        {'endpoint': 'edit', 'path': "/" + path, 'name': 'Bearbeiten'}
    ]

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

# Route for editing articles
@app.route('/create', defaults={'path': ''}, methods=["GET","POST"])
@app.route('/create/<path:path>', methods=["GET","POST"])
def create(path):
    return render_template('404.tmpl.html')