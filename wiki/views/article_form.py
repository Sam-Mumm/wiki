from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SubmitField, HiddenField

class ArticleForm(FlaskForm):
    path = TextField("Pfad", render_kw={"size": 45})
    comment = TextField("Kommentar", render_kw={"size": 40})

    save = SubmitField("Speichern")
    cancel = SubmitField("Abbrechen")

    article_content = TextAreaField("content", render_kw={"rows": 25, "cols": 100})