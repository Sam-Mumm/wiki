from setuptools import setup, find_packages

setup(
    name = 'wiki',
    version = '1.0.1',
    url = 'https://github.com/Sam-Mumm/wiki.git',
    author = 'Dan',
    author_email = 'dan.steffen.de@gmail.com',
    description = 'Small Wiki with git support',
    packages = find_packages(),
    install_requires = ['flask == 1.1.2', 'Whoosh == 2.7.4', 'markdown2 == 2.3.9', 'Flask-WTF==0.14.3', 'Flask-Babel==1.0.0'],
    include_package_data = True,
    extras_require={ 'testing': ["pytest"] },
    scripts=["wiki_run.py"]
)
