# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from mdnotes.config import Config
from mdnotes.note import Note
from mdnotes.index import Index
from mdnotes.utils import move_res

def main():
    config = Config()
    config, env = config.load()
    print('current dir is: ' + os.getcwd())
    # env = template_init()
    import glob
    mds = glob.glob(config['source_dir'] + '/*.md')
    notes = []
    for md in mds:
        note = Note(md, config)
        note.render(env)
        notes.append(note)
        print(note.title)
    index = Index(config)
    index.render(env, notes)
    move_res(config['theme_dir'] + '/resources', config['output_dir'])

if __name__ == '__main__':
    main()
