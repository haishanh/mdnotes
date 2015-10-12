import re
import yaml
import codecs


# Tentativ globals / should be removed in the future
frontmatter_max_lines=2 # title * 1, date * 1

def save_file(filename, text):
    with codecs.open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def load_file(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        return f.read()


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
            self.frontmatter = ''
            self.md = self.content
        return yaml.load(self.frontmatter)

    def render_md(self):
        """
        Render markdown file
        Return rendered html
        """
        pass
    def render(self):
        self.content = load_file(self.md_filename)
        print(self.parse_frontmatter_and_strip())


def test():
    import glob
    mds = glob.glob('notes/*.md')
    for md in mds:
        note = Note(md)
        note.render()


if __name__ == '__main__':
    test()
