import os
import logging
import yaml

cfg = {
  'global': {
    'join': {
      'apikey': 'abcdef',
    },
  },
  'filters': {
    'ex1': {
      'rules': {
        'to': 'abc@a.com',
      },
      'actions': [
        'join',
      ]
    },
  },
}


def create_config(path):
  try:
    with open(path, "w") as config_file:
      yaml.dump(cfg, stream=config_file, default_flow_style=False, encoding='utf-8')
  except IOError as e:
    logging.critical('Error while writing config_file %s: %s'
                     % (path, str(e)))
    logging.critical('Check the config file path and try again')
    return False
  return True


def check_config(path):
  if not os.path.exists(path):
    logging.warning('Config file %s doesn\'t exist. Trying to create'
                    % (path))
    if create_config(path):
      logging.warning('Created new config file %s. Edit it first to '
                      'configure your settings correctly & then run '
                      'program again' % (path))
    return False
  else:
    global cfg
    try:
      with open(path, "r") as config_file:
        cfg = yaml.load(config_file)
    except IOError as e:
      logging.critical('Error while reading config_file %s: %s'
                       % (path, str(e)))
      logging.critical('Check the config file path and try again')
      return False
    if not cfg or not 'filters' in cfg or not cfg['filters']:
      logging.critical('Empty or malformed config_file %s' % (path))
      logging.critical('Check the config file path and try again')
      return False
  return True


def read_config_plugin(filter_name, plugin_name):
  temp_cfg = {}
  if 'global' in cfg and plugin_name in cfg['global'] and cfg['global'][plugin_name]:
    temp_cfg = cfg['global'][plugin_name]
  try:
    for key in cfg['filters'][filter_name]['actions'][plugin_name].keys():
      temp_cfg[key] = cfg['filters'][filter_name]['actions'][key]
  except:
    # No specific options specified for this plugin in this action
    pass
  return temp_cfg
