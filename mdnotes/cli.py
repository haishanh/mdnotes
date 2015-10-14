# -*- coding: utf-8 -*-
import os
import sys
import shutil
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from mdnotes.config import Config
from mdnotes.note import Note
from mdnotes.index import Index
from mdnotes.utils import move_res, prt_exit

def parse_arguments():
    description = 'mdnotes - turn your markdown files into\n' \
                  'beautiful well structured html web page'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-b', '--build', action='store_true',
                        help='build notes')
    parser.add_argument('-c', '--cleanup', action='store_true',
                        help='clean up')
    return vars(parser.parse_args())

def build():
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

def cleanup():
    config = Config()
    config, env = config.load()
    try:
        shutil.rmtree(config['output_dir'])
    except:
        prt_exit('Can not cleanup {0}'.format(config['output_dir']))

def main():
    args = parse_arguments()
    if args['build']:
        build()
    if args['cleanup']:
        cleanup()

if __name__ == '__main__':
    main()
