import sys

# Some debug to uwsgi.log so we can troubleshoot situations
print("Starting WSGI, Python is {}, sys.path is {}".format(sys.version, sys.path))

# TODO: We need to have this dummy entry point load call, otherwise namespaced websauna packages do not seem to import and I was not unable to resolve why
# I suspect some of the packages (websauna.viewconfig) clashes with the Python installation and Python doesn't figure out it's actually a properly namespaced packages. Alternative explanation is that I run websauna in development mode pip -e websauna
from pkg_resources import load_entry_point
load_entry_point("websauna", "paste.app_factory", "main")

from pyramid.paster import get_app
from websauna.system.devop.cmdline import setup_logging

ini_path = '{{ websauna_config_file }}'
setup_logging(ini_path)
application = get_app(ini_path, 'main')
