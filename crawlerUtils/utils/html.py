import html


__all__ = [
    "Html"
]


class Html():

    def __init__(self, **kwargs):
        super().__init__()

    @classmethod
    def htmlUnescape(self, string):
        """ 返回html.unescape(string) """
        return html.unescape(string)

    @classmethod
    def htmlescape(cls, string):
        """ 返回html.escape(string) """
        return html.escape(string)