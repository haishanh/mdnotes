# -*- coding: utf-8 -*-

import os
import yaml
import jinja2

from mdnotes.utils import prt_exit

def get_config_default():
    config = {}
    user = os.environ['LOGNAME']
    if user == 'root': user = None
    config['title'] = user + '\'s Notes' if user else 'Notes'
    config['source_dir'] = 'notes'
    config['output_dir'] = 'output'
    config['theme_dir'] = 'themes'
    return config


def get_config_from_file(config_file='config.yml'):
    try:
        with open(config_file) as f:
            config_raw = f.read().decode('utf-8')
    except:
        prt_exit('Can not open {0}'.format(config_file))
    config = yaml.load(config_raw)
    return config

def template_init(path='../themes/templates'):
    """
    Jinja2 loader/env init
    Return a Jinja2.Environmant instance
    """
    loader = jinja2.FileSystemLoader(path)
    return jinja2.Environment(loader=loader)

class Config(object):
    def __init__(self):
        pass
    def load(self):
        config = get_config_default()
        config.update(get_config_from_file())
        env = template_init(os.path.join(config['theme_dir'], 'templates'))
        return config, env
