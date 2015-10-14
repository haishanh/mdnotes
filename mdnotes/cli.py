# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from mdnotes.config import template_init
from mdnotes.note import Note
from mdnotes.index import Index
from mdnotes.utils import move_res

def main():
    print('current dir is: ' + os.getcwd())
    env = template_init()
    import glob
    mds = glob.glob('../notes/*.md')
    notes = []
    for md in mds:
        note = Note(md)
        note.render(env)
        notes.append(note)
        print(note.title)
    index = Index()
    index.render(env, notes)
    move_res('../themes/resources')

if __name__ == '__main__':
    main()
