from flask import Blueprint, current_app, request, url_for
import re
from os import path

fix_images = Blueprint("fix_images", __name__, template_folder='templates')

@fix_images.app_template_filter()
def fix_images(text):
    path_parts=[]

    # Get the Path to the data-dir
    path_parts.append(url_for('static',filename='data'))

    # Get the current context
    path_parts.append(path.dirname(request.path))

    path_parts.append("/")

    static_path=''.join(path_parts)

    # Replace all img-src-Attribut with the path to the data-dir
    text = re.sub(r'<img src="([\.\/|\.\.\/]?[a-z.-_A-Z1-9]\/*[a-z.-_A-Z1-9]+)" alt="([a-z.-_A-Z1-9]*)" />', '<img src="'+static_path+r'\1" alt="\2" />', text)

    return text
