from app import app
import json

def init_wiki():
    config_file="./app/wiki_config.json"
    configs=None

    with open(config_file) as f:
        configs = json.load(f)

    print configs['data_dir']

if __name__ == '__main__':
    init_wiki()
    app.run(host='0.0.0.0',
            port=5002)
