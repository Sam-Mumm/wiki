from flask_wtf import FlaskForm
from flask_babel import lazy_gettext
from wtforms import StringField, TextAreaField, SubmitField, HiddenField

class ArticleForm(FlaskForm):
    path = StringField(lazy_gettext("Pfad"), render_kw={"size": 45})
    comment = StringField(lazy_gettext("Kommentar"), render_kw={"size": 40})

    save = SubmitField(lazy_gettext("Speichern"))
    cancel = SubmitField(lazy_gettext("Abbrechen"))

    article_content = TextAreaField(lazy_gettext("Inhalt"), render_kw={"rows": 25, "cols": 100})