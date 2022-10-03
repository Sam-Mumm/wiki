from flask_babel import _
from wiki.constants import *

all_endpoints= {
    "index": {'endpoint': 'pages_index.index', 'name': LBL_INDEX, 'parameter': {}},
    "edit": {'endpoint': 'pages_edit.edit', 'name': _(LBL_EDIT), 'parameter': {}},
    "create": {'endpoint': 'pages_create.create', 'name': _(LBL_CREATE), 'parameter': {}}
}

def get_config_settings(ca):
    config = {
        CONFIGFILE_KEY_DATA_DIR: ca.config[CONFIGFILE_KEY_DATA_DIR],
        CONFIGFILE_KEY_WIKI_NAME: ca.config[CONFIGFILE_KEY_WIKI_NAME],
        CONFIGFILE_KEY_START_SITE: ca.config[CONFIGFILE_KEY_START_SITE],
        CONFIGFILE_KEY_INDEX_DIR: ca.config[CONFIGFILE_KEY_INDEX_DIR]
    }

    return config

