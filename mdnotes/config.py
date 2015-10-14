# -*- coding: utf-8 -*-

import os
import yaml
import shutil
import jinja2

from mdnotes.utils import prt_exit, safe_copy

def get_config_default():
    config = {}
    user = os.environ['LOGNAME']
    if user == 'root': user = None
    config['title'] = user + '\'s Notes' if user else 'Notes'
    config['source_dir'] = 'notes'
    config['output_dir'] = 'output'
    config['theme_dir'] = 'themes'
    config['root'] = '/'
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

    def load_config(self):
        config = get_config_default()
        config.update(get_config_from_file())
        self._config = config
        return config

    def url_for(self, file):
        return self._files.get(file, None)

    def load_resource(self, ignore_prefix='_'):
        """
        Move resource files to output dir

        Example:
            <themes/default/resources/css/main.css>
                will bee moved to
            <output/css/main.css>
        """
        # this method must be called after load_config method
        config = getattr(self, '_config', None)
        assert 'theme_dir' in config
        assert 'output_dir' in config

        topdir = config['theme_dir'] + '/resources'
        dst_dir = config['output_dir']

        topdir = topdir.rstrip(os.path.sep)
        assert os.path.isdir(topdir)

        self._files = {}
        for root, dirs, files in os.walk(topdir):
            for dir in dirs:
                if dir.startswith(ignore_prefix):
                    dirs.remove(dir)
            for file in files:
                if file.startswith(ignore_prefix): continue
                src_path = os.path.join(root, file)
                dst_sub = src_path[len(topdir):]
                # dst_sub should have os.path.sep prefixed
                dst_path = dst_dir + dst_sub
                safe_copy(src_path, dst_path)
                self._files[file] = dst_sub

    def load_all(self):
        config = self.load_config()
        env = template_init(os.path.join(config['theme_dir'], 'templates'))
        self.load_resource()
        config['url_for'] = self.url_for
        return config, env
