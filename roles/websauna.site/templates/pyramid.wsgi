from pyramid.paster import get_app
from websauna.system.devop.cmdline import setup_logging
ini_path = '{{ websauna_config_file }}'
setup_logging(ini_path)
application = get_app(ini_path, 'main')
