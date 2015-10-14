# -*- coding: utf-8 -*-

import yaml
import jinja2

def get_global_config(config_file='config.yml'):
    print(config_file)
    with open(config_file) as f:
        config_raw = f.read().decode('utf-8')
    config = yaml.load(config_raw)
    return config

def template_init(path='../themes/templates'):
    """
    Jinja2 loader/env init
    Return a Jinja2.Environmant instance
    """
    loader = jinja2.FileSystemLoader(path)
    return jinja2.Environment(loader=loader)
