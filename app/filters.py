from app import app

## Dummy Methode - Zum Testen von custom filters in jinja
@app.template_filter()
def caps(text):
    return text.upper()