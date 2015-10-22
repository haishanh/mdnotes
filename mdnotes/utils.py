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

def ensure_dir(dir):
    """
    Ensure dir is exist
     - create it if it does not exit
     - immdiate exit if it can not be created
    """
    if not os.path.isdir(dir):
        try:
            os.makedirs(dir)
        except:
            prt_exit('DIR {0} not exist and can not be created'.format(dir))

def ensure_path(path):
    """
    Ensure path' parent dirs exits
    """
    dir = os.path.dirname(path)
    ensure_dir(dir)

def safe_copy(src, dst):
    if not os.path.exists(src):
        prt_exit('Source file {0} not exist'.format(src))
    if dst.endswith(os.path.sep):
        ensure_dir(dst)
    else:
        ensure_path(dst)
    # there is possiblity that the dst DO exist
    # but we DO NOT have permission to write there
    try:
        shutil.copy(src, dst)
    except:
        prt_exit('Can not copy from {0} to {1}'.format(src, dst))


def md_files_generator(topdir, ignore_prefix='_'):
    assert os.path.isdir(topdir)
    for root, dirs, files in os.walk(topdir):
        for dir in dirs:
            if dir.startswith(ignore_prefix):
                dirs.remove(dir)
        for file in files:
            if file.startswith(ignore_prefix) or not file.endswith('.md'):
                continue
            mdfile =  os.path.join(root, file)
            yield mdfile


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
