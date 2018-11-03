import os
from datetime import datetime

class Navigation:
    data_dir = None

    def __init__(self, data_dir):
        self.data_dir=data_dir

    # List entries of the given directory
    def list_dir(self, dir):
        dir_content = []

        full_path = self.data_dir+"/"+dir

        for e in os.listdir(full_path):
            full_entry=os.path.join(full_path,e)

            entry = {'name': None, 'isdir': None, 'path': None, 'size': None, 'mtime': None, 'ctime': None}

            # List only directories and files with *.md-ending
            if os.path.isdir(full_entry) and not e==".git":
                entry['is_dir'] = True
                entry['name'] = e
            elif e.endswith('.md'):
                entry['size'] = os.path.getsize(full_entry)
                entry['name'] = e[:-3]
            else:
                continue

            print dir
            if dir:
                entry['path'] = dir+"/"+entry['name']
            else:
                entry['path'] = entry['name']

            entry['mtime'] = datetime.fromtimestamp(os.path.getmtime(full_entry)).strftime('%Y-%m-%d %H:%M')
            entry['ctime'] = datetime.fromtimestamp(os.path.getctime(full_entry)).strftime('%Y-%m-%d %H:%M')

            dir_content.append(entry)
#        print dir_content
        return dir_content