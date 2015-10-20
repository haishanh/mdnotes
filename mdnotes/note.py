# -*- coding: utf-8 -*-
import re
import os
import yaml
import markdown

from mdnotes.utils import save_file, load_file, \
                          ensure_path, prt_exit
from mdnotes.tag import Tag


def process_toc(toc):
    """
    This will keep 3 levels of headings

    In the example below, "heading5" will be removed

    ## heading2
    ### heading3
    #### heading4
    ##### heading5
    """
    depth = 3
    stack = []
    to_remove = []
    index = 0
    while True:
        index = toc.find('<', index)
        if index < 0:
            break
        if toc[index: index+3] == '<ul':
            if len(stack) == depth:
                to_remove.append(index)
            stack.append(index)
        if toc[index: index+4] == '</ul':
            # len('</ul>')
            index += 5
            stack.pop()
            if len(stack) == depth:
                to_remove.append(index)
        index += 1
    to_remove.insert(0, 0)
    to_remove.append(len(toc))
    retstr = ''
    index = 0
    while index < len(to_remove):
        retstr += toc[to_remove[index]:to_remove[index+1]]
        index += 2
    return retstr


class Note(object):

    def __init__(self, filename, config, global_tags):
        # TODO do we have trouble if
        #      the filename is non ascii?
        bname = os.path.basename(filename)
        name, ext = os.path.splitext(bname)
        # Public
        self.name = name
        self.filename = filename
        self.title = ''
        self.category = ''
        self.article = ''
        self.toc = ''
        self.tags = []
        self.link = ''
        # Private
        self._global_tags = global_tags
        self._config = config

    def set_tags(self, frontmatter):
        gtags = self._global_tags
        for key in frontmatter:
            if key.strip().lower() == 'tags':
                # public
                tags = frontmatter[key]
                # it's possible people put 'tags:'
                # in fm, but leave it blank
                if tags is None:
                    return
                for tag in tags:
                    if tag not in gtags:
                        gtags[tag] = Tag(tag, self._config)
                    this_tag = gtags[tag]
                    this_tag.notes.append(self)
                    this_tag.count += 1
                    self.tags.append(this_tag)

    def set_title(self, frontmatter):
        for key in frontmatter:
            if key.strip().lower() == 'title':
                # public
                self.title = frontmatter[key]
                return
        self.title, _ = os.path.splitext(self.filename)

    def set_category(self, frontmatter):
        for key in frontmatter:
            if key.strip().lower().startswith('cate'):
                # public
                self.category = frontmatter[key]
                return
        self.category = 'general'

    def parse_frontmatter_and_strip(self):
        """
        Parse frontmatter and strip it
        """
        assert self._raw_content
        raw_content = self._raw_content

        tridash_re = re.compile('^-{3,5}\s*$', re.MULTILINE)
        m = tridash_re.search(raw_content)
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
        self.set_category(fm)

    def gen_md(self):
        """
        Render markdown file
        Return rendered html
        """
        # https://pythonhosted.org/Markdown/extensions/index.html
        extensions = ['extra', 'codehilite', 'admonition',
                      'toc', 'smarty', 'sane_lists', 'wikilinks']
        # TODO
        extension_configs = {'toc': {
                                    'anchorlink': False,
                                    'permalink': False
                                }
                            }
        output_format = 'html5'
        md = markdown.Markdown(extensions=extensions,
                               extension_configs=extension_configs,
                               output_format=output_format)
        html = md.convert(self.md)
        toc = getattr(md, 'toc', '')
        if toc:
            toc = process_toc(toc)
        return html, toc

    def set_link(self):
        self.link = self._config['root'] + self.category + '/' + self.name

    def mk_path(self, html_dir):
        new_dir = html_dir + os.path.sep + self.name
        html_path = new_dir + os.path.sep + 'index.html'
        # if html_path exist, likely new_dir should have been created
        if not os.path.exists(html_path):
            try:
                os.makedirs(new_dir)
            except:
                prt_exit('Unable to create dir {0}'.format(new_dir))
        self.html_path = html_path
        return html_path

    def render(self, env, context):
        """
        Rendering the template note.html
        """

        # load markdown file
        self._raw_content = load_file(self.filename)
        # parse frontmatter and strip it
        self._fm = self.parse_frontmatter_and_strip()
        self.article, self.toc = self.gen_md()
        self.set_link()
        context['title'] = self.title + ' | ' + context['title']
        context['note'] = self
        template = env.get_template('note.html')
        html = template.render(context)
        target_path = os.path.join(self._config['output_dir'],
                                   self.category, self.name, 'index.html')
        # target_path = self.mk_path(self._config['output_dir'])
        ensure_path(target_path)

        save_file(target_path, html)
