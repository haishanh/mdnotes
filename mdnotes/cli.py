# -*- coding: utf-8 -*-
import os
import sys
import shutil
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from mdnotes.config import Config
from mdnotes.context import Context
from mdnotes.note import Note
from mdnotes.index import Index
from mdnotes.utils import prt_exit

def parse_arguments():
    description = 'mdnotes - turn your markdown files into\n' \
                  'beautiful well structured html web page'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-b', '--build', action='store_true',
                        help='build notes')
    parser.add_argument('-s', '--serve', action='store_true',
                        help='start server')
    parser.add_argument('-c', '--cleanup', action='store_true',
                        help='clean up')
    return vars(parser.parse_args())

def build():
    config = Config()
    config, env = config.load_all()
    context = Context()
    context.update(config)
    tags = {}
    # env = template_init()
    import glob
    mds = glob.glob(config['source_dir'] + '/*.md')
    notes = []
    for md in mds:
        note = Note(md, config, tags)
        note.render(env, context.note)
        notes.append(note)
        print(note.title)
    for tag in tags:
        tags[tag].render(env, context.tag)
    index = Index(config)
    index.render(env, context.index, notes, tags=tags.values())
    # move_res(config['theme_dir'] + '/resources', config['output_dir'])


def serve():
    config = Config()
    config = config.load_config()
    if not os.path.isdir(config['output_dir']):
        print('Output files not found...building...')
        build()
    os.chdir(config['output_dir'])

    import SimpleHTTPServer
    import SocketServer
    PORT = 8000
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print("serving at port {0}".format(PORT))
    httpd.serve_forever()

def cleanup():
    config = Config()
    config = config.load_config()
    try:
        shutil.rmtree(config['output_dir'])
    except:
        prt_exit('Can not cleanup {0}'.format(config['output_dir']))

def main():
    args = parse_arguments()
    if args['build']:
        build()
    if args['serve']:
        serve()
    if args['cleanup']:
        cleanup()

if __name__ == '__main__':
    main()
