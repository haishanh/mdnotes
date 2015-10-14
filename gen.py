# -*- coding: utf-8 -*-
import re
import os
import sys
import yaml
import jinja2
import shutil
import codecs
import markdown


# Tentativ globals / should be removed in the future
frontmatter_max_lines=2 # title * 1, date * 1

def save_file(filename, text):
    with codecs.open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def load_file(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def prt_exit(fmt):
    print(fmt)
    sys.exit(1)


class Note(object):

    def __init__(self, filename):
        # TODO do we have trouble if
        #      the filename is non ascii?
        self.md_filename = filename

    def set_tags(self, frontmatter):
        for key in frontmatter:
            if key.strip().lower() == 'tags':
                # public
                self.tags = frontmatter[key]
                return
        self.tags = None

    def set_title(self, frontmatter):
        for key in frontmatter:
            if key.strip().lower() == 'title':
                # public
                self.title = frontmatter[key]
                return
        self.title, _ = os.path.splitext(self.md_filename)

    def parse_frontmatter_and_strip(self):
        """
        Parse frontmatter and strip it
        """
        assert self._raw_content
        raw_content = self._raw_content

        tridash_re=re.compile('^-{3,5}\s*$', re.MULTILINE)
        m =  tridash_re.search(raw_content)
        if m:
            start, end = m.span()
            # start is the 1st dash index
            # end is the index of '\n' in the same line
            self.frontmatter = raw_content[:start]
            self.md = raw_content[end+1:]
        else:
            self.frontmatter = None
            self.md = raw_content
        if self.frontmatter:
            # strings in fm is unicode or ascii depending on whether
            # the object is an ascii string or not
            fm = yaml.load(self.frontmatter)
        else:
            fm = {}
        self.set_tags(fm)
        self.set_title(fm)

    def gen_md(self):
        """
        Render markdown file
        Return rendered html
        """
        # https://pythonhosted.org/Markdown/extensions/index.html
        extensions=['extra', 'codehilite', 'admonition',
                    'toc', 'smarty', 'sane_lists', 'wikilinks']
        # TODO
        extension_configs = {'toc' : {
                                    'anchorlink': True,
                                    'permalink': True
                                }
                            }
        output_format = 'html5'
        md = markdown.Markdown(extensions=extensions,
                               extension_configs = extension_configs,
                               output_format=output_format)
        html = md.convert(self.md)
        toc = getattr(md, 'toc', '')
        return html, toc

    def mk_path(self):
        # currenly
        html_dir = 'output'
        _ = os.path.basename(self.md_filename)
        basename, ext = os.path.splitext(_)
        new_dir = html_dir + os.path.sep + basename
        html_path = new_dir + os.path.sep + 'index.html'
        # if html_path exist, likely new_dir should have been created
        if not os.path.exists(html_path):
            try:
                os.makedirs(new_dir)
            except:
                prt_exit('Unable to create dir {0}'.format(new_dir))
        self.html_path = html_path
        return html_path

    def render(self, env):
        """
        Rendering the template note.html
        """

        # load markdown file
        self._raw_content = load_file(self.md_filename)
        # parse frontmatter and strip it
        self._fm = self.parse_frontmatter_and_strip()
        self.article, self.toc = self.gen_md()
        context = {}
        context['article'] = self.article
        context['toc'] = self.toc
        template = env.get_template('note.html')
        # with open('themes/templates/index.html') as f:
        #    content = f.read().decode('utf-8')
        #template = jinja2.Template(content)
        html = template.render(context)
        save_file(self.mk_path(), html)

def template_init(path='themes/templates'):
    """
    Jinja2 loader/env init
    Return a Jinja2.Environmant instance
    """
    loader = jinja2.FileSystemLoader(path)
    return jinja2.Environment(loader=loader)

def render_index_page(env, notes):
    context = {}
    context['notes'] = notes
    template = env.get_template('index.html')
    html = template.render(context)
    save_file(os.path.join('output', 'index.html'), html)
## Resources related

def move_res(topdir, ignore_prefix='_'):
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
            dst_path = 'output' + dst_sub
            try:
                dst_dir = os.path.dirname(dst_path)
                if not os.path.isdir(dst_dir): os.makedirs(dst_dir)
                shutil.copy(src_path, dst_path)
            except:
                prt_exit('Can not copy file {0} to {1}'.format(src_path, dst_path))



def test():
    env = template_init()
    import glob
    mds = glob.glob('notes/*.md')
    notes = []
    for md in mds:
        note = Note(md)
        note.render(env)
        notes.append(note)
        print(note.title)
    render_index_page(env, notes)
    move_res('themes/resources')


if __name__ == '__main__':
    test()
