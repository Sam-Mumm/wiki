from flask_babel import _
from wiki.constants import *

all_endpoints= {
    "index": {'endpoint': 'pages_index.index', 'name': LBL_INDEX, 'parameter': {}},
    "edit": {'endpoint': 'pages_edit.edit', 'name': _(LBL_EDIT), 'parameter': {}},
    "create": {'endpoint': 'pages_create.create', 'name': _(LBL_CREATE), 'parameter': {}}
}