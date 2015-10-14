# -*- coding: utf-8 -*-
import os

from mdnotes.utils import save_file

class Index(object):
    """
    Model the index page
    """
    def __init__(self, config):
        self._config = config

    def render(self, env, notes):
        context = {}
        context['url_for'] = self._config['url_for']
        context['notes'] = notes
        template = env.get_template('index.html')
        html = template.render(context)
        output_dir = self._config['output_dir']
        save_file(os.path.join(output_dir, 'index.html'), html)
