# -*- coding: utf-8 -*-
import os

from mdnotes.utils import save_file, ensure_path


class Index(object):
    """
    Model the index page
    """
    def __init__(self, config):
        self._config = config

    def render(self, env, context, notes, categories, tags):
        per_page = self._config['per_page']
        page_total = ( len(notes) + per_page - 1 ) / per_page
        context['url_for'] = self._config['url_for']
        context['categories'] = categories
        context['tags'] = tags
        # context['notes'] = notes
        output_dir = self._config['output_dir']
        root = self._config['root']
        # hardcode
        # don't leave this to user
        page = 'page'
        prev_text = '&laquo; Older'
        next_text = 'Newer &raquo;'
        template = env.get_template('index.html')
        for page_id in range(page_total):
            start = page_id * per_page
            context['notes'] = notes[start:start+per_page]
            context['pagination'] = paginate(page_id+1, page_total,
                                             root, page,
                                             prev_text, next_text)
            html = template.render(context)
            if page_id == 0:
                target_path =  os.path.join(output_dir,
                                            self._config['root'].strip('/'),
                                            'index.html')
            else:
                target_path = os.path.join(output_dir,
                                           self._config['root'].strip('/'),
                                           page,
                                           str(page_id+1),
                                           'index.html')
            ensure_path(target_path)
            save_file(target_path, html)




def paginate(current, total, root, page, prev_text, next_text):
    """
    Return paginator html string

    current: the current page number(starting from 1)
    total: the total page number
    root: the url root(string)
    page: the dir for sub page(string)
    prev_text and next_text are strings
    """
    if total <= 1:
        return ''
    html = ''
    def href(id):
        if id == 1:
            return root
        else:
            return root + page + '/' + str(id) + '/'
    if current > 1:
        html += '<a href="' + href(current-1) + '" ' + 'class="prev">' + \
                prev_text + '</a>\n'
    start = max(current-2, 1)
    end = min(start+4, total)
    while start <= end:
        if start == current:
            html += '<span class="page-num current">' + str(current) + '</span>\n'
        else:
            html += '<a href="' + href(start) + '" class="page-num">'+ \
                    str(start) + '</a>\n'
        start += 1
    if current < total:
        html += '<a href="' + href(current+1) + '" ' + 'class="next">' + \
                next_text + '</a>\n'
    return html
