# -*- coding: utf-8 -*-
import os
import sys
import time
import shutil
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from mdnotes.config import Config
from mdnotes.context import Context
from mdnotes.note import Note
from mdnotes.index import Index
from mdnotes.utils import prt_exit, md_files_generator

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
    categories = {}
    # env = template_init()
    mds = md_files_generator(config['source_dir'])
    notes = []
    print('Building notes...')
    before = time.time()
    count = 0
    for md in mds:
        note = Note(md, config, tags, categories)
        note.render(env, context.note)
        notes.append(note)
        count += 1
        print( ' ' * 10 + note.title)
    now = time.time()
    print("Generate {0} entries in {1:.3f}s".format(count, now-before))
    before = time.time()
    print('Building index...')
    for tag in tags:
        tags[tag].render(env, context.tag)
    for cate in categories:
        categories[cate].render(env, context.category)
    index = Index(config)
    index.render(env, context.index, notes, categories=categories.values(),
                 tags=tags.values())
    now = time.time()
    print("Generate index in {0:.3f}s".format(now-before))
    # move_res(config['theme_dir'] + '/resources', config['output_dir'])


def serve():
    config = Config()
    config = config.load_config()
    if not os.path.isdir(config['output_dir']):
        print('Output files not found...building...')
        build()

    port = 8000
    host = '0.0.0.0'
    try:
        from tornado import ioloop
        from tornado import web
        application = web.Application([
            (r"/(.*)", web.StaticFileHandler, {
                "path": config['output_dir'],
                "default_filename": "index.html"
            })
        ])
        application.listen(port=port, address=host)
        print('Running at: http://{0}:{1}/'.format(host, port))
        try:
            ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            print('Stopping server...')
    except:
        import SimpleHTTPServer
        import SocketServer
        os.chdir(config['output_dir'])
        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = SocketServer.TCPServer((host, port), Handler)
        httpd.allow_reuse_address = True
        print('Running at: http://{0}:{1}/'.format(host, port))
        httpd.serve_forever()


def cleanup():
    config = Config()
    config = config.load_config()
    try:
        shutil.rmtree(config['output_dir'])
    except:
        prt_exit('Can not cleanup directory {0}\n'
                 'Maybe it does not exist or '
                 'we have permission issue'.format(config['output_dir']))

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
