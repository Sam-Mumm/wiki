import json

class Settings:
    config_file="./wiki_config.json"
    configs = None

    def __init__(self):
        with open(self.config_file) as f:
            self.configs = json.load(f)

    def get_data_dir(self):
        return self.configs['data_dir']

    def get_index_dir(self):
        return self.configs['index_dir']

    def get_wiki_name(self):
        return self.configs['wiki_name']
