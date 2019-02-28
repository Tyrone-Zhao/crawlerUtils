import xlrd
import json
import requests
import xlwt


__all__ = ["writeExcel", "readExcel", "readCookies", "getCookies", ]


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


def readCookies(session, filepath='cookies.txt'):
    """ 从txt文件读取cookies """
    # 如果能读取到cookies文件，执行以下代码，跳过except的代码，不用登录就能发表评论。
    cookies_txt = open(filepath, 'r')
    # 以reader读取模式，打开名为cookies.txt的文件。
    cookies_dict = json.loads(cookies_txt.read())
    # 调用json模块的loads函数，把字符串转成字典。
    cookies = requests.utils.cookiejar_from_dict(cookies_dict)
    # 把转成字典的cookies再转成cookies本来的格式。
    session.cookies = cookies
    # 获取cookies：就是调用requests对象（session）的cookies属性。
    cookies_txt.close()


def getCookies(session, url, headers, data={}, params={}, filepath='cookies.txt'):
    """ 登陆获取cookies """
    session.post(url, headers=headers, data=data, params=params)
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


# cd GitHub/crawlerUtils && rm -rf dist/* && python3 setup.py sdist bdist_wheel
# twine upload dist/*
# pip3 install --user --upgrade crawlerUtils
