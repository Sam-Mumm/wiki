import os
from flask_babel import _
from wiki.constants import *

def validate_path(data_dir, path):
    full_path_form = os.path.abspath(os.path.join(data_dir, path))

    if not full_path_form.startswith(data_dir):
        raise ValueError(_(MSG_INVALID_PATH))

    return True
