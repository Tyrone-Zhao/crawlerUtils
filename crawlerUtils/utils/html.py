import html


__all__ = [
    "Html"
]


class Html():

    @classmethod
    def htmlUnescape(self, string):
        ''' 返回html.unescape(string) '''
        return html.unescape(string)
