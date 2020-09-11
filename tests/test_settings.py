import os

BASE_DIR = os.path.dirname(__file__)

WIKI_NAME = "My Wiki"

DATA_DIR = os.path.join(BASE_DIR, "static/data")

INDEX_DIR = os.path.join(BASE_DIR, "static/index")

START_SITE = "README.md"

GIT_SUPPORT=False

DEBUG = True

print(BASE_DIR)
