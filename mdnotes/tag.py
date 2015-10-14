# -*- coding: utf-8 -*-

class Tag(object):
    def __init__(self, name):
        # name could be unicode
        self.name = name
        # TODO config['root']
        self.link = '/tags/' + name 
        self.count = 0
        self.notes = []
