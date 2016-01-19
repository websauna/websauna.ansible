from websauna.utils.configincluder import monkey_patch_paster_config_parser
monkey_patch_paster_config_parser()

from pyramid.paster import get_app
from websauna.system.devop.cmdline import setup_logging
ini_path = '{{ websauna_config_file }}'
setup_logging(ini_path)
application = get_app(ini_path, 'main')
