import xlrd
import requests
import xlwt
from bs4 import BeautifulSoup
import base64
import os
import json


__all__ = [
    "writeExcel", "readExcel", "readCookies", "getCookies", "getPostJson",
    "getGetJson", "getPostText", "getGetText", "getPostSoup", "getGetSoup",
    "captchaB64decode"
]


def writeExcel(row, column, label, worksheet=None, workbook=None, sheetname=None,
               encoding="ascii"):
    """ 写入Excel """
    if workbook:
        wb = workbook
    else:
        wb = xlwt.Workbook(encoding=encoding)
    if worksheet:
        ws = worksheet
    elif sheetname:
        ws = wb.add_sheet(sheetname)
    else:
        raise ValueError("没有传入Excel表，或者表名!")

    ws.write(row, line, label=label)
    return ws, wb


def readExcel(excelpath=None, row_num=None, workbook=None, worksheet=None, column_num=None,
              sheetindex=0, sheetname=None, cell_row_num=None, cell_column_num=None,
              nrows=False, ncols=False):
    """ 读取Excel, 行数和列数从1开始，单元格也从1开始 """
    if workbook and sheetname:
        ws = workbook.sheet_by_name(sheetname)
        return ws
    elif workbook and sheetindex:
        ws = workbook.sheet_by_index(sheetindex)
        return ws
    elif workbook:
        wb = workbook
    elif excelpath:
        wb = xlrd.open_workbook(excelpath)
    elif worksheet:
        ws = worksheet
    else:
        raise ValueError("缺少Excel路径或Excel对象，或者Sheet对象！")

    if nrows:
        return ws.nrows
    elif ncols:
        return ws.ncols

    if cell_row_num and cell_column_num:
        return ws.cell(cell_row_num-1, cell_column_num-1).value
    elif row_num:
        return ws.row_values(row_num-1)
    elif column_num:
        return ws.col_values(column_num-1)

    return wb.sheets()


def readCookies(session, filepath='crawlerUtilsCookies.txt'):
    """ 从txt文件读取cookies """
    # 如果能读取到cookies文件，执行以下代码，跳过except的代码，不用登录就能发表评论。
    try:
        cookies_txt = open(filepath, 'r')
        # 以reader读取模式，打开名为cookies.txt的文件。
        cookies_dict = cookies_txt.read()
        if cookies_dict:
            cookies_dict = json.loads(cookies_dict)
        else:
            raise FileNotFoundError
        # 调用json模块的loads函数，把字符串转成字典。
        cookies = requests.utils.cookiejar_from_dict(cookies_dict)
        # 把转成字典的cookies再转成cookies本来的格式。
        session.cookies = cookies
        # 获取cookies：就是调用requests对象（session）的cookies属性。
        cookies_txt.close()
    except FileNotFoundError:
        pass


def getCookies(session, url, headers, data={}, params={}, jsons={}, filepath='crawlerUtilsCookies.txt'):
    """ 登陆获取cookies """
    session.post(url, headers=headers, data=data, params=params, json=jsons)
    # 在会话下，用post发起登录请求。
    cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)
    # 把cookies转化成字典。
    cookies_str = json.dumps(cookies_dict)
    # 调用json模块的dump函数，把cookies从字典再转成字符串。
    f = open(filepath, 'w')
    # 创建名为cookies.txt的文件，以写入模式写入内容
    f.write(cookies_str)
    # 把已经转成字符串的cookies写入文件
    f.close()
    # 关闭文件


def getPostJson(session, url, headers={}, params={}, data={}, jsons={}):
    """ 获取Post请求的response.json() """
    if params or data or json:
        res = session.post(
            url, headers=headers, params=params, data=data, json=jsons
        )
        res_json = res.json()
        return res_json
    else:
        raise ValueError("缺少params参数或者data参数，或者json参数！")


def getGetJson(session, url, headers={}, params={}, data={}, jsons={}):
    """ 获取Get请求的response.json() """
    res = session.get(
        url, headers=headers, params=params, data=data, json=jsons
    )
    res_json = res.json()

    return res_json


def getPostText(session, url, headers={}, params={}, data={}, jsons={}):
    """ 获取Post请求的response.text """
    if params or data or json:
        res = session.post(
            url, headers=headers, params=params, data=data, json=jsons
        )
        return res.text
    else:
        raise ValueError("缺少params参数或者data参数，或者json参数！")


def getGetText(session, url, headers={}, params={}, data={}, jsons={}):
    """ 获取Get请求的response.text """
    res = session.get(
        url, headers=headers, params=params, data=data, json=jsons
    )
    return res.text


def getPostSoup(session, url, headers={}, params={}, data={}, jsons={}, parser="html.parser"):
    """ 获取Post请求的BeautifulSoup实例 """
    if params or data or json:
        res = session.post(
            url, headers=headers, params=params, data=data, json=jsons
        )
        soup = BeautifulSoup(res.text, parser)
        return soup
    else:
        raise ValueError("缺少params参数或者data参数，或者json参数！")


def getGetSoup(session, url, headers={}, params={}, data={}, jsons={}, parser="html.parser"):
    """ 获取Get请求的BeautifulSoup实例 """
    res = session.get(
        url, headers=headers, params=params, data=data, json=jsons
    )
    soup = BeautifulSoup(res.text, parser)
    return soup


def captchaB64decode(b64data, filename_unextension="b64temp", dir_path=None):
    """ base64文本解码成文件, 返回文件路径 """
    head_and_content = b64data.split(",")
    extension = head_and_content[0].rsplit("/")[1].split(";")[0]
    filename = filename_unextension + "." + extension
    if dir_path:
        filepath = dir_path + "/" + filename
    else:
        filepath = os.path.dirname(__file__) + \
            "/captcha/captcha_set/" + filename
    with open(filepath, 'wb') as f:
        content_decode = base64.b64decode(head_and_content[1])
        f.write(content_decode)
    # print(f"验证码获取成功，保存路径为：{filepath}")
    return filepath, extension
