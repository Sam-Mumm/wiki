from .. import app

@app.template_filter()
def caps(text):
    return text.uppercase()