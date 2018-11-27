from app import app
import re

## Dummy Methode - Zum Testen von custom filters in jinja
@app.template_filter()
def caps(text):
    # (\.\/|\.\.\/)?([a-z.-_A-Z1-9]\/*[a-z.-_A-Z1-9]+)
    text = re.sub(r'<img src="(\.\/|\.\.\/)?([a-z.-_A-Z1-9]\/*[a-z.-_A-Z1-9]+)" alt="([a-z.-_A-Z1-9]*)" />', '<img src="/static/data/\1" alt="\2" />', text)
    return text
#    return text.upper()
