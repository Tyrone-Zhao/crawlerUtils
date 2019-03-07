from urllib.request import quote, unquote, urlopen
from .requests import Crawler


__all__ = [
    "urllibOpen", "urllibOpenText", "urllibOpenJson",
    "urllibOpenSoup", "urlencode", "urldecode",
]


def urlencode(string):
    ''' 返回中文的urlencode()结果 '''
    return quote(string)


def urldecode(string):
    ''' 返回urldecode()的中文结果 '''
    return unquote(string)


def urllibOpen(url, data=None):
    ''' 通过urllib.request.urlopen访问url，返回response对象
        selenium当前版本在访问某些响应头没有指定编码的url时，driver.page_source会返回乱码
    '''
    return urlopen(url, data)


def urllibOpenText(url, data=None, encoding="utf-8"):
    ''' 返回response.read().decode("utf-8") '''
    return urllibOpen(url, data).read().decode(encoding)


def urllibOpenJson(url, data=None, encoding="utf-8"):
    ''' 返回urllibOpenText及一些处理后的json '''
    text = urllibOpenText(url, data, encoding)
    text_json = Crawler.beautifulJson(text)

    return text_json


def urllibOpenSoup(url, data=None, encoding="utf-8", parser="html.parser"):
    ''' 返回BeautifulSoup(
            urllibOpenText(url, data=None, encoding="utf-8"), "html.parser"
        ) 
    '''
    return Crawler.getBSText(
        urllibOpenText(url, data=None, encoding="utf-8"), parser)
