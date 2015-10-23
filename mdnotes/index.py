# -*- coding: utf-8 -*-
import os

from mdnotes.utils import save_file


class Index(object):
    """
    Model the index page
    """
    def __init__(self, config):
        self._config = config

    def render(self, env, context, notes, categories, tags):
        context['url_for'] = self._config['url_for']
        context['notes'] = notes
        context['categories'] = categories
        context['tags'] = tags
        template = env.get_template('index.html')
        html = template.render(context)
        output_dir = self._config['output_dir']
        save_file(os.path.join(output_dir,
                               self._config['root'].strip('/'),
                               'index.html'), html)
