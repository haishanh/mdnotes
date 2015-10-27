# -*- coding: utf-8 -*-

import os

from mdnotes.utils import ensure_path, save_file


class Category(object):
    def __init__(self, name, config):
        # name could be unicode
        self.name = name
        self.link = config['root'] + 'categories/' + name + '/'
        self.count = 0
        self.notes = []
        # private
        self._config = config

    def render(self, env, context):

        context['category'] = self
        template = env.get_template('category.html')
        html = template.render(context)

        target_path = os.path.join(self._config['output_dir'],
                                   self._config['root'].strip('/'),
                                   'categories', self.name, 'index.html')
        ensure_path(target_path)

        save_file(target_path, html)
