# -*- coding: utf-8 -*-

import yaml

def get_global_config(config_file='config.yml'):
    print(config_file)
    with open(config_file) as f:
        config_raw = f.read().decode('utf-8')
    config = yaml.load(config_raw)
    return config

config_file='../config.yaml'
config = get_global_config()

print(config)
