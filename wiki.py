#!/usr/bin/env python
from wiki import wiki

def start_app():
    wiki.run(host='0.0.0.0',
             port=5000)


if __name__ == '__main__':
    start_app()