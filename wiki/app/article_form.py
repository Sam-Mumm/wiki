import os
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext
from wtforms import StringField, TextAreaField, SubmitField, ValidationError

class ArticleForm(FlaskForm):
    path = StringField(lazy_gettext("Pfad"), render_kw={"size": 45})
    comment = StringField(lazy_gettext("Kommentar"), render_kw={"size": 40})

    save = SubmitField(lazy_gettext("Speichern"))
    cancel = SubmitField(lazy_gettext("Abbrechen"))

    article_content = TextAreaField(lazy_gettext("Inhalt"), render_kw={"rows": 25, "cols": 100})

    def validate_path(self, data_dir, path_form):
        full_path_form=os.path.abspath(os.path.join(data_dir, path_form))

        if not full_path_form.startswith(data_dir):
            raise ValidationError(lazy_gettext("Der Pfad ist ungültig"))

        return True