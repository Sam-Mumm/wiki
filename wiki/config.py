from flask_babel import _
from .utils import magic

all_endpoints= {
    "index": {'endpoint': 'pages_index.index', 'name': magic.LBL_INDEX, 'parameter': {}},
    "edit": {'endpoint': 'pages_edit.edit', 'name': _(magic.LBL_EDIT), 'parameter': {}},
    "create": {'endpoint': 'pages_create.create', 'name': _(magic.LBL_CREATE), 'parameter': {}}
}