# -*- coding: utf-8 -*-

import os

from mdnotes.utils import ensure_path, save_file

class Tag(object):
    def __init__(self, name, config):
        # name could be unicode
        self.name = name
        self.link = config['root'] + 'tags/' + name
        self.count = 0
        self.notes = []
        # private
        self._config = config

    def render(self, env, context):

        context['tag'] = self
        template = env.get_template('tag.html')
        html = template.render(context)

        target_path = os.path.join(self._config['output_dir'],
                                   'tags', self.name, 'index.html')
        ensure_path(target_path)

        save_file(target_path, html)
