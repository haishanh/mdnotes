# -*- coding: utf-8 -*-
import os
import sys
import shutil
import codecs

def save_file(filename, text):
    with codecs.open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def load_file(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def prt_exit(fmt):
    print(fmt)
    sys.exit(1)

def move_res(topdir, dst_dir, ignore_prefix='_'):
    topdir = topdir.rstrip(os.path.sep)
    assert os.path.isdir(topdir)
    for root, dirs, files in os.walk(topdir):
        for dir in dirs:
            if dir.startswith(ignore_prefix):
                dirs.remove(dir)
        for file in files:
            if file.startswith(ignore_prefix): continue
            src_path = os.path.join(root, file)
            dst_sub = src_path[len(topdir):]
            # dst_sub should have os.path.sep prefixed
            dst_path = dst_dir + dst_sub
            try:
                dirname = os.path.dirname(dst_path)
                if not os.path.isdir(dirname): os.makedirs(dirname)
                shutil.copy(src_path, dst_path)
            except:
                prt_exit('Can not copy file {0} to {1}'.format(src_path, dst_path))
