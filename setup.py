from setuptools import setup

setup(
    name='mdnotes',
    author='HAN Haishan',
    author_email='haishanhan@gmail.com',
    packages=['mdnotes'],
    install_requires=[
        'markdown>=2.6.2', # markdown
        'PyYAML>=3.11',    # config file / frontmatter
        'Pygments>=2.0.2', # codehilite
        'Jinja2>=2.8',     # templating
        'tornado>=4.2.1'   # static server
    ],
    entry_points='''
        [console_scripts]
        note=mdnotes.cli:main
    '''
)
