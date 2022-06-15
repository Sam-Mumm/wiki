import os
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext
from wtforms import StringField, TextAreaField, SubmitField, ValidationError
from wiki.constants import *

class ArticleForm(FlaskForm):
    path = StringField(lazy_gettext(LBL_PATH), render_kw={"size": 45})
    comment = StringField(lazy_gettext(LBL_COMMENT), render_kw={"size": 45})

    save = SubmitField(lazy_gettext(LBL_SAVE))
    cancel = SubmitField(lazy_gettext(LBL_CANCEL))

    article_content = TextAreaField(lazy_gettext(LBL_CONTENT), render_kw={"rows": 25, "cols": 100})

    def validate_path(self, data_dir, path_form):
        full_path_form=os.path.abspath(os.path.join(data_dir, path_form))

        if not full_path_form.startswith(data_dir):
            raise ValidationError(lazy_gettext(MSG_INVALID_PATH))

        return True