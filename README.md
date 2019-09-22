# Wiki

## Feature


## Screenshots

## Installation
For the Installation via pypi or git I recommand to install the wiki i a virtual environment.
```commandline
# python3 -m venv /opt/wiki
# source /opt/wiki/bin/activate
```


### ... via PyPi


### ... via git
```commandline
$ git clone https://github.com/Sam-Mumm/wiki.git /opt/wiki
$ cd /opt/wiki
```

### ... via Docker


## Configuration
### Reverse Proxy
#### nginx
```commandline
# apt install -y nginx
```

### systemd
```buildoutcfg
[Unit]
Description=uWSGI instance to serve project
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/opt/wiki
Environment="PATH=/opt/wiki/bin"
ExecStart=/opt/wiki/bin/uwsgi --ini uwsgi.ini

[Install]
WantedBy=multi-user.target
```


## Running
### docker-compose
