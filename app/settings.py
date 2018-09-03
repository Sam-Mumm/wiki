import configparser
import os, sys

class Settings:
    # Auslesen der Einstellungen aus der settings.ini
    def readConfig(self):
        try:
            config = configparser.ConfigParser()
            config.read('/home/dsteffen/python/wiki/app/settings.ini')
        except Exception as e:
            print(str(e))

        # Auslesen der Liste der zu ignorierenden Dateien
        try:
            ignoring_dirs=config.get('Default', 'ignoring_dir').split(',')
        except Exception as e:
            print(str(e))

        try:
            self.createPageTree(config.get('Default', 'data_dir'), ignoring_dirs)
        except Exception as e:
            print(str(e))
        return "kekse"

    # Erstellen der Datenstruktur fuer den Seitenbaum
    def createPageTree(self, data_dir, ignoring_dirs):
        pagetree={}

        # TODO: Aufnahme der Ignore-Funktion fuer Verzeichnisse
        for (path, dirs, files) in os.walk(data_dir):
            # Ermitteln von dem relativen Pfad wenn man sich nicht im Root-Element befindet
            # Bsp.: /path/to/data/dir/site/subsite2 -> site/subsite

            print "PATH: "+path
            rel_path = path[len(data_dir) + 1:]

            rel_path_dirs = rel_path.split('/')

            # Iteriere ueber die Dateien im Verzeichnis
            for file in files:
                tmp={}

                # Betrachte nur Markdown-Files
                if file.endswith('.md'):
                    # Hole den Titel aus der Ueberschrift der Datei
                    with open(path + "/" + file) as f:
                        title = f.readline().strip('\n')
                        if not title.startswith('# '):
                            title = '<kein Titel>'
                        else:
                            title = title.replace('# ','')

                    # Abschneiden von der Dateiendung .md
                    name = os.path.splitext(file)[0]

                    # befinden wir uns im Root-Element? Falls nicht hole den Namen von dem aktuellen Verzeichnis
                    if not rel_path:
                        tmp['title']=title
                        tmp['subpages']={}
                        pagetree[name]=tmp
                    else:
                        tmp2={}
                        subtree=pagetree

                        for d in rel_path_dirs:
                            subtree=subtree[d]['subpages']

                        tmp2['title']=title
                        tmp2['subpages']={}
                        tmp[name]=tmp2

                        subtree['subpages'].append(tmp)
                print pagetree
