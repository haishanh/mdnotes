# -*- coding: utf-8 -*-

import os
import yaml
import jinja2
import subprocess

from mdnotes.utils import prt_exit, safe_copy


def get_config_default():
    """
    Initialize a basic workable config
    This config will be updated by subsequent procedures
    """
    config = {}
    user = os.environ['LOGNAME']
    if user == 'root':
        user = None
    config['title'] = user + '\'s Notes' if user else 'Notes'
    config['author'] = 'Jon Doe'
    config['menu'] = {}
    config['source_dir'] = 'notes'
    config['output_dir'] = 'output'
    config['theme_dir'] = 'themes'
    config['per_page'] = 10
    config['root'] = '/'
    config['highlight_style'] = 'friendly'
    return config


def normalize_config(config):
    """
    Normalize config in case of error config.yml

        - remove trailing seperator for dir related config
        - for url "dir" trailing slash is needed,
          config['root'] should be '/' or '/notes/' style
    """

    for key in ['source_dir', 'output_dir', 'theme_dir']:
        config[key] = os.path.expanduser(config[key])
        config[key] = config[key].rstrip(os.path.sep)

    if not config['root'].endswith('/'):
        config['root'] += '/'
    if not config['root'].startswith('/'):
        config['root'] = '/' + config['root']

    config['per_page'] = int(config['per_page'])
    if config['per_page'] < 1:
        print('Warning: "per_page" set to {0} is '
              'not allowed, use 1 instead'.format(config['per_page']))
        config['per_page'] = 1


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


def compile_less(path):
    """
    Using less.js to compile main.less to main.css
    """
    infile = os.path.join(path, 'main.less')
    outfile = os.path.join(path, 'main.css')
    if os.path.isfile(infile):
        which = subprocess.Popen('which less', shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        which.wait()
        if which.returncode != 0:
            print('Warning: less.js compiler not found')
            if not os.path.isfile(outfile):
                prt_exit('Can not build main.css')
            return
        cmd = 'lessc ' + infile + ' ' + outfile
        lessc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        lessc.wait()
        if lessc.returncode != 0:
            prt_exit('Can not compile {0} to {1}'.format(infile, outfile))


def generate_codehilite(path, style):
    """
    Generate pygments stylesheet
    """
    outfile = os.path.join(path, 'pygments.less')
    cmd = 'pygmentize -S ' + style + \
          ' -f html -a .codehilite > ' + \
          outfile
    # TODO Judge if pygments.less changed?
    which = subprocess.Popen('which pygmentize', shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    which.wait()
    pygmentize = subprocess.Popen(cmd, shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    pygmentize.wait()
    if pygmentize.returncode != 0:
        prt_exit('Can not generate style {0}'.format(outfile))


class Config(object):
    def __init__(self):
        pass

    def load_config(self):
        config = get_config_default()
        config.update(get_config_from_file())
        normalize_config(config)
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

        topdir = os.path.join(config['theme_dir'], 'resources')
        dst_dir = os.path.join(config['output_dir'], config['root'].strip('/'))

        topdir = topdir.rstrip(os.path.sep)
        assert os.path.isdir(topdir)

        self._files = {}
        for root, dirs, files in os.walk(topdir):
            for dir in dirs:
                if dir.startswith(ignore_prefix):
                    dirs.remove(dir)
            for file in files:
                if file.startswith(ignore_prefix):
                    continue
                src_path = os.path.join(root, file)
                dst_sub = src_path[len(topdir):]
                # dst_sub should have os.path.sep prefixed
                dst_path = dst_dir + dst_sub
                safe_copy(src_path, dst_path)
                self._files[file] = config['root'].rstrip('/') + dst_sub

    def load_all(self):
        config = self.load_config()
        env = template_init(os.path.join(config['theme_dir'], 'templates'))
        generate_codehilite(os.path.join(config['theme_dir'], 'resources',
                                         'css'),
                            config['highlight_style'])
        compile_less(os.path.join(config['theme_dir'], 'resources', 'css'))
        self.load_resource()
        config['url_for'] = self.url_for
        return config, env
