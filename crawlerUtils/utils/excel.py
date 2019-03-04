import xlrd
import xlwt


__all__ = [
    "writeExcel", "readExcel",
]


def writeExcel(row=None, column=None, label=None, worksheet=None, workbook=None, sheetname=None,
               encoding="ascii"):
    """ 写入Excel """
    ws = None
    if workbook:
        wb = workbook
    else:
        wb = xlwt.Workbook(encoding=encoding)
    if worksheet:
        ws = worksheet
    elif sheetname:
        ws = wb.add_sheet(sheetname)

    if row != None and column != None and label != None and ws:
        ws.write(row, column, label=label)

    if ws:
        return ws
    else:
        return wb


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
