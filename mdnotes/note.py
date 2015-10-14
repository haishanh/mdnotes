# -*- coding: utf-8 -*-
import re
import os
import yaml
import markdown

from mdnotes.utils import save_file, load_file, prt_exit

class Note(object):

    def __init__(self, filename, config):
        # TODO do we have trouble if
        #      the filename is non ascii?
        bname = os.path.basename(filename)
        self.name, ext = os.path.splitext(bname)
        self.filename = filename
        self._config = config

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
        self.title, _ = os.path.splitext(self.filename)

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

    def set_link(self):
        self.link = self._config['root'] + self.name

    def mk_path(self, html_dir):
        _ = os.path.basename(self.filename)
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
        self._raw_content = load_file(self.filename)
        # parse frontmatter and strip it
        self._fm = self.parse_frontmatter_and_strip()
        self.article, self.toc = self.gen_md()
        context = {}
        context['url_for'] = self._config['url_for']
        context['article'] = self.article
        context['toc'] = self.toc
        template = env.get_template('note.html')
        html = template.render(context)
        target_path = self.mk_path(self._config['output_dir'])
        save_file(target_path, html)
        self.set_link()
