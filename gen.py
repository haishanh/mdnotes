# -*- coding: utf-8 -*-
import re
import os
import sys
import yaml
import codecs
import markdown
from jinja2 import Template


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
        self.md_filename = filename
        pass
    def parse_frontmatter_and_strip(self):
        """
        Parse frontmatter and strip it
        """
        assert self.content

        tridash_re=re.compile('^-{3,5}\s*$', re.MULTILINE)
        m =  tridash_re.search(self.content)
        if m:
            start, end = m.span()
            # start is the 1st dash index
            # end is the index of '\n' in the same line
            self.frontmatter = self.content[:start]
            self.md = self.content[end+1:]
        else:
            self.frontmatter = None
            self.md = self.content
        if self.frontmatter:
            return yaml.load(self.frontmatter)
        else:
            return None

    def gen_md(self):
        """
        Render markdown file
        Return rendered html
        """
        # https://pythonhosted.org/Markdown/extensions/index.html
        extensions=['extra', 'codehilite', 'admonition',
                    'smarty', 'sane_lists', 'wikilinks']
        output_format = 'html5'
        html = markdown.markdown(self.md, extensions=extensions,
                                 output_format=output_format)
        return html

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

    def render(self):
        self.content = load_file(self.md_filename)
        print(self.parse_frontmatter_and_strip())
        self.article = self.gen_md()
        context = {}
        context['article'] = self.article
        with open('themes/templates/base.html') as f:
            content = f.read().decode('utf-8')
        template = Template(content)
        html = template.render(context)
        save_file(self.mk_path(), html)


def test():
    import glob
    mds = glob.glob('notes/*.md')
    for md in mds:
        note = Note(md)
        note.render()


if __name__ == '__main__':
    test()
