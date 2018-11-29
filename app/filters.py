from app import app
import flask
import re

@app.template_filter()
def caps(text):

    # Get the Path to the data-dir
    content_folder_path=flask.url_for('static',filename='data/')

    # Replace all img-src-Attribut with the path to the data-dir
    text = re.sub(r'<img src="(\.\/|\.\.\/)?([a-z.-_A-Z1-9]\/*[a-z.-_A-Z1-9]+)" alt="([a-z.-_A-Z1-9]*)" />', '<img src="'+content_folder_path+r'\2" alt="\3" />', text)

    return text
