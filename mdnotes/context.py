# -*- coding: utf-8 -*-

class Context(object):
    def __init__(self):
        self.share = {}
        self.index = {}
        self.note = {}

    def update(self, config):
        """
        """
        share = self.share
        index = self.index
        note = self.note

        ## function
        share['url_for'] = config['url_for']

        ## head
        share['title'] = config['title']

        ## body
        share['header_title'] = config['title']

        index.update(share)
        note.update(share)
