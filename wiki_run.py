#!/usr/bin/env python
from wiki import wiki
from pathlib import Path
import argparse
import os

def start_app():
    wiki.run(host='0.0.0.0',
             port=5000)


def setup_dialog():
    user_home = str(Path.home())
    rel_config_path = ['.wiki', 'settings.py']
    abs_config_path = os.path.join(user_home, *rel_config_path)
    config_entries = {}

    if os.path.isfile(abs_config_path):
        override_configfile = None
        while override_configfile!="" and not override_configfile=="N" and not override_configfile=="y":
            override_configfile = input("configuration file already exists. Override (N/y)? ")

        if override_configfile=="N" or override_configfile=="":
            return

    name = input("What should be the Name of the wiki? [My Wiki]")
    if name != "":
        config_entries['WIKI_NAME'] = '"'+name+'"'

    # git Unterstützung
    git_support = input("Do you want git-support? (N/y)")
    if git_support == "" or git_support == "N":
        config_entries['GIT_SUPPORT'] = False
    else:
        config_entries['GIT_SUPPORT'] = True

        git_url=""
        while not git_url.startswith("https://github.com"):
            git_url = input("What is the URL to the github-Repository?")
        config_entries['GIT_URL'] = '"'+git_url+'"'

    # Schreiben der Konfiguration in die Datei
    with open(abs_config_path, 'w') as fh:
        for k in config_entries.keys():
            fh.write(k+"="+str(config_entries[k])+"\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--setup", help="increase output verbosity", action="store_true")
    args = parser.parse_args()

    if args.setup:
        setup_dialog()

    start_app()
