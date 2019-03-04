import html


__all__ = [
    "unescapeHtml"
]


def unescapeHtml(string):
    ''' 返回html.unescape(string) '''
    return html.unescape(string)
