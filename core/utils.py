import re


def remove_html_tags(val):
    open_tag = '<[^>]*>'
    close_tag = r'</[^>]*>'

    val = re.sub(open_tag, '', val[::])
    val = re.sub(close_tag, '', val[::])

    return val
